import numpy as np


def get_L(n):
    '''
    Function to compute aggregate
    labor supplied
    '''
    L = n.sum()
    return L


def get_K(b):
    '''
    Function to compute aggregate
    capital supplied
    '''
    K = b.sum()
    return K


def get_r(K, L, params):
    '''
    Compute the interest rate from
    the firm's FOC
    '''
    alpha, delta, A = params

    r = alpha * A * (L / K) ** (1 - alpha) - delta
    return r


def get_w(r, params):
    '''
    Solve for the w that is consistent
    with r from the firm's FOC
    '''
    alpha, delta, A = params
    w = (1 - alpha) * A * ((alpha * A) / (r + delta)) ** (alpha / (1 - alpha))
    return w


def mu_c_func(c, sigma):
    '''
    Marginal utility of consumption
    '''
    mu_c = c ** -sigma
    return mu_c


def get_c(r, w, b_s, b_sp1, n):
    '''
    Find consumption using the budget constraint
    and the choice of savings (b_sp1)
    '''
    c = (1 + r) * b_s + w * n - b_sp1
    return c



def sumsq(params, *objs):
    '''
    This function generates the sum of squared deviations between the
    constant Frisch elasticity function and the elliptical utility
    function.
    '''
    theta, l_tilde, n_grid = objs
    b, k, upsilon = params
    CFE = ((n_grid / l_tilde) ** (1 + theta)) / (1 + theta)
    ellipse = (b * ((1 - ((n_grid / l_tilde) ** upsilon)) **
                    (1 / upsilon)) + k)
    errors = CFE - ellipse
    ssqdev = (errors ** 2).sum()
    return ssqdev


def sumsq_MU(params, *objs):

    theta, l_tilde, n_grid = objs
    b, upsilon = params
    CFE_MU = (1.0 / l_tilde) * ((n_grid / l_tilde) ** theta)
    ellipse_MU = (b * (1.0 / l_tilde) * ((1.0 - (n_grid / l_tilde) **
                                          upsilon) **
                                         ((1.0 / upsilon) - 1.0)) *
                  (n_grid / l_tilde) ** (upsilon - 1.0))
    errors = CFE_MU - ellipse_MU
    ssqdev = (errors ** 2).sum()
    return ssqdev

def estimation(frisch, l_tilde):
    theta = 1 / frisch
    N = 101

    b_init = .6701

    upsilon_init = 2.3499

    n_grid = np.linspace(0.01, 0.8, num=N)

    ellipse_MU_params_init = np.array([b_init, upsilon_init])
    ellipse_MU_objs = (theta, l_tilde, n_grid)
    bnds_MU = ((None, None), (None, None))
    ellipse_MU_params_til = opt.minimize(sumsq_MU,
                                         ellipse_MU_params_init,
                                         args=(ellipse_MU_objs),
                                         method="L-BFGS-B",
                                         bounds=bnds_MU, tol=1e-15)
    (b_MU_til, upsilon_MU_til) = ellipse_MU_params_til.x


    return b_MU_til, upsilon_MU_til