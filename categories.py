# Written by: Nick Gerend, @dataoutsider
# Viz: "Good Read", enjoy!

import numpy as np
import pandas as pd
import os

df1 = pd.read_csv(os.path.dirname(__file__) + '/quill_cat.csv')
df2 = pd.read_csv(os.path.dirname(__file__) + '/thegreatestbooks_quill_cat.csv')
df3 = pd.read_csv(os.path.dirname(__file__) + '/1001bookreviews_quill_cat.csv')

df1['source'] = 'Most Recommended Books'
df2['source'] = 'The Greatest Books of All Time'
df3['source'] = '1,000 Books to Read Before You Die'

dfs = []
dfs.append(df1)
dfs.append(df2)
dfs.append(df3)
df_out = pd.concat(dfs, ignore_index=True)

df_out.to_csv(os.path.dirname(__file__) + '/quill_categories.csv', encoding='utf-8', index=False)

print('finished')