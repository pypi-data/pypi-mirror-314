import numpy as np
import pandas as pd

def binary(
  coeffs,
  labels=[0, 1],
  r1=[0, 1.1, 0.1],
  r2=[0, 1.1, 0.1]
):
    x1 = []
    x2 = []
    y = []
    
    for i2 in np.arange(r2[0], r2[1], r2[2]):
        for i1 in np.arange(r1[0], r1[1], r1[2]):
            sum = 0
            for i, ci in enumerate(coeffs):
                p = i
                for j, cj in enumerate(ci):
                   p1 = p - j
                   p2 = j
                   sum += cj * i1**p1 * i2**p2
    
            x1.append(i1)
            x2.append(i2)
            if sum > 0:
               y.append(labels[1])
            else:
               y.append(labels[0])
    
    df = pd.DataFrame({
        'x1': x1,
        'x2': x2,
        'y': y
    })
    
    return df
