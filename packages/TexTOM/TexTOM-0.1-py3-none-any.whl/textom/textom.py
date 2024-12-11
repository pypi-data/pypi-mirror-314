import os, glob, sys, shutil
# Housekeeping, set num threads to 1 before importing numpy
os.environ["MKL_NUM_THREADS"] = "1" 
os.environ["NUMEXPR_NUM_THREADS"] = "1" 
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np
import h5py, hdf5plugin
import matplotlib.pyplot as plt
plt.ion()
from importlib import reload # this is to reload
import imageio.v3 as iio
from time import time

from .src.model import model
from .src import data
from .src import mumott_plugins as mum
from .src.fitting import fitting
from .src import handle as hdl
from .src import plotting as plot
from .src import optimizer 
from .src import symmetries as sym
from .src import mask as msk
from .src import misc as msc
from .src import orix_plugins as orx
from .src import exceptions as exc
from .src import rotation as rot
from .src import segmentation as seg
from .config import use_gpu

sample_dir = ''
mod, fit, opt  = None, None, None
results = {}

msc.fancy_title()
sample_dir = input('Set sample base directory: ')

def main():
    import IPython
    import textom
    # Create a dictionary of all public functions and classes from textom
    textom_namespace = {k: v for k, v in vars(textom).items() if not k.startswith("_")}
    # Start IPython with the namespace
    IPython.start_ipython(argv=[], user_ns=textom_namespace)

def set_path( path ):
    """Set the path where integrated data and analysis is stored

    Parameters
    ----------
    path : str
        full path to the directory, must contain a folder '/data_integrated'
    """    
    global sample_dir
    sample_dir = path
    print(f'Set sample path to: {sample_dir}')

def check_state( ):
    """Prints in terminal which parts of the reconstruction are ready
    """    
    sample_dir = _sdir( )
    print('Checking state of analysis')
    to_check = [
        ['Alignment', os.path.join(sample_dir,'analysis','alignment_result.h5')],
        ['Model (crystal)', os.path.join(sample_dir,'analysis','crystal.h5')],
        ['Model (beam intensities)', os.path.join(sample_dir,'analysis','tomo.h5')],
        ['Data', os.path.join(sample_dir,'analysis','data_textom.h5')],
    ]

    for ch in to_check:
        state = 'ready' if os.path.isfile(ch[1]) else 'missing'
        print(f'\t{ch[0]} - {state}')

def integrate():
    """Function for integrating raw data (to do)
    """
    print('')

def align_data( 
        pattern='.h5', sub_data='data_integrated', 
        q_index_range=(0,5), q_range = False,
        crop_image=False, mode='optical_flow',
        redo_import=False, flip_fov=False, regroup_max=16,
        align_horizontal=True, align_vertical=True,
        pre_rec_it = 5, pre_max_it = 5,
        last_rec_it = 40, last_max_it = 5,
          ):
    """Align data using the Mumott optical flow alignment

    Requires that data has been integrated and that sample_dir contains
    a subfolder with data

    Parameters
    ----------
    pattern : str, optional
        substring contained in all files you want to use, by default '.h5'
    sub_data : str, optional
        subfolder containing the data, by default 'data_integrated'
    q_index_range : tuple, optional
        determines which q-values are used for alignment (sums over them), by default (0,5)
    q_range : tuple, optional
        give the q-range in nm instead of indices e.g. (15.8,18.1), by default False
    crop_image : bool or tuple of int, optional
        give the range you want to use in x and y, e.g. ((0,-1),(10,-10)), by default False
    mode : str, optional
        choose alignment mode, 'optical_flow' or 'phase_matching', by default 'optical_flow'
    redo_import : bool, optional
        set True if you want to recalculate data_mumott.h5, by default False
    flip_fov : bool, optional
        only to be used if the fov is in the wrong order in the integrated
        data files, by default False
    regroup_max : int, optional
        maximum size of groups when downsampling for faster processing, by default 16
    align_horizontal : bool, optional
        align your data horizontally, by default True
    align_vertical : bool, optional
        align your data vertically, by default True
    pre_rec_it : int, optional
        reconstruciton iterations for downsampled data, by default 5
    pre_max_it : int, optional
        alignment iterations for downsampled data, by default 5
    last_rec_it : int, optional
        reconstruciton iterations for full data, by default 40
    last_max_it : int, optional
        alignment iterations for full data, by default 5
    """    
    ### replace saxs_end_idx with q-range
    sample_dir = _sdir( )
    # get geometry file from input/ if not present in sample_dir
    geo_path = os.path.join(sample_dir,'analysis/geometry.py')
    if ~os.path.isfile( geo_path ):
        os.makedirs(os.path.join(sample_dir,'analysis'), exist_ok=True )
        shutil.copyfile('input/geometry.py', geo_path )
        # msc.cp_addno('input/geometry.py', os.path.join(sample_dir,'analysis'))
    # do data preprocessing if not yet done
    if ( os.path.isfile(os.path.join(sample_dir,'analysis/data_mumott.h5')) and
        not redo_import ):
        mm_file = os.path.join(sample_dir,'analysis','data_mumott.h5')
    else:
        mm_file = mum.mumottize(sample_dir, 
            sub_data=sub_data, pattern=pattern, 
            q_index_range=q_index_range, q_range=q_range,
            geo_path=geo_path,
            flip_fov=flip_fov, check_ori=True,
            )
    # downsample data
    mum.regroup(mm_file, regroup_max=regroup_max,
                horizontal=align_horizontal, vertical=align_vertical,
                )
    if crop_image:
        # crop_image = ()
        with h5py.File(mm_file, 'r') as hf:
            im_test = hf['projections']['0']['diode'][()]
        plt.figure()
        plt.imshow(im_test[slice(*crop_image[0]), slice(*crop_image[1])])
        plt.show(block=True)
        # happy = input('happy? (y/n)')
        # if 'n' in happy:
        #     break
        if mode=='optical_flow':
            print('\tcropping not possible for optical flow alignment, switching to phase-matching')
            mode='phase_matching'
    # run the alignment
    mum.align_regrouped(os.path.join(sample_dir,'analysis'), use_gpu=use_gpu,
                            regroup_max=regroup_max, 
                            crop_image=crop_image, mode=mode,
                            pre_rec_it = pre_rec_it, pre_max_it = pre_max_it,
                            last_rec_it = last_rec_it, last_max_it = last_max_it,
                            align_horizontal=align_horizontal, align_vertical=align_vertical,
                            )
    # plot a rough consistency check
    mum.check_consistency( 
        os.path.join(sample_dir,'analysis','alignment_result.h5'), 
        os.path.join(sample_dir,'analysis','data_mumott.h5'),
        save_to_result=True  )
    
