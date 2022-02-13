import numpy as np
import pandas as pd
from scipy.optimize import fsolve
from scipy.stats import norm

def bs_call_premium(f: float, k: float, sigma: float, r: float, t: float) -> float:

    x =  bs_call_fwd_premium(f, k, sigma, t)

    return  np.exp(-r * t) * x

def bs_put_premium(f: float, k: float, sigma: float, r: float, t: float) -> float:

    return np.exp(-r * t) * bs_put_fwd_premium(f, k, sigma, t)

def bs_call_fwd_premium(f: float, k: float, sigma: float, t: float) -> float:
    
     a = f * norm.cdf(d_plus(f, k, sigma, t)) 
     b = k * norm.cdf(d_minus(f, k, sigma, t))

     return (a - b)

def bs_put_fwd_premium(f: float, k: float, sigma: float, t: float) -> float:
    
    return f * norm.ppf(-1 * d_plus(f, k, sigma, t)) - k * norm.ppf(-1 * d_minus(f, k, sigma, t))

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
    
    s = 30000
    k = 25000
    t = 1
    r = 0.03 * 0
    sig = 0.15 * 10  
    
    print(bs_call_premium(s * np.exp(r * t),k,sig,r,t))
    print("Le Fin")