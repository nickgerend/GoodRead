# Written by: Nick Gerend, @dataoutsider
# Viz: "Good Read", enjoy!

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from math import pi, cos, sin, exp, sqrt, atan2

class point:
    def __init__(self, index, item, x, y, path = -1, value = '', length = -1, width = -1, color = ''): 
        self.index = index
        self.item = item
        self.x = x
        self.y = y
        self.path = path
        self.value = value  
        self.length = length
        self.width = width
        self.color = color
    def to_dict(self):
        return {
            'index' : self.index,
            'item' : self.item,
            'x' : self.x,
            'y' : self.y,
            'path' : self.path,
            'value' : self.value,
            'length' : self.length,
            'width' : self.width,
            'color' : self.color }

def feather_blade(points, size = 1.0, sf = 2.0, ef = 2.0, sx = 0.0, ex = 2.0, scale = 25.):
    # Nick's feather equation
    xi = np.linspace(1.5, 3.5, num=points)
    x = np.linspace(sx, ex, num=points)
    a = np.linspace(0., 40., num=points)
    f = np.linspace(sf, ef, num=points)
    y = (1./xi**f)*np.sin(a*np.pi/180.)*scale
    return x*size, y*size

def feather(list_xy, df, x_shift = 0, side = 'left'):
    points = 100
    ix = 1
    iter = 1
    switch = 1
    if side == 'right':
        switch = -1
    threshold = 1000.
    x, y = feather_blade(points, 1.0) # 1.0 2.0
    cutoff = 1.0
    x_factor = 1.0
    for index, row in df.iterrows(): 
        check = row['title']
        length = row['pages']/threshold
        if length >= 1:
            length = points 
        else:
            length = int(length*points)
        for i in range(int(length*cutoff)):
            list_xy.append(point(ix, row['google_id'], y[i]*switch, x[i]*x_factor+x_shift, i, row['title'], row['pages'], row['publication_date'], row['category'] ))
        # if iter % 2 == 0:
        #     x_shift += 1./50.

        if iter % 40 == 0:
            x_factor = np.random.random()
            if x_factor < .3:
                x_factor = 1 - x_factor

        #switch *= -1
        x_shift += 1./50.
        iter += 1
    return list_xy, x_shift

#region data prep
df = pd.read_csv(os.path.dirname(__file__) + '/1001bookreviews_google.csv')
df = df.dropna()

df = df.drop_duplicates(subset=['google_id'])
df.to_csv(os.path.dirname(__file__) + '/1001bookreviews_google_clean.csv', encoding='utf-8', index=False)
#print(df.head(5))

df_high = df.loc[df['pages'] >= 80]
df_low = df.loc[df['pages'] < 80]
dfs_high = df_high.sample(frac=1)
dfs_low = df_low.sample(frac=1)

dfs_high_list = np.array_split(dfs_high, 4)
dfs_low_list = np.array_split(dfs_low, 2)

df_Left_Bot = dfs_high_list[0].sort_values(by=['pages'], ascending=True)

df_Left_Top = pd.concat([dfs_low_list[0], dfs_high_list[1]], axis=0)
df_Left_Top = df_Left_Top.sort_values(by=['pages'], ascending=False)

df_Right_Bot = dfs_high_list[2].sort_values(by=['pages'], ascending=True)

df_Right_Top = pd.concat([dfs_low_list[1], dfs_high_list[3]], axis=0)
df_Right_Top = df_Right_Top.sort_values(by=['pages'], ascending=False)

for i in range(4):
    print(len(dfs_high_list[i]))
#endregion

list_xy = []

list_xy, shift = feather(list_xy, df_Left_Bot)
list_xy, shift = feather(list_xy, df_Left_Top, shift)
list_xy, shift = feather(list_xy, df_Right_Bot, 0, 'right')
list_xy, shift = feather(list_xy, df_Right_Top, shift, 'right')

df_out = pd.DataFrame.from_records([s.to_dict() for s in list_xy])
df_out.to_csv(os.path.dirname(__file__) + '/test_feather.csv', encoding='utf-8', index=False)

print('finished')