def check_alignment_consistency( ):
    """Plots the squared residuals between data and the projected tomograms

    """    
    sample_dir = _sdir( )
    mum.check_consistency( 
        os.path.join(sample_dir,'analysis','alignment_result.h5'), 
        os.path.join(sample_dir,'analysis','data_mumott.h5'),  )

def check_alignment_projection( g=0 ):
    """Plots the data and the projected tomogram of projection g

    Parameters
    ----------
    g : int, optional
        projection running index, by default 0
    """     
    sample_dir = _sdir( )
    mum.show_aligned_projection( g,
        os.path.join(sample_dir,'analysis','alignment_result.h5'), 
        os.path.join(sample_dir,'analysis','data_mumott.h5'),  )
    # check all as a movie

def make_model( ):
    """Calculates the TexTOM model for reconstructions

    Is automatically performed by the functions that require it
    """    
    sample_dir = _sdir( )
    global mod
    mod = model( sample_dir )

def preprocess_data( pattern='.h5', flip_fov=False, baselines=True, use_ion=True ):
    """Loads integrated data and pre-processes them for TexTOM

    Parameters
    ----------
    pattern : str, optional
        substring contained in all files you want to use, by default '.h5'
    flip_fov : bool, optional
        only to be used if the fov is in the wrong order in the integrated
        data files, by default False
    baselines : bool, optional
        choose if you want to draw polynomial baselines, by default True
    use_ion : bool, optional
        choose if you want to normalize data by the field 'ion' in the 
        data files, by default True
    """    
    sample_dir = _sdir( )
    global mod
    if mod is None:
        make_model()

    qmask = os.path.join(sample_dir,'analysis','peak_regions.txt')
    if not os.path.isfile(qmask):
        qmask = None
    detmask = os.path.join(sample_dir,'analysis','fit_detmask.txt')
    if not os.path.isfile(detmask):
        detmask = None

    data.import_data( sample_dir, 
                     pattern ,mod, 
                     baselines=baselines,
                     qmask_path=qmask,
                     detmask_path=detmask,
                     geo_path=os.path.join(sample_dir,'analysis/geometry.py'),
                     flip_fov=flip_fov,
                     use_ion=use_ion,
                     )

    print('')

def make_fit( redo=True ):
    """Initializes a TexTOM fit object for reconstructions

    Is automatically performed by the functions that require it

    Parameters
    ----------
    redo : bool, optional
        set True for recalculating, by default True
    """    
    sample_dir = _sdir( )
    global mod, fit
    if mod is None:
        make_model()
    if (fit is None or redo):
        fit = fitting( sample_dir, mod )

