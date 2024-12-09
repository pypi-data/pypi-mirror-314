import numpy as np

from scipy.optimize import leastsq


def AdustPmaj(isophote, harmonic, grad):
    """
    Adjusts the major axis position of an isophote based on the given harmonic and gradient values.

    Parameters:
    - isophote: An object representing an isophote.
    - harmonic: The harmonic value used for adjustment.
    - grad: The gradient value used for adjustment.

    Returns:
    - new_isophote: A new isophote object with the adjusted major axis position.
    """

    new_isophote = isophote.copy()

    delta_pmaj = - harmonic / grad
    new_isophote.x0 += delta_pmaj * np.cos(isophote.pa)
    new_isophote.y0 += delta_pmaj * np.sin(isophote.pa)

    return new_isophote


def AdustPmin(isophote, harmonic, grad):
    """
    Adjusts the minimum semi-major axis length of an isophote based on the given harmonic and gradient values.

    Parameters:
    - isophote: An instance of the Isophote class representing an isophote.
    - harmonic: The harmonic value used for adjustment.
    - grad: The gradient value used for adjustment.

    Returns:
    - new_isophote: A new instance of the Isophote class with the adjusted minimum semi-major axis length.
    """

    new_isophote = isophote.copy()

    delta_pmin = - harmonic * (1 - isophote.eps) / grad
    new_isophote.x0 -= delta_pmin * np.sin(isophote.pa)
    new_isophote.y0 += delta_pmin * np.cos(isophote.pa)

    return new_isophote
    

def AdjustEllipticity(isophote, harmonic, grad):
    new_isophote = isophote.copy()

    delta_eps = -2 * harmonic * (1 - isophote.eps) / (isophote.sma * grad)
    new_isophote.eps += delta_eps

    return new_isophote


def AdjustPA(isophote, harmonic, grad):
    new_isophote = isophote.copy()

    delta_pa = 2 * harmonic * (1 - isophote.eps) / (isophote.sma * grad * ((1 - isophote.eps)**2 - 1))
    new_isophote.pa += delta_pa
    new_isophote.pa = new_isophote.pa % (2 * np.pi)

    return new_isophote


def lower_harmonic_function(phi, params):
    i0, a1, b1, a2, b2 = params
    return i0 + a1 * np.sin(phi) + b1 * np.cos(phi) + a2 * np.sin(2 * phi) + b2 * np.cos(2 * phi)

def higher_harmonic_function(phi, params):
    i0, a3, b3, a4, b4, a5, b5 = params
    
    return i0 + a3 * np.sin(3 * phi) + b3 * np.cos(3 * phi) + a4 * np.sin(4 * phi) + b4 * np.cos(4 * phi)


def fit_lower_harmonics(phi, samp):

    def residuals(params):
        return samp - lower_harmonic_function(phi, params)

    params = leastsq(residuals, [np.nanmean(samp), 1, 1, 1, 1])[0]
    
    return params


def fit_higher_harmonics(phi, samp):
    
        def residuals(params):
            return samp - higher_harmonic_function(phi, params)
    
        params = leastsq(residuals, [np.nanmean(samp), 1, 1, 1, 1, 1, 1])[0]
        
        return params
