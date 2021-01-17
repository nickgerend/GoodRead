# Written by: Nick Gerend, @dataoutsider
# Viz: "Good Read", enjoy!

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from math import pi, cos, sin, exp, sqrt, atan2
import matplotlib.pyplot as plt

def feather(x, length, cutoff_0_to_2):
    xt = x/length
    xf = xt*cutoff_0_to_2
    # x space
    xr = [0., 2.0]
    # paramters
    xi = [1.5, 3.5]
    a = [0., 40.]
    f = [2.0, 2.0]
    # parameter linear transform
    xi_t = np.interp(xf, xr, xi)
    a_t = np.interp(xf, xr, a)
    f_t = np.interp(xf, xr, f)
    # Nick's feather equation
    y = (1./xi_t**f_t)*sin(a_t*pi/180.)*25.
    return y

df = pd.read_csv(os.path.dirname(__file__) + '/quill.csv')
df['z'] = [feather(y+2.5, 8.5, 0.5) for y in df['y']]
df.to_csv(os.path.dirname(__file__) + '/quill.csv', encoding='utf-8', index=False)