def optimize( order=0, mode=0,
             proj='full',
             redo_fit=False,
             tol=1e-3, minstep=1e-9, itermax=3000,
             alg='quadratic', save_h5=True,
              ):
    """Performs a single TexTOM parameter optimization

    Parameters
    ----------
    order : int, optional
        maximum sHSH order to be used, by default 0
    mode : int, optional
        set 0 for only optimizing order 0, 1 for highest order, 2 for all,
        by default 0
    proj : str, optional
        choose projections to be optimized: 'full', 'half', 'third', 'notilt', 
        by default 'full'
    redo_fit : bool, optional
        recalculate the fit object, by default False
    tol : float, optional
        tolerance for precision break criterion, by default 1e-3
    minstep : float, optional
        minimum stepsize in line search, by default 1e-9
    itermax : int, optional
        maximum number of iterations, by default 3000
    alg : str, optional
        choose algorithm between 'backtracking', 'simple', 'quadratic', 
        by default 'quadratic'
    save_h5 : bool, optional
        choose if you want to save the result to the directory analysis/fits, 
        by default True    
    """    
    sample_dir = _sdir( )
    global mod, fit, opt, results
    make_fit( redo=redo_fit )
    
    fit.choose_projections( proj ) 
    fit.set_orders( mod, order )
    if mode==0:
        fit.prepare_fit_c0()
    proj_c0 = False if mode==1 else True
    fit.C, opt = optimizer.optimize( fit, mode,
                alg=alg, tol=tol, minstep=minstep, itermax=itermax, project_c0=proj_c0 )
    results['optimization'] = opt['resname']
    if save_h5:
        os.makedirs(os.path.join(sample_dir,'analysis','fits'), exist_ok=True)
        hdl.save_dict_to_h5( opt, os.path.join(sample_dir,'analysis','fits',opt['resname']))

def optimize_auto( max_order=8,
                    start_order=None,
                    redo_fit=False,
                    proj='full',
                    alg='quadratic',
                    adj_scal = False,
              ):
    """Automated TexTOM reconstruction workflow

    Parameters
    ----------
    max_order : int, optional
        maximum HSH order to be used, by default 8    
    start_order : int or None, optional
        lowest order to be fitted, if None continues where you are standing, 
        by default None
    redo_fit : bool, optional
        recalculate the fit object, by default False
    proj : str, optional
        choose projections to be optimized: 'full', 'half', 'third', 'notilt', by default 'full'
    alg : str, optional
        choose algorithm between 'backtracking', 'simple', 'quadratic', 
        by default 'quadratic'
    """    
    sample_dir = _sdir( )
    global mod, fit, opt, results
    make_fit( redo=redo_fit )
    
    t0=time()
    os.makedirs(os.path.join(sample_dir,'analysis','fits'), exist_ok=True)
    fit.choose_projections( proj ) 

    orders = mod.get_orders(n_max=max_order,info=False)
    if not isinstance(start_order, int):
        start_order = min(orders[orders>max(fit.ns)])
    orders = orders[orders>=start_order]

    if start_order==0:
        print( 'Optimizing 0 order intensities')
        fit.prepare_fit_c0()
        # opimize c0 from average intensity
        fit.C, opt0 = optimizer.optimize( fit, 0, tol=1e-7, minstep=1e-5, alg=alg ) 
        if adj_scal:
            adjust_data_scaling()
            fit.C, opt0 = optimizer.optimize( fit, 0, tol=1e-7, minstep=1e-5, alg=alg ) 

    print( 'Optimizing anisotropy')
    for n in orders[orders>0]:
        fit.set_orders( mod, n )
        # optimize only highest
        fit.C, opt = optimizer.optimize( fit, 1, minstep=1e-5, alg=alg, project_c0=False ) 
        # hdl.save_dict_to_h5( opt, os.path.join(sample_dir,'analysis','fits',opt['resname']))

        if n%4 == 0:
            print( 'Refining all orders')
            # optimize all orders
            fit.C, opt = optimizer.optimize( fit, 2, tol=1.-4, minstep=1e-5, alg=alg ) 

        hdl.save_dict_to_h5( opt, os.path.join(sample_dir,'analysis','fits',opt['resname']))
    print(f'Total optimization time: {(time()-t0)/60} min')
    results['optimization'] = opt['resname']
    check_projections_average()
    check_projections_orientations()

def adjust_data_scaling( ):
    global fit
    print('\tAdjusting data scaling')
    fit.prepare_fit_c0()
    scal = fit.insert_fov( fit.projections_c0( fit.C ) 
                ).sum(axis=1) / fit.insert_fov( fit.data_av ).sum(axis=1)
    scal_fl = np.tile(scal,(fit.Beams.shape[1],1)).T[fit.scanmask]
    fit.data = np.array( [s*d for s,d in zip(scal_fl,fit.data)])

def list_opt():
    """Shows all stored optimizations
    """
    sample_dir = _sdir( )
    opt_dir = os.path.join(sample_dir, 'analysis','fits')
    optimizations = msc.list_files_by_modification_time(opt_dir,reverse=True,extension='.h5')
    for o in optimizations:
        print(f'\r{o}')

def load_opt( h5path = 'last' ): 
    """Loads a previous Textom optimization into memory

    Parameters
    ----------
    h5path : str, optional
        filepath, just filename or full path
        if 'last', uses the youngest file is used in analysis/fits/, 
        by default 'last'
    """    
    sample_dir = _sdir( )
    
    if h5path == 'last':
        h5path = msc.lastfile( os.path.join(sample_dir,'analysis','fits'), '*.h5' )
    elif os.path.dirname(h5path) == '': # if only filename
        h5path = os.path.join(sample_dir,'analysis','fits',h5path)
    print(f'Loading {os.path.basename(h5path)}')
    global fit,mod,opt, results
    make_fit( )
    i0 = h5path.find('nmax')
    i1 = h5path.find('_', i0)
    nmax = int( h5path[i0+4 : i1] )
    fit.set_orders(mod,nmax)
    opt = hdl.load_h5_to_dict( h5path )
    fit.C = opt['c']
    results['optimization'] = opt['resname']
    print('Loaded opt object and hsh coefficients to fit.C')

