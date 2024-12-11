import numpy as np
import os
from time import time
import sys
from numba import njit
from resource import getrusage, RUSAGE_SELF

from .fitting import fitting
from .misc import timestring

def optimize( fit:fitting, mode, name='', alg='backtracking', project_c0=True,
              tol=1e-3, minstep=1e-2, itermax=3000):
    """ Gradient descent optimizer for texture tomography

    Parameters
    ----------
    fit : class object
        object from the fitting module containing loss function and gradient
    mode : int
        decides what to optimize
        0: only zero order, 1: only highest order, 2: all orders
    -- optional --
    name : str
        add sth to the name of the output file
    tol : float
        stops optimization if the relative change of the norm of the
        gradient deceeds this value
    minstep : float
        stops optimization if the initial stepsize is reduced by this factor
    itermas : int
        stops optimization if this number of iterations is reached
    
    Return values
    ------------
    c : 1D ndarray, float
        solution found by the optimization in terms of sHSH coefficients
    opt : dict
        collection of results:
        'c' : 1D ndarray, float
            solution found by the optimization in terms of sHSH coefficients
        'loss' : 1D ndarray, float
            value of the loss function at each iteration
        'nGrad' : 1D ndarray, float
            norm of the gradient at each iteration
        'proj' : 1D ndarray, bool
            marks if c0 was projected or not for each iteration
        'prec' : float
            final precision
        'fgam' : float
            final stepsize modification
        't_total' : float
            total optimization time in s
        't_iter_av' : float
            average time per iteration in s
        'max_memory' : float
            memory usage of the process
    """

    t0 = time()
    c = fit.C
    match mode:
        case 0: # fit c0 from average intensity
            print('Start optimizing c0 from average intensity')
            modename = 'c0'
            def fun( C ):
                return fit.loss_c0( C )
            def jac( C ):
                return fit.grad_c0( C )
        case 1: # fit only highest order
            print('Start optimizing order %d' % fit.ns[-1])
            modename = 'hc'
            def fun( C ):
                return fit.loss( C )
            def jac( C ):
                return fit.grad_highest( C )
        case 2: # fit all orders
            print('Start optimizing all orders')
            modename='C'
            def fun( C ):
                return fit.loss( C )
            def jac( C ):
                return fit.grad_full( C )

    # Initialize functions    
    loss = fun( c )
    grad = jac( c )
    t1 = time()
    print('\tCompiled functions, %.3f s' % ((t1-t0)) )
    
    # calculate inverse lipschitz constants
    L = fit.lipschitz().reshape((c.shape[0],1))
    L[ L < 1e-4*L.max() ] = 0.
    invL = np.zeros_like(L)
    invL[L!=0] = 2/L[L!=0]
    gam = np.tile( invL, (1,c.shape[1]) )

    # initialize iterables
    c_next = c
    fgam, prec = 1,1
    nGrad = _vnorm(grad)
    c0_proj = []
    opt = {}
    opt['loss'] = [loss]
    opt['nGrad'] = [nGrad]
    opt['proj'] = []
    opt['max_memory'] = getrusage(RUSAGE_SELF)
    iter = 0
    t_iter_av = 0.
    try:
        # start optimization
        while ( 
            ( prec > tol ) and 
            ( iter < itermax ) and
            ( fgam > minstep)
            ):        

            # specify search direction
            direction = - gam * grad

            # determinate stepsize according to algorithm
            if alg=='backtracking':
                step_size = backtracking_line_search(
                    fun, grad, c, direction, c1=1e-4, alpha0=1.0, beta=0.5, min_alpha=1e-6)
            elif alg=='simple':
                step_size = fgam
            elif alg=='quadratic':
                step_size = quadratic_interpolation_line_search(
                    fun, grad, c, direction, c1 = 1e-4, alpha0=1.0, max_iters=10)
            
            # Update parameters with the found step size
            c_next = c + step_size * direction
            
            # project 0-order coefficients to non-negative values
            if project_c0:
                c_next[:,0], c0_proj = _project_c0(c_next[:,0])

            loss_next = fun( c_next )
            if loss_next < loss: # check if loss function decreased
                iter += 1
                # accept new values
                c = c_next
                loss = loss_next
                # get new gradient
                grad = jac( c )
                # get precision of fit
                nGrad_m1 = nGrad
                nGrad = _vnorm(grad)
                prec = np.abs(nGrad_m1-nGrad)/nGrad
                # write into opt dictionary
                opt['loss'].append( loss )
                opt['nGrad'].append( nGrad )
                opt['proj'].append( c0_proj )
                opt['max_memory'] = max( getrusage(RUSAGE_SELF), opt['max_memory'] )

                t_iter_av = (time()-t1)/iter
                sys.stdout.write('\r\tIt %d, loss: %5.3f, t/it: %.2f s, precision: %.5e         ' % (
                    iter,loss,t_iter_av, prec))
                sys.stdout.flush()
            else: 
                fgam *= 0.8
                # break
    finally:
        opt['c'] = c # optimized parameters
        opt['t_iter_av'] = t_iter_av # average time per iteration in s
        opt['t_total'] = time()-t0 # total optimization time in s
        opt['prec'] = prec # final precision
        opt['MDL'] = fit.MDL(loss)
        # opt['fgam'] = fgam # final stepsize modification
        print('\n\tFinished. total time: %.2f min' % ( (time()-t0)/60 ))
        if fgam <= minstep:
            print('\t\tMinimum stepsize reached')

        # write solution to file
        if name != '':
            name = '_'+name
        resname = 'opt_%s_%s_nmax%s%s_%s.h5' % (
            fit.title, modename, fit.ns[-1], name, timestring())
        opt['resname'] = resname
        # os.makedirs('output/', exist_ok=True)
        # with open('output/'+resname, 'wb') as file:
        #     dump(opt, file)
        return c, opt

