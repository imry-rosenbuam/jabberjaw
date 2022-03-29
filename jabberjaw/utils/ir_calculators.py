import pandas as pd
import numpy as np

def continious_compounding(rate: float, time: float) -> float:
    """ this function take an anualized rate and time in years and return the compounded rate"""
    return np.exp(rate * time)


def discrete_compounding(rate: float, time: float, frequency: int) -> float:
    """the function take a rate, time and frequency and return the compounded rate
    """
    return np.power(1+rate/frequency,frequency * time)

if __name__ == "__main__":
    print(continious_compounding(1,1))
    print("Le Fin")