def check_fit_average( ):
    """Plots the reconstructed average intensity for each projection with data

    Parameters
    ----------
    """    
    plt.figure()
    plt.plot(fit.data_av, label='data')
    plt.plot(fit.projections_c0(fit.C),label='fit')
    plt.legend()

def check_fit_random( N=10, mode='line' ):
    """Generates TexTOM reconstructions and plots them with data for random points

    Parameters
    ----------
    N : int, optional
        Number of images created, by default 10    
    mode : str, optional
        plotting mode, 'line' or 'color', by default line
    """    
  
    for _ in range(N):
        idx = np.random.randint(fit.gt_mask.shape[0])
        plot.singlefit2D(fit, idx,
            polar=False, mode=mode,
            log=False, show_off=True,
            show=False)
    # plt.show()

def check_residuals( ):
    """Plots the squared residuals summed over each projection
    """    
    global mod, fit
    if fit is None:
        print('\tNo fit available, load or obtain result first')
        return
    # fit.choose_projections('full') ## doesn't work with less projections yet (else modify fit.data_av)
    # if np.all(fit.ns == np.array([0])):
    #     if not hasattr( fit, 'data_av' ):
    #         fit.prepare_fit_c0()
    #     proj = fit.projections_c0( fit.C )
    #     res = fit.insert_fov( (proj-fit.data_av)**2 ).sum(axis=1)
    # else:
    #     #calculate full projections and get residuals for all data per proj
    #     print('todo')
    plot.projection_residuals( fit )

def check_projections_average( G=None ):
    """Plots the reconstructed average intensity for chosen projections with data
    
    Parameters
    ----------
    G : int or ndarray or None, optional
        projection indices, if None takes 10 equidistant ones, by default None
    """    
    global mod, fit
    if fit is None:
        print('\tNo fit available, load or obtain result first')
        return
    if G is None: # plot 10 projections over all angles
        G = np.linspace(0, fit.scanmask.shape[0]-1,num=10,dtype=int)
    
    if not hasattr( fit, 'data_av' ):
        fit.prepare_fit_c0()
    proj = fit.insert_fov( fit.projections_c0( fit.C ) )
    d_av = fit.insert_fov( fit.data_av )
    
    if hasattr(mod, 'fov_single'):
        fov = mod.fov_single
    else:
        fov = mod.fov
    for g in np.atleast_1d(G):
        title = f'Projection {g}: kap {mod.Kappa[g]*180/np.pi}, ome {mod.Omega[g]*180/np.pi}'
        plot.compare_projection_av( 
            d_av[g].reshape(fov), proj[g].reshape(fov), title=title,
         )

def check_projections_residuals( G=None ):
    """Plots the residuals per pix3l for chosen projections with data
    
    Parameters
    ----------
    G : int or ndarray or None, optional
        projection indices, if None takes 10 equidistant ones, by default None
    """    
    if fit is None:
        print('\tNo fit available, load or obtain result first')
        return
    if G is None: # plot 10 projections over all angles
        G = np.linspace(0, fit.scanmask.shape[0]-1,num=10,dtype=int)
    for g in np.atleast_1d( G ):
        title = f'Projection {g}: kap {np.round(mod.Kappa[g]*180/np.pi,1)}, ome {np.round(mod.Omega[g]*180/np.pi,1)}'
        plot.image_residuals( fit, g, mod.fov, title=title, )

def check_projections_orientations( G=None ):
    """Plots the reconstructed average orientations for chosen projections with data
    
    Parameters
    ----------
    G : int or ndarray or None, optional
        projection indices, if None takes 10 equidistant ones, by default None
    """    
    if fit is None:
        print('\tNo fit available, load or obtain result first')
        return
    if G is None: # plot 10 projections over all angles
        G = np.linspace(0, fit.scanmask.shape[0]-1,num=10,dtype=int)
    
    if hasattr(mod, 'fov_single'):
        fov = mod.fov_single
    else:
        fov = mod.fov
    for g in np.atleast_1d( G ):
        title = f'Projection {g}: kap {np.round(mod.Kappa[g]*180/np.pi,1)}, ome {np.round(mod.Omega[g]*180/np.pi,1)}'
        ori_dat, ori_fit = fit.check_orientations(g)
        plot.compare_projection_ori( 
            ori_dat.reshape((ori_dat.shape[0],*fov)), 
            ori_fit.reshape((ori_dat.shape[0],*fov)),
            fit.q, title=title, )
        
