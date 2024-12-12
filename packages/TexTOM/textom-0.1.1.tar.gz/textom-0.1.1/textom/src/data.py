import os
# Housekeeping, set num threads to 1 before importing numpy
os.environ["MKL_NUM_THREADS"] = "1" 
os.environ["NUMEXPR_NUM_THREADS"] = "1" 
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np
from time import time
import sys
import h5py
from numba import prange, njit
from scipy.signal import find_peaks

# domestic
from . import mask as msk
from .misc import import_module_from_path
from .model import model
from ..config import data_type

def import_data( path, pattern, mod:model,  baselines=False,
                qmask_path=None, detmask_path=None, geo_path='input/geometry.py',
                flip_fov=False, use_ion=True ):

    geo = import_module_from_path('geometry', geo_path)
    # get the images that show the sample
    scanmask = mod.Beams[:,:,0].astype(bool)                           ###########

    print('Starting data import')
    print('\tLoading integrated data from files')
    t0=time()
    bl_coeff, airscat, ion = [], [], []
    filelist = sorted( os.listdir( os.path.join(path,'data_integrated')) )
    filelist = [s for s in filelist if pattern in s]#[:2]
    t1=time()
    for g, file in enumerate( filelist ):
        # Read data from integrated file
        with h5py.File(os.path.join(path, 'data_integrated', file),'r') as hf:
            q_in = ( hf['radial_units'][0] ).astype(data_type)
            chi_in = ( hf['azimuthal_units'][0]*np.pi/180 ).astype(data_type)
            fov = ( hf['fov'][()] ).astype(np.int32)
            d = np.array(hf['cake_integ'])[()]
            if 'ion' in hf and use_ion:
                ion.append(hf['ion'][()])

        ### Rebin in chi if necessary
        n_chi = chi_in.size
        if n_chi != mod.detShape[1]:
            n_chi = mod.detShape[1]
            d = rebin_stack_2d_cols(d, n_chi)

        if flip_fov:
            fov = np.flip( fov )
            
        if ion and use_ion:
            # print('\tRescale by beam intensity')
            d = _rescale( d, ion[g] )

        ## Reshaping in function of scanning mode ###
        # Base code written for column scan
        d = d.reshape( *fov, d.shape[1], d.shape[2] )
        
        if 'line' in geo.scan_mode:
            fov = np.flip( fov )
            # d = np.fliplr(np.flipud( np.transpose( d, axes=(1,0,2,3)) ) )
            d = np.transpose( d, axes=(1,0,2,3)) 

        # reorder data so that they are all treated the same in the model
        if 'snake' in geo.scan_mode:
            # Flip every second row
            for ii in range(d.shape[0]):
                if ii % 2 != 0:
                    d[ii] = d[ii][::-1]
        ##############################################

        # dat.append( d )
        i0=d.shape[-1]//4
        edge_sample = np.array([ d[0,0,:,i0:].mean(), d[0,-1,:,i0:].mean(), 
                    d[-1,0,:,i0:].mean(), d[-1,-1,:,i0:].mean()])
        airscat.append( np.min( edge_sample[edge_sample > 0.] ))
        if not ion or not use_ion:
            # print('\tRescale by air scattering')
            d /= airscat[g]

        # print('\tPadding data.')
        # t0=time()
        if hasattr( mod, 'fov_single' ):
            fov_max = mod.fov_single
        else:
            fov_max = mod.fov
        # pad the data as in mumottize
        proj =  np.zeros( (*fov_max, n_chi, *q_in.shape), data_type)
        si, sj = d.shape[:2]
        i0 = (fov_max[0] - si)//2
        j0 = (fov_max[1] - sj)//2
        proj[i0:i0+si, j0:j0+sj] = d
        proj = proj.reshape(fov_max[0]*fov_max[1], n_chi, *q_in.shape)
        # print(f'\t\ttook {time()-t0:.2f} s')

        if g==0:
            #### Select q-regions ####
            # prepare data for choosing q-regions
            q_mask = np.ones_like(q_in, dtype=bool)
            q_mask &= (q_in > mod.q[0]) # cut away SAXS signal
            dat_cmp = proj[scanmask[0]].mean(axis=0).mean(axis=0) # make a pseudo-powderpattern from data

            if isinstance( qmask_path, str ):
                # if peak regions are defined in file, take them
                peak_reg = np.genfromtxt(qmask_path)
                peak_reg = peak_reg.reshape( (peak_reg.size//2, 2)  )
                print('\tLoaded peak regions')
            else:
                # select peak regions from data and simulated powder pattern
                print('\tChoose regions containing diffraction peaks')
                happy = 'n'
                while happy != 'y':
                    powder = mod.difflets[0].reshape(mod.detShape)[:,0]
                    powder = powder / powder[-10:].mean() * dat_cmp[-10:].mean()

                    peak_reg = msk.select_regions( q_in[q_mask], dat_cmp[q_mask], mod.q, powder, 
                            max_regions=None,
                            title='Select individual Bragg peaks by holding LMB, remove by RMB' )
                    happy = input('\thappy? (y/n) ')
                peak_reg = peak_reg.get_regions()

                with open( os.path.join(path,'analysis','peak_regions.txt'),'w') as fid:
                    for reg in peak_reg:
                        fid.write(f'{reg[0]}\t{reg[1]}\n')
            
            # q_peaks = np.array([(end-start)/2 for start,end in peak_reg]) # why is this wrong??
            q_peaks = np.mean(peak_reg, axis=1)

            # find out prominence of the highest peak for filtering data
            I_mx = 0.                   
            q_mask_k = []
            for k, (start, end) in enumerate( peak_reg ):
                q_mask_k.append( ((q_in >= start) & (q_in <= end)) )
                q_mask &= ~q_mask_k[k]
                dat_peak = dat_cmp[q_mask_k[k]]
                if dat_peak.max() > I_mx:
                    q_mask_hp = q_mask_k[k]
                    _, info = find_peaks(dat_peak, prominence=0)
                    prom = info['prominences'].max()
                    I_mx = dat_peak.max()
            q_mask_k = np.array(q_mask_k)#.astype(data_type)   

            #### Make the Detector mask ####
            if isinstance( detmask_path, str ):
                mask_detector = np.genfromtxt(detmask_path, bool)
                print('\tLoaded detector mask')
            else:
                # create the detector mask
                sampleim = proj[scanmask[0]].sum(axis=0)
                sampleim = np.array([sampleim[:,qm].sum(axis=1) for qm in q_mask_k])
                # check if there is a mask from pyfai
                cakemask_path = os.path.join(path, 'analysis', 'mask_detector_cake.h5')
                if os.path.isfile(cakemask_path):
                    with h5py.File(cakemask_path,'r') as hf:
                        mc = hf['cake_mask'][()]
                    QQ,_ = np.meshgrid( q_in, chi_in )
                    qm = [np.logical_and(QQ >= start, QQ <= end) for start,end in peak_reg]
                    mask_detector = np.array([
                        [np.logical_and.reduce(mc[k, qm[l][k]]) for k in range(n_chi)] 
                            for l in range(len(peak_reg))])
                else:
                    mask_detector = np.ones_like(sampleim).astype(bool)

                # start = np.argmax(q_mask) # this could be useful if taking a full mask, then partially regroup ? have to do it with diffractlets too maybe
                # end = len(q_mask) - 1 - np.argmax(q_mask[::-1]) # then make these values None and when regrouping do np.mean * number of points to make up for Nones
                mask_detector = msk.mask_detector( sampleim, mask_detector )
                with open( os.path.join(path, 'analysis', 'fit_detmask.txt'),'w') as fid:
                    for pxl in mask_detector:
                        fid.write(f'{pxl}\n')
            
        # print('\tRemoving outliers')
        # t0=time()
        # projections_1=projections.copy()
        # for k in range(proj.shape[0]):
        scanmask_g = scanmask[g].copy()
        proj = _remove_crazypixels(proj, scanmask_g)
            # sys.stdout.write('\r\t\t %d / %d' % (k+1,proj.shape[0]))
            # sys.stdout.flush()
        # print(f'\t\ttook {time()-t0:.2f} s')

        if baselines:
            # print('\tDrawing baselines')
            # t0=time()
            bl_coeff_tmp1, scanmask_g = _draw_baselines( 
                proj, scanmask_g, q_in, q_mask, q_mask_hp, prom, 5 )
            bl_coeff_tmp2 = bl_coeff_tmp1[scanmask_g]
            # # get rid of outliers
            t_mask_0 = np.where(scanmask_g)
            blc_weight = (bl_coeff_tmp2**2).sum(axis=1) 
            bl_mask = blc_weight < 200*np.median(blc_weight)
            t_mask = t_mask_0[0][bl_mask]
            scanmask_g = np.zeros_like(scanmask_g)
            scanmask_g[t_mask] = True
            scanmask[g] = scanmask_g
            bl_coeff_tmp1 = bl_coeff_tmp1[scanmask_g]    
            t_mask = np.array( np.where(scanmask_g) ).T        
            # print(f'\t\ttook {time()-t0:.2f} s')
        else:
            t_mask = np.array( np.where(scanmask_g) ).T
            bl_coeff_tmp1 = np.zeros( (t_mask.shape[0], 5), data_type )

        # # plot data and baseline
        # plt.plot(_mean_ax0_nb( proj[t] ))
        # plt.plot(_polyval_nb(bl_coeff_tmp1[t], q_in))

        bl_coeff.append(bl_coeff_tmp1)

        # print('\tSubstracting background, regrouping data')
        # t0=time()
        q_mask_k_ext = np.array([_tile_1d_nb(qmk, n_chi) for qmk in q_mask_k]
                                ).astype(data_type)
        data_fit = _regroup_q( 
            proj, t_mask, mask_detector, 
            bl_coeff_tmp1, q_in, n_chi, q_mask_k_ext )
        # print(f'\t\ttook {time()-t0:.2f} s')

        # dplot=np.zeros_like(scanmask_g).astype(data_type)
        # dplot[scanmask_g] = data_fit.mean(axis=1)
        # plt.figure()
        # plt.imshow(dplot.reshape(fov_max))

        out_path = os.path.join( path, 'analysis', 'data_textom.h5')
        if g == 0:
            print('\tSaving data to file: %s' % out_path)
            with h5py.File( out_path, 'w') as hf:
                hf.create_dataset( 'data',
                        shape=(0, data_fit.shape[1]),
                        maxshape=(None, data_fit.shape[1]),
                        chunks=(1, data_fit.shape[1]),
                        dtype='float64'
                    )
                hf.create_dataset( 'peak_reg', data=peak_reg )
                hf.create_dataset( 'q', data = q_peaks)
                hf.create_dataset( 'detShape', data = [q_mask_k.shape[0], n_chi] )
                hf.create_dataset( 'mask_detector', data = mask_detector)

        # add data to h5 file
        with h5py.File( out_path, 'r+') as hf:
            dset = hf['data']
            current_rows = dset.shape[0]
            new_rows = current_rows + data_fit.shape[0]
            dset.resize( new_rows, axis=0)
            dset[current_rows:new_rows, :] = data_fit


        t_it = (time()-t1)/(g+1)
        Nrot = len(filelist)
        sys.stdout.write(f'\r\t\tProjection {(g+1):d} / {Nrot:d}, t/proj: {t_it:.1f} s, t left: {((Nrot-g-1)*t_it/60):.1f} min' )
        sys.stdout.flush()

    ion_av = np.array( [i.mean() for i in ion] ) # cannon write ion directly because shape
    gt_mask = np.array( np.where(scanmask) ).T
    # add metadata to h5 file
    with h5py.File( out_path, 'r+') as hf:
        hf.create_dataset( 'scanmask', data=scanmask )
        hf.create_dataset( 'gt_mask', data=gt_mask )
        hf.create_dataset( 'bl_coeff', data=np.concatenate(bl_coeff) )
        hf.create_dataset( 'airscat', data = airscat )
        hf.create_dataset( 'ion', data = ion_av )

    print(f'\t\ttook {time()-t0:.2f} s')

@njit(parallel=True)
def _regroup_chi( d, n_old, n_new ):
    # Create an array to hold the rebinned result
    d_rebinned = np.empty((d.shape[0], n_new, d.shape[2]))

    # Create the old and new column indices
    old_indices = np.arange(n_old)
    new_indices = np.linspace(0, n_old - 1, n_new)

    for t in prange( d.shape[0] ):
        # Interpolate each row
        for ii in range( d.shape[2] ):
            d_rebinned[t, :, ii] = np.interp(new_indices, old_indices, d[t, :, ii])
    return d_rebinned

@njit(parallel=True)
def _draw_baselines_all(projections, scanmask, q, qmask, q_mask_hp, prom, porder=5 ):
    # draw baselines for chosen data
    bl_coeff = np.zeros( (projections.shape[0],projections.shape[1],porder+1), data_type )
    for g in range(projections.shape[0]):
        for t in prange(projections.shape[1]):
            if scanmask[g,t]:
                # regroup data azimutally
                data_1D = _mean_ax0_nb( projections[g,t] )

                if _any_peak( data_1D[q_mask_hp], 0.05*prom ):
                    # draw a baseline
                    c = _polyfit_nb( q[qmask], data_1D[qmask], porder )
                    b = _polyval_nb( c, q[qmask] )
                    bl_coeff[g,t] = c * (data_1D[qmask]/b).min()
                else:
                    # exclude this image
                    scanmask[g,t]=False
    return bl_coeff, scanmask, projections

@njit(parallel=True)
def _draw_baselines(proj, scanmask, q, qmask, q_mask_hp, prom, porder=5 ):
    # draw baselines for chosen data
    bl_coeff = np.zeros( (proj.shape[0],porder+1), data_type )
    for t in prange(proj.shape[0]):
        if scanmask[t]:
            # regroup data azimutally
            data_1D = _mean_ax0_nb( proj[t] )

            if _any_peak( data_1D[q_mask_hp], 0.05*prom ):
                # draw a baseline
                c = _polyfit_nb( q[qmask], data_1D[qmask], porder )
                b = _polyval_nb( c, q[qmask] )
                bl_coeff[t] = c * (data_1D[qmask]/b).min()
            else:
                # exclude this image
                scanmask[t]=False
    return bl_coeff, scanmask

@njit
def _any_peak( curve, prominence_threshold ):
    # numba-optimized function to check if there is a peak
    # with the given prominence in the data
    i_peak = np.argmax( curve )
    left_min = np.min(curve[:i_peak]) if i_peak > 0 else 0
    right_min = np.min(curve[i_peak + 1:]) if i_peak < curve.size-1 else 0
    prominence = curve[i_peak] - max(left_min, right_min)
    if prominence >= prominence_threshold:
        return True
    return False

@njit
def _mean_ax0_nb(a):
    # numba-optimized function to calculate mean values along the first dimension
    res = np.empty( a.shape[1], data_type)
    for i in range(a.shape[1]):
        res[i] = a[:,i].mean()
    return res

@njit
def _polyfit_nb(x, y, degree):
    """
    Fit a polynomial of a specified degree to the given data using least squares approximation.
    Numba compatible version of the numpy function
    
    Parameters:
    x (array-like): The x-coordinates of the data points.
    y (array-like): The y-coordinates of the data points.
    degree (int): The degree of the polynomial to fit.

    Returns:
    array: Coefficients of the polynomial, highest power first.
    """
    n = len(x)
    m = degree + 1
    A = np.empty((n, m), data_type)
    for i in range(n):
        for j in range(m):
            A[i, j] = x[i] ** (degree - j)
    return np.linalg.lstsq(A, y )[0]

@njit
def _polyval_nb(coeff, x):
    """
    Evaluate a polynomial given the coefficients at the points x.
    Uses Horner's Method.
    Numba compatible version of the numpy function

    Parameters:
    coeff (array-like): The coefficients of the polynomial.
    x (array-like): The x-coordinates of the data points.
    """
    res = np.zeros_like(x)
    for c in coeff:
        res = x * res + c
    return res

@njit(parallel=True)
def _regroup_q( proj, t_mask, mask_detector, bl_coeff, q_in, n_chi, q_mask_k_ext ):
    nD = t_mask.shape[0] # effective number of images
    data_fit = np.empty( (nD, mask_detector.sum()), data_type )
    n_peaks = q_mask_k_ext.shape[0]
    for k in prange(nD):
        # get image and subtract baseline
        d_k = proj[t_mask[k,0]] 
        bl = _polyval_nb( bl_coeff[k], q_in)
        d_k_sub = d_k - _tile_1d_nb(bl, n_chi)

        # regroup data into peaks
        d_k_regr = np.empty( (n_peaks, n_chi), data_type )
        for p in range(n_peaks):
            d_k_regr[p] = (d_k_sub*q_mask_k_ext[p]).sum(axis=1)
        d_k_regr_fl = d_k_regr.flatten()[mask_detector]

        data_fit[k] = d_k_regr_fl
    return data_fit

@njit
def _tile_1d_nb(a, n):
    # numba-optimized function to c
    # Create an output array of the desired shape
    out = np.empty((n, len(a)), data_type)
    
    # Fill the output array with repeated values from a
    for i in range(n):
        out[i] = a
    
    return out

@njit(parallel=True)
def _rescale( data, norm ):
    for k in prange( data.shape[0] ):
        if norm[k] == 0:
            data[k] = 0
        else:
            data[k] /= norm[k]
    return data

@njit(parallel=True)
def _rescale_perimage( data, norm ):
    for k in prange( data.shape[0] ):
        for l in range( data.shape[1] ):
            data[k,l] /= norm[k,l]
    return data

@njit(parallel=True)
def _remove_crazypixels( projection, scanmask ):
    dat_new = projection.copy()
    for k in prange(projection.shape[0]):
        if scanmask[k]:
            for l in range(1,projection.shape[2]-1):
                # base = np.median(projection[k,:,l])
                for m in range(-1,projection.shape[1]-1):
                    sample = np.array([
                        projection[k,m-1,l-1],projection[k,m-1,l],projection[k,m-1,l+1],
                        projection[k,m,l-1],projection[k,m,l+1],                        
                        projection[k,m,l-2],projection[k,m,l+2],
                        projection[k,m+1,l-1],projection[k,m+1,l],projection[k,m+1,l+1]
                    ])
                    base = np.median(sample)
                    if projection[k,m,l] > 10*np.abs(base):
                        dat_new[k,m,l] = base
    return dat_new

@njit(parallel=True)
def rebin_stack_2d_cols(stack, new_cols):
    """
    Rebin a stack of 2D arrays to a new shape using a weighted average of the corresponding regions.
    
    Parameters:
    - stack: 3D array with the arrays of original shape in dimensions 1/2.
    - new_cols: int of the new number of cols.
    
    Returns:
    - stack_rebinned: 3D array with the rebinned arrays in dimensions 1/2.
    """
    n_images = stack.shape[0]
    stack_reshaped = np.empty( (n_images, new_cols[0], stack.shape[2]) )
    for k in prange( n_images ):
        stack_reshaped[k] = rebin_2d_cols_weighted( stack[k], new_cols )
    return stack_reshaped

@njit
def rebin_2d_cols_weighted(array, new_shape):
    """
    Rebin a 2D array to a new shape using a weighted average of the corresponding regions.
    
    Parameters:
    - array: Input 2D array (original shape).
    - new_cols: int of the new number of cols.
    
    Returns:
    - rebinned_array: Rebinned 2D array with weighted averages.
    """
    original_shape = array.shape
    orig_rows, orig_cols = original_shape
    new_rows, new_cols = new_shape
    
    # Calculate the scaling factors (step size in each dimension)
    col_scale = orig_cols / new_cols

    # Create an empty rebinned array
    rebinned_array = np.zeros((new_rows, new_cols))

    for i in range(orig_rows):
        for j in range(new_cols):
            # Determine the range of pixels in the original array that contribute to the new bin
            col_start = j * col_scale
            col_end = (j + 1) * col_scale

            # Find the indices of the original array that overlap with the new bin
            col_indices = np.arange(int(np.floor(col_start)), int(np.ceil(col_end)))

            # Accumulate weighted sum over these indices
            weight_sum = 0
            value_sum = 0
            for c in col_indices:
                # Compute the overlap (weight) for each pixel
                weight = min(col_end, c + 1) - max(col_start, c)

                # Add the contribution to the weighted sum
                value_sum += array[i, c] * weight
                weight_sum += weight

            # Assign the weighted average to the rebinned array
            rebinned_array[i, j] = value_sum / weight_sum

    return rebinned_array

@njit(parallel=True)
def rebin_stack_2d(stack, new_shape):
    """
    Rebin a stack of 2D arrays to a new shape using a weighted average of the corresponding regions.
    
    Parameters:
    - stack: 3D array with the arrays of original shape in dimensions 1/2.
    - new_shape: Tuple of the new shape (new_rows, new_cols).
    
    Returns:
    - stack_rebinned: 3D array with the rebinned arrays in dimensions 1/2.
    """
    n_images = stack.shape[0]
    stack_reshaped = np.empty( (n_images, new_shape[0], new_shape[1]) )
    for k in prange( n_images ):
        stack_reshaped[k] = rebin_2d_weighted( stack[k], new_shape )
    return stack_reshaped

@njit
def rebin_2d_weighted(array, new_shape):
    """
    Rebin a 2D array to a new shape using a weighted average of the corresponding regions.
    
    Parameters:
    - array: Input 2D array (original shape).
    - new_shape: Tuple of the new shape (new_rows, new_cols).
    
    Returns:
    - rebinned_array: Rebinned 2D array with weighted averages.
    """
    original_shape = array.shape
    orig_rows, orig_cols = original_shape
    new_rows, new_cols = new_shape
    
    # Calculate the scaling factors (step size in each dimension)
    row_scale = orig_rows / new_rows
    col_scale = orig_cols / new_cols

    # Create an empty rebinned array
    rebinned_array = np.zeros((new_rows, new_cols))

    for i in range(new_rows):
        for j in range(new_cols):
            # Determine the range of pixels in the original array that contribute to the new bin
            row_start = i * row_scale
            row_end = (i + 1) * row_scale
            col_start = j * col_scale
            col_end = (j + 1) * col_scale

            # Find the indices of the original array that overlap with the new bin
            row_indices = np.arange(int(np.floor(row_start)), int(np.ceil(row_end)))
            col_indices = np.arange(int(np.floor(col_start)), int(np.ceil(col_end)))

            # Accumulate weighted sum over these indices
            weight_sum = 0
            value_sum = 0
            for r in row_indices:
                for c in col_indices:
                    # Compute the overlap (weight) for each pixel
                    row_overlap = min(row_end, r + 1) - max(row_start, r)
                    col_overlap = min(col_end, c + 1) - max(col_start, c)
                    weight = row_overlap * col_overlap

                    # Add the contribution to the weighted sum
                    value_sum += array[r, c] * weight
                    weight_sum += weight

            # Assign the weighted average to the rebinned array
            rebinned_array[i, j] = value_sum / weight_sum

    return rebinned_array

def import_data_1d( path, pattern, mod:model,
                geo_path='input/geometry.py',
                flip_fov=False, use_ion=True ):

    geo = import_module_from_path('geometry', geo_path)
    # get the images that show the sample
    scanmask = mod.Beams[:,:,0].astype(bool)                           ###########

    print('Starting data import')
    print('\tLoading integrated data from files')
    t0=time()
    airscat, ion = [], []
    filelist = sorted( os.listdir( os.path.join(path,'data_integrated_1d')) )
    filelist = [s for s in filelist if pattern in s]#[:2]
    t1=time()
    for g, file in enumerate( filelist ):
        # Read data from integrated file
        with h5py.File(os.path.join(path, 'data_integrated_1d', file),'r') as hf:
            q_in = ( hf['radial_units'][0] ).astype(data_type)
            fov = ( hf['fov'][()] ).astype(np.int32)
            d = np.array(hf['cake_integ'])[()]
            if 'ion' in hf:
                ion.append(hf['ion'][()])

        if flip_fov:
            fov = np.flip( fov )
            
        if ion and use_ion:
            # print('\tRescale by beam intensity')
            d = _rescale( d, ion[g] )

        ## Reshaping in function of scanning mode ###
        # Base code written for column scan
        d = d.reshape( *fov, d.shape[1] )
        
        if 'line' in geo.scan_mode:
            fov = np.flip( fov )
            d = np.transpose( d, axes=(1,0,2)) 

        # reorder data so that they are all treated the same in the model
        if 'snake' in geo.scan_mode:
            # Flip every second row
            for ii in range(d.shape[0]):
                if ii % 2 != 0:
                    d[ii] = d[ii][::-1]
        ##############################################

        # i0=d.shape[-1]//4
        # airscat.append(
        #         min( d[0,0,:,i0:].mean(), d[0,-1,:,i0:].mean(), 
        #             d[-1,0,:,i0:].mean(), d[-1,-1,:,i0:].mean() ))
        # get airscattering:
        airscat.append(
            min( d[0,0].mean(), d[0,-1].mean(), d[-1,0].mean(), d[-1,-1].mean() )
        )
        if not ion or not use_ion:
            # print('\tRescale by air scattering')
            d /= airscat[g]

        max_shape = mod.fov
        # pad the data as in mumottize
        # fill projections with air scattering
        proj =  np.random.normal(airscat[g],np.sqrt(airscat[g])/2,(*max_shape, d.shape[2]))
        si, sj = d.shape[:2]
        i0 = (max_shape[0] - si)//2
        j0 = (max_shape[1] - sj)//2
        proj[i0:i0+si, j0:j0+sj] = d
        proj = proj.reshape(max_shape[0]*max_shape[1], *q_in.shape)

        scanmask_g = scanmask[g].copy()
        proj = _remove_crazypixels_1d(proj, scanmask_g)

        out_path = os.path.join( path, 'analysis', 'data_1drec.h5')
        if g == 0:
            print('\tSaving data to file: %s' % out_path)
            with h5py.File( out_path, 'w') as hf:
                hf.create_dataset( 'data',
                        shape=(0, proj.shape[1]),
                        maxshape=(None, proj.shape[1]),
                        chunks=(1, proj.shape[1]),
                        dtype='float64'
                    )
                hf.create_dataset( 'radial_units', data = q_in )

        # add data to h5 file
        with h5py.File( out_path, 'r+') as hf:
            dset = hf['data']
            current_rows = dset.shape[0]
            new_rows = current_rows + proj.shape[0]
            dset.resize( new_rows, axis=0)
            dset[current_rows:new_rows, :] = proj


        t_it = (time()-t1)/(g+1)
        Nrot = len(filelist)
        sys.stdout.write(f'\r\t\tProjection {(g+1):d} / {Nrot:d}, t/it: {t_it:.1f} s, t left: {((Nrot-g-1)*t_it/60):.1f} min' )
        sys.stdout.flush()

    ion_av = np.array( [i.mean() for i in ion] ) # cannon write ion directly because shape
    gt_mask = np.array( np.where(scanmask) ).T
    # add metadata to h5 file
    with h5py.File( out_path, 'r+') as hf:
        hf.create_dataset( 'scanmask', data=scanmask )
        hf.create_dataset( 'gt_mask', data=gt_mask )
        hf.create_dataset( 'airscat', data = airscat )
        hf.create_dataset( 'ion', data = ion_av )
        hf.create_dataset( 'q', data=q_in)

    print(f'\t\ttook {time()-t0:.2f} s')

@njit(parallel=True)
def _remove_crazypixels_1d( projection, scanmask ):
    dat_new = projection.copy()
    for k in prange(projection.shape[0]):
        if scanmask[k]:
            for m in range(-1,projection.shape[1]-1):
                sample = np.array([
                    projection[k,m-2],projection[k,m-1],projection[k,m+1],projection[k,m+2]
                ])
                base = np.median(sample)
                if projection[k,m] > 10*np.abs(base):
                    dat_new[k,m] = base
    return dat_new