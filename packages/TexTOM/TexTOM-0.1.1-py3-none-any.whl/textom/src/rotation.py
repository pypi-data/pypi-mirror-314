import numpy as np
from numba import njit, prange

from ..config import data_type

"""
Some functions helping to convert between different rotation conventions,
to perform rotations and to handle quaternions
"""

def XAfromOTP(ome,tta,phi):
    """ Creates an axis-angle vector from 3 angles omega, theta, phi

    Parameters
    ----------
    omega : ndarray, float
        rotation angle, usually ∈[0,pi)
    theta : ndarray, float
        polar angle of the rotation axis, usually ∈[0,pi)
    phi : ndarray, float
        azimutal angle of the rotation axis, usually ∈[0,2pi)

    Return values
    ------------
    XA : 2D ndarray, float
        array of axis-angle vectors with 3 entries
    """
    XA = np.column_stack([
            ome * np.sin(tta) * np.cos(phi),
            ome * np.sin(tta) * np.sin(phi),
            ome * np.cos(tta)
        ])
    return XA

def OTPfromXA(V):
    """ Extracts the 3 angles omega, theta, phi from an axis-angle vector

    Parameters
    ----------
    XA : 2D ndarray, float
        array of axis-angle vectors with 3 entries

    Return values
    ------------
    omega : ndarray, float
        rotation angle, usually ∈[0,pi)
    theta : ndarray, float
        polar angle of the rotation axis, usually ∈[0,pi)
    phi : ndarray, float
        azimutal angle of the rotation axis, usually ∈[0,2pi)
    """
    ome = np.sqrt((V**2).sum(axis=1))
    tta = np.arccos(np.divide(V[:,2],ome, where=(ome!=0)))
    phi = np.sign(V[:,1]) * np.arccos(
        np.divide(V[:,0],np.sqrt(V[:,0]**2+V[:,1]**2), where=[a[0]!=0 or a[1]!=0 for a in V]) )
    return ome, tta, phi

def RodfromOTP(ome,tta,phi):
    """ Creates a Rodrigues vector from 3 angles omega, theta, phi

    Parameters
    ----------
    omega : ndarray, float
        rotation angle, usually ∈[0,pi)
    theta : ndarray, float
        polar angle of the rotation axis, usually ∈[0,pi)
    phi : ndarray, float
        azimutal angle of the rotation axis, usually ∈[0,2pi)

    Return values
    ------------
    Rod : 2D ndarray, float
        array of Rodrigues vectors with 3 entries
    """
    Rod = np.column_stack([
            np.tan(ome/2) * np.sin(tta) * np.cos(phi),
            np.tan(ome/2) * np.sin(tta) * np.sin(phi),
            np.tan(ome/2) * np.cos(tta)
        ])
    return Rod

@njit(parallel=True)
def QfromOTP( OTP ):
    """ Creates Quaternions from 3 angles omega, theta, phi

    Parameters
    ----------
    OTP : 2D ndarray, float
        stack of angles for axis-angle rotations
        dim 0: rotation index, 1: [omega, theta, phi]

    Return values
    ------------
    Q : 2D ndarray, float
        stack of quaternions with 4 entries
        dim 0: rotation index, 1: [q0, q1, q2, q3]
    """
    Q = np.empty( (OTP.shape[0],4), data_type )
    for g in prange(OTP.shape[0]):
        ome, tta, phi = OTP[g,0], OTP[g,1], OTP[g,2]
        Q[g] = np.array([
                np.cos(ome/2),
                np.sin(ome/2) * np.sin(tta) * np.cos(phi),
                np.sin(ome/2) * np.sin(tta) * np.sin(phi),
                np.sin(ome/2) * np.cos(tta)
            ])
    return Q

@njit(parallel=True)
def OTPfromQ( Q ):
    """ Extracts the 3 angles omega, theta, phi from a quaterion

    Parameters
    ----------
    Q : 2D ndarray, float
        stack of quaternions with 4 entries
        dim 0: rotation index, 1: [q0, q1, q2, q3]

    Return values
    ------------
    OTP : 2D ndarray, float
        stack of angles for axis-angle rotations
        dim 0: rotation index, 1: [omega, theta, phi]
    """
    OTP = np.empty( (Q.shape[0],3), data_type )
    for g in prange(Q.shape[0]):
        r = np.sqrt( (Q[g,1:]**2).sum() )
        OTP[g] = np.array([
            2 * np.arctan2( r, Q[g,0] ),
            np.arctan2( np.sqrt( Q[g,1]**2 + Q[g,2]**2 ), Q[g,3] ),
            np.arctan2( Q[g,2], Q[g,1] ),
        ])
    OTP[ OTP[:,2]<0, 2 ] += 2*np.pi
    return OTP
        