def calculate_orientation_statistics( ):
    """Calculates prefered orientations and stds and saves them to results dict

    """
    sample_dir = _sdir( )
    global mod, fit, results
    if (mod is None or fit is None):
        print('model/fit not defined!')
        return
    results['scaling'] = fit.C[:,0].reshape(mod.nVox)
    print('\tExtracting mean orientations')
    g_pref = mod.g_ML_sample( fit.C[mod.mask_voxels] )
    results['g_pref'] = mod.insert_sparse_tomogram(g_pref)
    print('\tExtracting stds')
    stds = mod.std_sample( fit.C[mod.mask_voxels], g_pref )
    results['std']=mod.insert_sparse_tomogram(stds)
    # export vtk-file for paraview
    a_pref, b_pref, c_pref = mod.abc_pref_sample( g_pref )
    results['a_pref'] = mod.insert_sparse_tomogram(a_pref)
    results['b_pref'] = mod.insert_sparse_tomogram(b_pref)
    results['c_pref'] = mod.insert_sparse_tomogram(c_pref)
    results['inv_pf'] = orx.inverse_pf_stack(results['g_pref'], mod)
    print("\tAdded to results: 'std', 'g_pref', 'a_pref', 'b_pref', 'c_pref', 'inv_pf'")

def calculate_segments(thresh=10, min_segment_size=30, max_segments_number=31):
    """Segments the sample based on misorientation borders

    Parameters
    ----------
    thresh : float, optional
        misorientation angle threshold inside segment in degree, by default 10
    min_segment_size : int, optional
        minimum number of voxels in segment, by default 30
    max_segments_number : int, optional
        maximum number of segments (ordered by size), by default 32
    """
    global results
    with h5py.File(os.path.join(sample_dir,'analysis','crystal.h5'), 'r') as hf:
        ppgrp = hf['symmetry'][()].decode('utf-8')
    mx,my,mz,mori = seg.mori_3d( results['g_pref'], ppgrp )
    plt.figure()
    plt.hist(mori[mori<3.14]*180/np.pi,50)
    plt.xlabel('Misorientation [deg]')
    plt.ylabel('No of voxels')
    labeled_zones,zone_sizes = seg.label_zones(mori, thresh*np.pi/180,
                                               min_segment_size, max_segments_number)
    results['segments'] = labeled_zones
    mori[mori>3.14] = np.nan
    results['mori'] = mori
    results['mori'][results['mori']>3.14] = np.nan
    # results['segments'][results['segments']==0] = np.inf
    plt.figure()
    plt.bar(range(zone_sizes.size),zone_sizes)
    plt.xlabel('Zone label')
    plt.ylabel('No of voxels in zone')
    nvseg,nvtot = zone_sizes.sum(), (mori<3.14).sum()
    show_volume(data=['segments','mori'],cut=0)
    print(f'\tSegmented voxels: {nvseg}/{nvtot} ({nvseg/nvtot*100:.1f} %)')
    print("\tAdded to results: 'mori', 'segments'")

def show_volume( data='scaling', plane='z', colormap='inferno', cut=1, save_video=False ):
    """Visualizes the whole sample by slices, colored by a value of your choice

    Parameters
    ----------
    data : str or list, optional
        name of one entry in the results dict or list of entries, 
        by default 'scaling'
    plane : str, optional
        sliceplane 'x'/'y'/'z', by default 'z'
    colormap : str, optional
        identifier of matplotlib colormap, default 'inferno'
        https://matplotlib.org/stable/users/explain/colors/colormaps.html
    cut : int, optional
        cut colorscale at upper and lower percentile, by default 0.1
    """
    sample_dir = _sdir()
    if isinstance(data,np.ndarray):
        if data.ndim==3:
            data=[data]
    else:
        if isinstance(data,str):
            data = [data]
        names = data
        data = [results[key] for key in data]
    if save_video:
        save_video = os.path.join(sample_dir, 'results', f'{names[0]}_{plane}_{msc.timestring()}.gif')
    plot.interactive_tomogram( np.array(data), names, show_voxel_odf, 
                    cmap=colormap, sliceplane=plane, cut=cut, save_vid_path=save_video )

def show_slice_ipf( h, plane='z' ):
    """Plots an inverse pole figure of a sample slice

    Parameters
    ----------
    h : int
        height of the slice
    plane : str, optional
        slice direction: x/y/z, by default 'z'
    """
    sample_dir = _sdir( )
    with h5py.File(os.path.join(sample_dir,'analysis/crystal.h5'), 'r') as hf:
        ppgrp = hf['symmetry'][()].decode('utf-8')
    orx.inverse_pf_map( _slice('g_pref', h, plane), ppgrp )

def show_volume_ipf( plane='z', save_video=False ):
    sample_dir = _sdir( )
    with h5py.File(os.path.join(sample_dir,'analysis/crystal.h5'), 'r') as hf:
        ppgrp = hf['symmetry'][()].decode('utf-8')
    if save_video:
        save_video = os.path.join(sample_dir, 'results', f'ipf_{plane}_{msc.timestring()}.gif')
    orx.plot_ipf_movie(results['inv_pf'], ppgrp, plane, save_vid_path=save_video)

