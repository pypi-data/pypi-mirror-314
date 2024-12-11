import pandas as pd
from iprint import *

def dfFormat(df):
    if isinstance(df,pd.pandas.core.series.Series):
        return {'N_N':df.to_list()}
    DF = {}
    for i in df:
        DF[i] = df[i].to_list()
    return DF


# df = pd.DataFrame({
#     'A': ['foo', 'bar', 'foo', 'bar', 'foo'],
#     'B': ['one', 'one', 'two', 'three', 'two'],
#     'C': ['small', 'large', 'large', 'small', 'large'],
# })


# df = df['C']
# ij(dfFormat(df))



# print(ipd_to_DataFrame(df))