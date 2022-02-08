import numpy as np
import pandas as pd
from scipy.optimize import fsolve
from scipy.stats import lognorm

def bs_call_premium(f: float, k: float, sigma: float, r: float, t: float) -> float:

    return np.exp(-r * t) * bs_call_fwd_premium(f, k, sigma, t)


def bs_put_premium(f: float, k: float, sigma: float, r: float, t: float) -> float:

    return np.exp(-r * t) * bs_put_fwd_premium(f, g, sigma, t)

def bs_call_fwd_premium(f: float, k: float, sigma: float, t: float) -> float:
    
    return f * lognorm.ppf(d_plus(f, k, sigma, t),1) - k * lognorm.ppf(d_minus(f, k, sigma, t),1)

def bs_put_fwd_premium(f: float, k: float, sigma: float, t: float) -> float:
    
    return f * lognorm.ppf(-1 * d_plus(f, k, sigma, t), 1) - k * lognorm.ppf(-1 * d_minus(f, k, sigma, t),1)

def d_plus(f: float, k: float, sigma:float, t: float) -> float:
    
    return (np.log(f/k) + 0.5 * np.power(sigma,2) * t)/(sigma * np.sqrt(t))

def d_minus(f: float, k: float, sigma:float, t: float) -> float:
    
    return (np.log(f/k) - 0.5 * np.power(sigma,2) * t)/(sigma * np.sqrt(t))


def implied_vol(f: float, k: float, p: float, t: float, r: float = None, call: bool = True, fwd: bool = False) -> float:
    if call:
        if fwd:
            price = lambda x: bs_call_fwd_premium(f, k, x, t)
        else:
            price = lambda x: bs_call_premium(f, k, x, r, t)
    else:
        if fwd:
            price = lambda x: bs_put_fwd_premium(f, k, x, t)
        else:
            price = lambda x: bs_put_premium(f, k , x, r, t)
    
    return fsolve(price, [0,10])
    


if __name__ == "__main__":
    # TODO: check that the calculations are actually correct    
    print("Le Fin")