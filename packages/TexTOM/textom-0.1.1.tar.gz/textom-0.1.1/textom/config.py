import numpy as np # don't delete this line
##################################################

# Define how many cores you want to use 
n_threads = 8 

# Choose if you want to use a GPU for integration and alignment
use_gpu = True

# Choose your precision
# recommended np.float64 for double precision or np.float32 for low-memory mode
data_type = np.float32
