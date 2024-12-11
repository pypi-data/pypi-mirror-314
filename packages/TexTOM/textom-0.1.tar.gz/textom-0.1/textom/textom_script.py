from textom import *

# sample_dir = '/dataSATA/data_synchrotron/esrf_id11_2024_09_Ti64/PROCESSED_DATA/Analysis_Moritz/test_2D/'
# sample_dir = '/dataSATA/data_synchrotron/esrf_id13_2024_2_enthesis/20240215/PROCESSED_DATA/biomorph_blobb/'
# sample_dir = '/dataSATA/data_synchrotron/esrf_id13_2024_05_ch7039_enthesisII/20240501/PROCESSED_DATA/INTEG/helix_nuc1/'
# sample_dir = '/dataSATA/data_synchrotron/esrf_id13_2024_2_enthesis/20240215/PROCESSED_DATA/biomorph_leaf/'
sample_dir = '/dataSATA/data_synchrotron/esrf_id13_2023_09_ihmi1513_biomorphs/ihmi1531/id13/20230914/PROCESSED_DATA/integ/helix_s7/'
# sample_dir = '/dataSATA/data_synchrotron/esrf_id13_2024_05_ch7039_enthesisII/20240501/PROCESSED_DATA/INTEG/cement_pmma/'
# set_path('/dataSATA/data_synchrotron/esrf_id13_2024_05_ch7039_enthesisII/20240501/PROCESSED_DATA/INTEG/s3hur4/')
# set_path('/dataSATA/data_synchrotron/esrf_id13_2021_11_ls3046_zlotnikov/20211104/PROCESSED_DATA/b1_block000/')
# set_path('/dataSATA/data_synchrotron/esrf_id15a_2024_02_braids/20240208/PROCESSED_DATA/int_new/contr_36/')
# set_path('/dataSATA/data_synchrotron/esrf_id15a_2024_02_braids/20240208/PROCESSED_DATA/testdgx/ent_textom_e/')
# set_path('/dataSATA/data_synchrotron/esrf_id15a_2024_02_braids/20240208/PROCESSED_DATA/int_new/cnnm2_25/')
# set_path('/dataSATA/data_synchrotron/esrf_id13_2024_05_ch7039_enthesisII/20240501/PROCESSED_DATA/INTEG/s1529_6_cementline/')
# sample_dir = '/dataSATA/data_synchrotron/esrf_id13_2024_05_ch7039_enthesisII/20240501/PROCESSED_DATA/INTEG/coral_tt/'
# set_path('/dataSATA/data_synchrotron/esrf_id13_2023_09_ihmi1513_biomorphs/ihmi1531/id13/20230914/PROCESSED_DATA/integ/coral_s3/')
set_path(sample_dir)

# mum.mumottize(sample_dir, sub_data='data_integrated', pattern='int', 
#               q_index_range=[28,31],
#               geo_path= os.path.join(sample_dir,'analysis/geometry.py'))
# mum.just_project(os.path.join(sample_dir,'analysis/data_mumott.h5'))
# align_data('2d',redo_import=True, regroup_max=4, align_vertical=False)
# align_data('diff','data_integrated_stitchsaxsraw',redo_import=True)
# align_data(q_index_range=(0,10), sub_data='data_integrated_1d')
# align_data(q_index_range=(930,970),flip_fov=True,sub_data='data_integrated_1d',redo_import=True)
align_data()

# check_ali_consistency()
# check_projections_orientation(10)

# make_model()
# make_fit()

# get_patched_shifts('data_integrated_stitchsaxsraw')
# preprocess_data()
# preprocess_data(flip_fov=True)#, use_ion=False)
# preprocess_data(baselines=False)

# optimize( proj='full', order=0, mode=0, tol=1e-6 )
# optimize( proj='full', order=4, mode=2, tol=1e-3 )

load_opt()
# visualize_odf(40,40,50)
# visualize_sample()
check_fit_random()

# make_vtk()

# reconstruct_1d_mum(  )
# reconstruct_1d_mum( only_mumottize=True )
# reconstruct_1d_tex( flip_fov=True )
peakfit_1d( )

load_results()
with h5py.File(os.path.join(sample_dir,'analysis','crystal.h5'), 'r') as hf:
    ppgrp = hf['symmetry'][()].decode('utf-8')
gen = sym.generators(ppgrp)
g = results['g_pref']
q = rot.QfromOTP( g.reshape((np.prod(g.shape[:3]), 3))  ).reshape((*g.shape[:3], 4))
cl,cl_l = seg.find_clusters_numba(q,gen,0.15)
# orx.cluster_misorientations( slice(results['g_pref'],90), ppgrp )
# cl_labels, cl_count = orx.find_clusters( results['g_pref'], ppgrp, 0.05 )
nvox = np.prod(g.shape[:3]) - np.isnan(g[:,:,:,0]).sum()
cluster_sizes = np.array([(cl==n+1).sum() for n in range(cl_l)])
cl_pl = cl.copy()
cl_pl[cl==1] = 0
seg.plot_clusters_3d(cl_pl, 100)
orx.test_mori(results['g_pref'], ppgrp)
end=1