@njit
def OTP_to_matrix( ome, tta, phi ):
    """ Creates rotation matrices from 3 angles omega, theta, phi

    Parameters
    ----------
    omega : ndarray, float
        rotation angle, usually ∈[0,pi)
    theta : ndarray, float
        polar angle of the rotation axis, usually ∈[0,pi)
    phi : ndarray, float
        azimutal angle of the rotation axis, usually ∈[0,2pi)

    Return values
    ------------
    R : ndarray, float
    """
    x = np.sin(tta) * np.cos(phi)
    y = np.sin(tta) * np.sin(phi)
    z =  np.cos(tta)
    so = np.sin(ome)
    co = np.cos(ome)
    R = np.array([
        [ co + x**2*(1-co), x*y*(1-co) - z*so, x*z*(1-co) + y*so ],
        [ y*x*(1-co) + z*so, co + y**2 *(1-co), y*z*(1-co) - x*so ],
        [ z*x*(1-co) - y*so, z*y*(1-co) + x*so, co + z**2 *(1-co) ]
    ])
    return R

@njit
def stack_mrot( vs, OTP ):
    """ Rotates a stack of vectors by a list of rotations

    Parameters
    ----------
    vs : 2D ndarray, float
        stack of vectors
        dim 0: vector index, 1: [x,y,z]
    OTP : 2D ndarray, float
        stack of angles for axis-angle rotations
        dim 0: rotation index, 1: [omega, theta, phi]

    Return values
    ------------
    R : ndarray, float
    """
    Nrot = OTP.shape[0]
    vs_rot = np.empty( ( Nrot, vs.shape[0], 3 ), data_type)
    for g in prange( Nrot ):
        R = OTP_to_matrix( OTP[g,0], OTP[g,1], OTP[g,2] ).T
        vs_rot[g] = vs @ R
    return vs_rot

@njit(parallel=True)
def ang_distance( q1, q2, gen ):
    """ Calculates the closest distance between 2 quaternions
    respecting a crystal symmetry represented by symmetry generators

    Q. Huynh, Metrics for 3d rotations: Comparison and analysis, 
    Journal of Mathematical Imaging and Vision, vol. 35, pp. 155-164, 2009.

    Parameters
    ----------
    q1, q2 : 2D ndarray, float
        stacks of quaternions
    gen : 2D ndarray, float
        2 symmetry generators in OTP representation
        [[ome1,tta1,phi1], [ome2,tta2,phi2]]

    Return values
    ------------
    DQ : ndarray, float
    """
    DQ = np.empty(q1.shape[0], data_type )
    # make quaternions from generators
    Q_gen = QfromOTP( gen )
    n1 = int(2*np.pi / gen[0,0]) # n1-fold symmetry from 1st generator
    n2 = int(2*np.pi / gen[1,0]) # n2-fold symmetry from 2nd generator
    for k in prange(q1.shape[0]):
        dq = np.pi
        qc = q2[k]
        for _ in range(n1):
            qc = q_mult( qc, Q_gen[0] ) # rotate point by 1st generator
            for _ in range(n2):
                qc = q_mult( qc, Q_gen[1] ) # rotate point by 2st generator
                # add to the odf according to the real quaternion distance
                r = 2*(qc*q1[k]).sum()**2 - 1
                if np.abs(r) > 1:
                    r /= np.abs(r) # this is for rounding errors
                dq = min(dq, np.arccos( r ))
        DQ[k] = dq
    return DQ