def show_histogram(x, nbins=50, cut=0.1, segments=None):
    """plots a histogram of a result parameter

    Parameters
    ----------
    x : str,
        name of a scalar from results
    bins : int, optional
        number of bins, by default 50
    cut : int, optional
        cut upper and lower percentile, by default 0.1
    segments : list of int, optional
        list of segments or None for all data, by default None
    """
    sample_dir = _sdir( )
    global results
    f,ax = plt.subplots()
    if segments:
        data, high, low = [], -np.inf, np.inf
        for s in segments:
            d = results[x][results['segments']==s]
            data.append( d[~np.isnan(d)] )
            low = min(low, np.percentile(d, cut))
            high = max(high, np.percentile(d, 100-cut))
        ax.hist( data, bins=nbins, 
            range=(low,high),
            label=[str(s) for s in segments],
            # histtype='step', stacked=True, fill=False
            )
        ax.legend()
        ax.set_title('Per segment')
    else:
        with h5py.File(os.path.join(sample_dir,'analysis/tomo.h5'), 'r') as hf:
            mask = hf['mask_voxels'][()]
        data = results[x].flatten()[mask]
        data = data[~np.isnan(data)]
        ax.hist( data, bins=nbins, 
                range=(np.percentile(data, cut),np.percentile(data, 100-cut)) )
        ax.set_title('All voxels')
    ax.set_xlabel(x)
    ax.set_ylabel('No. of voxels')

def show_correlations( x, y, nbins=50, cut=(0.1,0.1), segments=None ):
    """plots a 2D histogram between 2 result parameters

    Parameters
    ----------
    x : str,
        name of a scalar from results
    y : str,
        name of a scalar from results
    bins : int, optional
        number of bins, by default 50
    cut : tuple, optional
        cut upper and lower percentile of both parameters, by default (0.1,0.1)
    segments : list, optional
        list of segments or None for all data, by default None
    """
    sample_dir = _sdir( )
    if segments:
        for s in segments:
            f,ax = plt.subplots()
            data_x = results[x][results['segments']==s]
            data_y = results[y][results['segments']==s]
            filter_nan = ~np.logical_or(np.isnan(data_x), np.isnan(data_y))
            data_x, data_y = data_x[filter_nan], data_y[filter_nan]
            ax.hist2d( data_x, data_y, bins=nbins,
                    range=((np.percentile(data_x, cut[0]),np.percentile(data_x, 100-cut[0])),
                            (np.percentile(data_y, cut[1]),np.percentile(data_y, 100-cut[1]))) )
            ax.set_title(f'Segment {s}')
            ax.set_xlabel(x)
            ax.set_ylabel(y)
    else:
        with h5py.File(os.path.join(sample_dir,'analysis/tomo.h5'), 'r') as hf:
            mask = hf['mask_voxels'][()]
        data_x = results[x].flatten()[mask]
        data_y = results[y].flatten()[mask]
        ax.hist2d( data_x, data_y, bins=nbins,
                range=((np.percentile(data_x, cut[0]),np.percentile(data_x, 100-cut[0])),
                        (np.percentile(data_y, cut[1]),np.percentile(data_y, 100-cut[1]))) )
        ax.set_xlabel(x)
        ax.set_ylabel(y)

def show_voxel_odf( x,y,z, num_samples=1000 ):
    """Show a 3D plot of the ODF in the chosen voxel

    Parameters
    ----------
    x : int
        voxel x-coordinate
    y : int
        voxel y-coordinate
    z : int
        voxel z-coordinate
    """
    iv = np.ravel_multi_index((x,y,z), mod.nVox)
    if np.any(fit.C[iv]):
        title = f'Voxel {x}/{y}/{z}'
        orx.odf_cloud(mod, fit.C[iv], num_samples=num_samples, title=title )
    else:
        print('\tNo ODF in this voxel')

def show_voxel_polefigure( x,y,z, hkl=(1,0,0), mode='density',
                     alpha=0.1, num_samples=1e4 ):
    """Show a polefigure plot for the chosen voxel and hkl

    Parameters
    ----------
    x : int
        voxel x-coordinate
    y : int
        voxel y-coordinate
    z : int
        voxel z-coordinate
    hkl : tuple, optional
        Miller indices, by default (1,0,0)
    mode : str, optional
        plotting style 'scatter' or 'density', by default 'density'
    alpha : float, optional
        opacity of points, only for scatter, by default 0.1
    num_samples : int/float, optional
        number of samples for plot generation, by default 1e4
    """
    iv = np.ravel_multi_index((x,y,z), mod.nVox)
    title = f'Voxel {x}/{y}/{z}, hkl ({hkl[0]},{hkl[1]},{hkl[2]})'
    if np.any(fit.C[iv]):
        orx.plot_pole_figure(mod, fit.C[iv], hkl, mode=mode, title=title,
                             num_samples=num_samples, alpha=alpha )
    else:
        print('\tNo ODF in this voxel')