def backtracking_line_search(
        loss, grad, theta, direction, 
        c1 = 1e-4, alpha0=1.0, beta=0.5, min_alpha=1e-2 ):
    """Rudimentary search for a stepsize that gives us sufficient progress as measured by the Armijo condition

    A common choice for alpha_0 is alpha_0 = 1, but this can vary
    somewhat depending on the algorithm. The choice of c1 can range
    from extremely small (10e-4, encouraging larger steps) to relatively
    large (0.3, encouraging smaller steps), and typical values of beta range
    from 0.1, (corresponding to a relatively coarse search) to 0.8 (corre-
    sponding to a finer search).
    https://mdav.ece.gatech.edu/ece-3803-fall2021/notes/11-notes-3803-f21.pdf

        Parameters:
        loss (function): Objective function to minimize.
        grad (np.array): Current gradient.
        theta (np.array): Current parameter vector.
        direction (np.array): Descent direction (e.g., negative gradient).
        c1 (float): Armijo condition constant for sufficient decrease.
        alpha_0 (float): Initial step size.
        min_alpha (float): Minimum step size.
        
    Returns:
        alpha (float): Step size that approximately minimizes the loss along `direction`.
    """
    # Evaluate the loss and gradient at the starting point
    f0 = loss(theta)
    g0 = np.einsum('ij,ij->',direction,grad) #this does not give the good gradient - why?

    step_size = alpha0
    # Check Armijo condition for sufficient decrease
    while loss(theta + step_size * direction) > f0 + c1 * step_size * g0:
        step_size *= beta  # Reduce step size by factor beta
        if step_size <= min_alpha:
            break
    return step_size


def quadratic_interpolation_line_search(loss, grad, theta, direction, c1 = 1e-4, alpha0=1.0, max_iters=10):
    """Quadratic interpolation line search along the search direction.
    
    Parameters:
        loss (function): Objective function to minimize.
        grad (np.array): Current gradient.
        theta (np.array): Current parameter vector.
        direction (np.array): Descent direction (e.g., negative gradient).
        c1 (float): Armijo condition constant for sufficient decrease.
        alpha0 (float): Initial step size.
        max_iters (int): Maximum number of line search iterations.
        
    Returns:
        alpha (float): Step size that approximately minimizes the loss along `direction`.
    """
    
    # Evaluate the loss and gradient at the starting point
    f0 = loss(theta)
    g0 = np.einsum('ij,ij->',direction,grad)
    
    alpha_curr = alpha0  # Current step size guess
    f_curr = loss(theta + alpha_curr * direction)  # Loss at current alpha

    for _ in range(max_iters):
        # Check Armijo condition for sufficient decrease
        if f_curr <= f0 + c1 * alpha_curr * g0:
            return alpha_curr
        
        if alpha_curr == 0:
            break

        # Fit a quadratic model based on the two points: (0, f0) and (alpha_curr, f_curr)
        a = ((f_curr - f0) - alpha_curr * g0) / alpha_curr**2
        
        # Calculate the minimum of the quadratic model
        alpha_star = -g0 / (2 * a)
        
        # Clip alpha_star to be within reasonable bounds
        if alpha_star < 0 or alpha_star > alpha_curr / 2:
            alpha_star = alpha_curr / 2
        
        # Update interval for next iteration
        alpha_curr = alpha_star
        f_curr = loss(theta + alpha_curr * direction)

    return alpha_curr

def _vnorm( v ):
    " calculates the vector norm "
    if isinstance(v,np.ndarray):
        return (v**2).sum()**(1/2)
    else:
        return 1

@njit 
def _project_c0( c0 ):
    " projects any negative values to 0 "
    proj = np.any(c0<0)
    if proj:
        c0[c0<0] = 0
    return c0, proj
