

import numpy as np
from scipy.special import wofz as Faddeeva_function
from scipy.special import  iv


def ive(n, x):
    return iv(n, x) * np.exp(-x)


def Z(xi):
    return 1j * np.sqrt(np.pi) * Faddeeva_function(xi)

def Zp(xi):
    return -2*(1 + xi*Z(xi))



def complex_grid(w_domain, n_real=256, n_imag=256):

    wr_min = w_domain[0]
    wi_min = w_domain[1]

    wr_max = w_domain[2]
    wi_max = w_domain[3]

    dwr = (wr_max - wr_min ) /( n_real -1)
    wr = np.arange(n_real) *dwr + wr_min

    dwi = (wi_max - wi_min ) /( n_imag -1)
    wi = np.arange(n_imag) *dwi + wi_min

    # ... and build a multidimensional version of w
    wwr, wwi = np.meshgrid(wr, wi, indexing='ij')
    ww = wwr + 1j *wwi

    return ww.T#, wr, wi
