import necessary_equations as ne
import scipy.optimize as opt



def SS_solver(r_guess, b_guesses, n_guesses, alpha, delta, A, S, b, l, v, sigma, beta, b_MU_til, upsilon_MU_til):
    '''
    Solves for the SS of the economy
    '''
    
    xi = 0.8
    tol = 1e-8
    max_iter = 500
    dist = 7
    iter = 0
    r = r_guess
    b_sp1 = b_guesses
    n_s = n_guesses
    while (dist > tol) & (iter < max_iter):
        w = ne.get_w(r, (alpha, delta, A)) # i- (a)
        sol = opt.root(ne.hh_foc, x0=[b_sp1, n_s],args=(r, w, S,(sigma, beta, b, l, v))) # ii- (a)
        b_sp1, n_s = sol.x
        euler_error_c, euler_error_n = sol.fun
        K = ne.get_K(b_sp1)
        L = ne.get_L(n_s)
        r_prime = ne.get_r(K, L, (alpha, delta, A))
        dist = (r - r_prime) ** 2
        iter += 1
        r = xi * r + (1 - xi) * r_prime     
    success = iter < max_iter

    return r, success, euler_error_c, euler_error_n