@njit(parallel=True)
def misorientation( q1, q2, gen ):
    """ Calculates the closest distance between 2 quaternions
    respecting a crystal symmetry represented by symmetry generators

    Q. Huynh, Metrics for 3d rotations: Comparison and analysis, 
    Journal of Mathematical Imaging and Vision, vol. 35, pp. 155-164, 2009.

    Parameters
    ----------
    q1, q2 : 2D ndarray, float
        stacks of quaternions
    gen : 2D ndarray, float
        2 symmetry generators in OTP representation
        [[ome1,tta1,phi1], [ome2,tta2,phi2]]

    Return values
    ------------
    DQ : ndarray, float
    """
    DQ = np.empty(q1.shape[0], data_type )
    # make quaternions from generators
    Q_gen = QfromOTP( gen )
    if gen[0,0] > 0:
        n1 = int(2*np.pi / gen[0,0]) # n1-fold symmetry from 1st generator
    else:
        n1=1
    if gen[1,0] > 0:
        n2 = int(2*np.pi / gen[1,0]) # n2-fold symmetry from 2nd generator
    else:
        n2=1
    for k in prange(q1.shape[0]):
        dq = np.pi
        qa = q1[k]
        qb = q2[k]
        for _ in range(n1):
            qa = q_mult( Q_gen[0], qa ) # rotate point by 1st generator
            for _ in range(n2):
                qa = q_mult( Q_gen[1], qa ) # rotate point by 2st generator
                for _ in range(n1):
                    qb = q_mult( qb, Q_gen[0] ) # rotate point by 1st generator
                    for _ in range(n2):
                        qb = q_mult( qb, Q_gen[1] ) # rotate point by 2st generator
                        # add to the odf according to the real quaternion distance
                        r = 2*(qa*qb).sum()**2 - 1
                        if np.abs(r) > 1:
                            r /= np.abs(r) # this is for rounding errors
                        dq = min(dq, np.arccos( r ))
        DQ[k] = dq
    return DQ

@njit()
def misorientation_single( qa, qb, gen ):
    """ Calculates the closest distance between 2 quaternions
    respecting a crystal symmetry represented by symmetry generators

    Q. Huynh, Metrics for 3d rotations: Comparison and analysis, 
    Journal of Mathematical Imaging and Vision, vol. 35, pp. 155-164, 2009.

    Parameters
    ----------
    q1, q2 : 1D ndarray, float
        quaternions to compare
    gen : 2D ndarray, float
        2 symmetry generators in OTP representation
        [[ome1,tta1,phi1], [ome2,tta2,phi2]]

    Return values
    ------------
    DQ : ndarray, float
    """
    # make quaternions from generators
    Q_gen = QfromOTP( gen )
    n1 = int(2*np.pi / gen[0,0]) # n1-fold symmetry from 1st generator
    n2 = int(2*np.pi / gen[1,0]) # n2-fold symmetry from 2nd generator
    dq = np.pi
    for _ in range(n1):
        qa = q_mult( Q_gen[0], qa ) # rotate point by 1st generator
        for _ in range(n2):
            qa = q_mult( Q_gen[1], qa ) # rotate point by 2st generator
            for _ in range(n1):
                qb = q_mult( qb, Q_gen[0] ) # rotate point by 1st generator
                for _ in range(n2):
                    qb = q_mult( qb, Q_gen[1] ) # rotate point by 2st generator
                    # add to the odf according to the real quaternion distance
                    r = 2*(qa*qb).sum()**2 - 1
                    if np.abs(r) > 1:
                        r /= np.abs(r) # this is for rounding errors
                    dq = min(dq, np.arccos( r ))
    return dq

@njit
def q_mult(q1, q2):
    """ Multiplies 2 quaternions according to their rules

    Parameters
    ----------
    q1, q2 : ndarray, float
        quaternions [q0, q1, q2, q3]

    Return values
    ------------
    multiplied quaternion [q0, q1, q2, q3]
    """
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
    z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
    return np.array([w, x, y, z])

def samplerotations_eq3D( d_rot, tilts ):
    """ Calculates rotation and tilt angles equally spaced over a sphere

    Parameters
    ----------
    d_rot : float
        distance between rotations at zero tilt in degree
    tilts : list of int
        list of tilt angles in degree

    returns: 
    ------------
    Omega, Kappa : ndarray, float
        rotation and tilt angles in degree
    """
    omega, kappa = np.array([]),np.array([])
    d_ome = d_rot
    for k, kap in enumerate( np.array(tilts) ):
        if kap == 0.0:
            ome_max = 180
        else:
            ome_max = 360
        n_ome = np.round(ome_max/d_ome * np.cos(kap*np.pi/180)).astype(int)
        if np.mod(k,2) != 0:
            ome_min = ome_max/n_ome/2
        else:
            ome_min = 0
        omega = np.concatenate(
            [omega, np.linspace(ome_min,ome_max,n_ome, endpoint=False)],
            axis=0 )
        kappa = np.concatenate([kappa, kap*np.ones(n_ome)], axis=0)

    return np.array(omega).flatten(), np.array(kappa).flatten()
