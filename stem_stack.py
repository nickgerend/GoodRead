# Written by: Nick Gerend, @dataoutsider
# Viz: "Good Read", enjoy!

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from math import pi, cos, sin, exp, sqrt, atan2
#pd.set_option('display.max_rows', None)

class point:
    def __init__(self, index, item, x, y, path = -1, value = ''): 
        self.index = index
        self.item = item
        self.x = x
        self.y = y
        self.path = path
        self.value = value  
    def to_dict(self):
        return {
            'index' : self.index,
            'item' : self.item,
            'x' : self.x,
            'y' : self.y,
            'path' : self.path,
            'value' : self.value }

def ellipse_y(a, b, xs, xe, points):
    x = np.linspace(xs, xe, num=points)
    y = (b/a)*np.sqrt(a**2-x**2)
    return x, y

def ellipse_x(a, b, y):
    x = sqrt(-((a**2.*y**2.-b**2.*a**2.)/(b**2.)))
    return x

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

#region data prep
df = pd.read_csv(os.path.dirname(__file__) + '/1001bookreviews_google_clean.csv')
df_cat_count = df.groupby('category').count().reset_index()
# Lump singles into 'Other'
df_cat_count['type'] = ['[\'All Single-Book Categories\']' if x == 1 else y for x, y in zip(df_cat_count['google_id'], df_cat_count['category'])]
# Save out lumped categories
df_cat_count.to_csv(os.path.dirname(__file__) + '/1001bookreviews_quill_cat.csv', encoding='utf-8', index=False)
# Final group
df_cat_count = df_cat_count.groupby('type').sum()
group_sort = df_cat_count.sort_values(by=['google_id'], ascending=[True]).reset_index()
group_sort['cat_perc'] = group_sort['google_id']/len(df.index)
print(group_sort)
#endregion

#region constants
top_x = 0.15 # 0.15 0.3
top_y = 8.5 #6 19.5
btm_x = 0.15 # 0.15 0.3
btm_y = -3.25 #-2.5 -7.0
#endregion

#region algorithm
upper = top_y - 0.01
lower = 0.0
delta = upper-lower
offset = 0
list_xy = []
ix = 0
resolution = 100
spine_b = 0.05 #0.05 0.15
path = 1
xt = []
yt = []
for index, row in group_sort.iterrows():
    y_high = upper-offset
    y_low = y_high-delta*row['cat_perc']
    offset += delta*row['cat_perc']
    x_high = ellipse_x(top_x, top_y, y_high)
    x_low = ellipse_x(top_x, top_y, y_low)   
    # v (top down bend) >list_xy.append(point(ix, index, -x_high, y_high, 1, 0))
    x, y = ellipse_y(x_high, -spine_b, -x_high, x_high, resolution)
    for i in range(resolution):
        list_xy.append(point(ix, -(index+1), x[i], y_high+y[i], path, row['type']))
        path += 1
    # / (right side inward bend) >list_xy.append(point(ix, index, x_high, y_high, 2, 0))
    x, y = ellipse_y(top_x, top_y, x_high, x_low, resolution)
    for i in range(resolution):
        list_xy.append(point(ix, -(index+1), x[i], y[i], path, row['type']))
        path += 1
    # ^ (bottom down bend) >list_xy.append(point(ix, index, -x_high, y_low, 4, 0))
    x, y = ellipse_y(x_low, -spine_b, x_low, -x_low, resolution)
    for i in range(resolution):
        list_xy.append(point(ix, -(index+1), x[i], y_low+y[i], path, row['type']))
        path += 1
    if index == len(group_sort.index)-1:
        xt = x
        yt = y
    # \ (left side inward bend) >list_xy.append(point(ix, index, x_high, y_low, 3, 0))
    x, y = ellipse_y(top_x, top_y, -x_low, -x_high, resolution)
    for i in range(resolution):
        list_xy.append(point(ix, -(index+1), x[i], y[i], path, row['type']))
        path += 1
    path = 1

# pen tip
for i in range(resolution):
        list_xy.append(point(ix, -(index+2), xt[i], yt[i], path, '[\'aaa\']'))
        path += 1
x, y = ellipse_y(btm_x, btm_y, -btm_x, btm_x, resolution)
for i in range(resolution):
        list_xy.append(point(ix, -(index+2), x[i], y[i], path, '[\'aaa\']'))
        path += 1

#endregion

#region output
df_quill = pd.DataFrame.from_records([s.to_dict() for s in list_xy])
df_quill['color'] = df_quill['value']
df_feather = pd.read_csv(os.path.dirname(__file__) + '/test_feather.csv')
df_out = pd.concat([df_feather, df_quill], ignore_index=True)
df_out['z'] = [feather(y-btm_y, top_y-btm_y, 0.5) for y in df_out['y']]
df_out.to_csv(os.path.dirname(__file__) + '/test_quill.csv', encoding='utf-8', index=False)
#endregion

print('finished')