def reconstruct_1d_full( redo_import=False, only_mumottize=False, batch_size=10 ):
    """Reconstructs standard tomographic data such as azimutally averaged
    diffraction data. Uses the same alignment as textom

    Parameters
    ----------
    redo_import : bool, optional
        _description_, by default False
    only_mumottize : bool, optional
        only preprocesses a file analysis/rec1d/data_rec1d.h5, by default False
    batch_size : int, optional
        number of q-values to load at the same time. Needs to be an integer fraction
        of the total number of q-values, else it will crash at the last batch. Higher
        numbers will decrease i/o time, but require more memory, by default 10
    """
    sample_dir = _sdir( )
    msc.cp_add_dt('input/input_1Drec.py', os.path.join(sample_dir,'analysis/rec_1d/'))
    datapath = os.path.join(sample_dir,'analysis/rec_1d/data_rec1d.h5')
    if not os.path.isfile(datapath) or redo_import:
        datapath=None
    out_path = mum.backproject_all( sample_dir, 'input/input_1Drec.py', datapath, 
                            only_mumottize=only_mumottize, batch_size=batch_size)
    with h5py.File(os.path.join(sample_dir,'analysis','tomo.h5'), 'r') as hf:
        mask = hf['mask_voxels'][()]
        nVox = hf['nVox'][()]
    mask_voxels = np.zeros(np.prod(nVox), bool)
    mask_voxels[mask] = True 
    mask_voxels = mask_voxels.reshape(nVox)
    with h5py.File(out_path, 'r+') as hf:
        hf.create_dataset('mask_voxels', data=mask_voxels, compression=hdf5plugin.LZ4())
    # # compress and add voxel mask for further processing
    # with h5py.File(os.path.join(sample_dir,'analysis/rec_1d/reconstruction_1Dmm_helix_s7_2024_11_26_19h17_compressed.h5'), 'w') as hfout:
    #     with h5py.File(os.path.join(sample_dir,'analysis/rec_1d/reconstruction_1Dmm_helix_s7_2024_11_26_19h17.h5'), 'r') as hf:
    #         hfout.create_dataset('radial_units', data=hf['radial_units'][()])
    #         hfout.create_dataset(
    #             "data",
    #             data=hf['tomogram'][()],
    #             compression=hdf5plugin.LZ4()
    #         )
    #         hfout.create_dataset(
    #             "mask_voxels",
    #             data=mask_voxels,
    #             compression=hdf5plugin.LZ4()
    #         )

def save_results( ):
    """Saves the results dictionary to a h5 file

    """
    sample_dir = _sdir( )
    with h5py.File(os.path.join(sample_dir,'analysis','tomo.h5'), 'r') as hf:
        nVox = hf['nVox'][()]
    title = os.path.basename(os.path.dirname(sample_dir))
    types, names = [], []
    res_name = f'results_{msc.timestring()}'
    with h5py.File( 
        os.path.join(sample_dir,'results',f'{res_name}.h5'), 'w' ) as hf:
        hf.create_dataset('title', data=title)
        for key, value in results.items():
            if isinstance(value,np.ndarray):
                if value.ndim == 3:
                    types.append('Scalar')
                    names.append(key)
                elif value.ndim == 4:
                    types.append('Vector')
                    names.append(key)
                hf.create_dataset( key, data = value )
    hdl.write_xdmf_reader(
        os.path.join(sample_dir,'results',f'{res_name}.xdmf'),
        os.path.join(sample_dir,'results',f'{res_name}.h5'),
        nVox, names, types
    )

def link_xdmf( paths ):
    sample_dir = _sdir( )
    with h5py.File(os.path.join(sample_dir,'analysis','tomo.h5'), 'r') as hf:
        nVox = hf['nVox'][()]
    res_name = f'results_{msc.timestring()}_linked'
    files, types, names = [], [], []
    for path in paths:
        with h5py.File( os.path.join(sample_dir,'results',path), 'r' ) as hf:
            for key in hf.keys():
                try:
                    if hf[key].ndim == 3:
                        types.append('Scalar')
                        names.append(key)
                        files.append(path)
                    elif hf[key].ndim == 4:
                        types.append('Vector')
                        names.append(key)
                        files.append(path)
                except:
                    pass
    print('Found values:')
    print(names)
    hdl.write_xdmf_reader(
        os.path.join(sample_dir,'results',f'{res_name}.xdmf'),
        files, nVox, names, types
    )

def list_results():
    """Shows all results .h5 files in results directory
    """
    sample_dir = _sdir( )
    res_dir = os.path.join(sample_dir, 'results')
    res_files = msc.list_files_by_modification_time(res_dir,reverse=True,extension='.h5')
    for r in res_files:
        print(f'\r{r}')

def load_results( h5path='last', make_bg_nan=False ):
    """Loads the results from a h5 file do the results dictionary

    """
    sample_dir = _sdir( )
    global results
    t0=time()
    print('Loading results')
    if h5path == 'last':
        h5path = msc.lastfile( os.path.join(sample_dir,'results'), 'results*.h5' )
    elif os.path.dirname(h5path) == '': # if only filename
        h5path = os.path.join(sample_dir,'results',h5path)
    with h5py.File( h5path, 'r' ) as hf:
        for key in hf.keys():
            results[key] = hf[key][()]
        if make_bg_nan:
            with h5py.File(os.path.join(sample_dir,'analysis','tomo.h5')) as hf:
                mask = hf['mask_voxels'][()]
                nvox = hf['nVox'][()]
            results[key] = msc.insert_sparse_tomogram(nvox, mask, results[key].flatten()[mask])
            # tmp = np.empty_like(results[key])
            # tmp[:] = np.nan
            # tmp[mask] = results[key][mask]
            # results[key] = tmp
    print(f'\ttook {time()-t0:.2f} s')
    # del results['title']

def list_results_loaded():
    """Shows all results currently in memory
    """
    for res in results.keys():
        print(f'\rresults[\'{res}\']')

def save_images( x, ext='raw' ):
    """Export results as .raw or .tiff files for dragonfly

    Parameters
    ----------
    x : str,
        name of a scalar from results, e.g. 'scaling'
    """
    sample_dir = _sdir( )
    if results[x].dtype == np.float64:
        data = results[x].astype(np.float32)
    else:
        data = results[x]
    # data[np.isnan(data)] = 0
    if ext=='raw':
        with open(os.path.join(sample_dir,'results',x+'.raw'), 'wb') as file:
            file.write(data.tobytes())
    elif 'tif' in ext:
        iio.imwrite(
            os.path.join(sample_dir,'results',x+'.tiff'),
            data, plugin="tifffile")
    else:
        print('format not recognized')

def sort_integrated_files( source='data_integrated', target='data_integrated_1d', 
                          check_end=-6, pattern='.h5'):
    """Reads all filenames in source folder and checks if the same exist in target
    Moves the non-overlapping to an 'excluded'-subfolder 

    Parameters
    ----------
    source : str, optional
        directory with sorted files, by default 'data_integrated'
    target : str, optional
        directory with files to sort, by default 'data_integrated_1d'
    check_end : int, optional
        index of the last character of the filename to check, by default -6
    pattern : str, optional
        only filenames that contain this are searched, by default '.h5'
    """    
    sample_dir = _sdir( )

    # Create the excluded subfolder if it doesn't exist
    excl_path = os.path.join(sample_dir,target,'excluded')
    os.makedirs( excl_path, exist_ok=True)

    # make the filelist
    filelist = []
    for filename in os.listdir(os.path.join(sample_dir,source)):
        if pattern in filename:
            filelist.append( filename[:check_end])

    # Iterate over all files in the source folder
    for filename in os.listdir(os.path.join(sample_dir,target)):
        file_path = os.path.join(sample_dir,target, filename)
        # Check if it is a file and not in the list of filenames
        if os.path.isfile(file_path) and filename[:check_end] not in filelist:
            # Move the file to the subfolder
            shutil.move(file_path, os.path.join(excl_path, filename))
            print(f"Moved {filename} to {excl_path}")

    # check if anything missing
    print('Missing:')
    for name_2d in filelist:
        cnt=0
        for name_1d in os.listdir(os.path.join(sample_dir,target)):
            if name_2d == name_1d[:check_end]:
                cnt+=1
        if cnt==0:
            print(name_2d)

def help( method=None, module=None, filter='' ):
    """Prints information about functions in this library

    Parameters
    ----------
    method : str or None, optional
        get more information about a function or None for overview over all functions, by default None
    module : str or None, optional
        choose python module or None for the base TexTOM library, by default None
    filter : str, optional
        filter the displayed functions by a substring, by default ''
    """    
    if module is None:
        module = __import__(__name__)
    if method is None:
        msc.print_library_functions_and_docstrings(module, filter=filter)
    elif method in msc.list_library_functions(module):
        msc.print_function_docstring(module,method)
    else:
        print('Method name not recognized')
        msc.print_library_functions_and_docstrings(module)

def _sdir( ):
    """Imports the sample directory into a function

    Returns
    -------
    sample_dir : str
        path to sample directory

    Raises
    ------
    exc.NoPath
        raised if no path is defined
    """    
    global sample_dir
    if sample_dir is None:
        sys.tracebacklimit = 0
        raise exc.NoPath('Sample directory not defined. Use set_path(\'path/to/your/sample\')')
    return sample_dir

def _slice( x, h, plane='z'):
    """Extracts a slice from the sample and reduces it to non-Nan regions

    Parameters
    ----------
    x : str,
        name of a scalar from results
    h : int
        height of the slice
    plane : str, optional
        slice direction: x/y/z, by default 'z'

    Returns
    -------
    ndarray
        2D slice
    """
    # global results
    array = results[x]
    if plane=='x':
        sl = array[h,:,:]  
    elif plane=='y':
        sl = array[:,h,:] 
    else:
        sl = array[:,:,h] 
    return msc.crop_to_non_nan_region(sl)