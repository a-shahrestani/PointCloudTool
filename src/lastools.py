import pandas as pd
import numpy as np
import laspy
from pathlib import Path

def las_to_df(las_file):
    data = []
    for column in list(las_file.point_format.dimension_names):
        data.append(np.array(las_file[column]))
    df = pd.DataFrame(np.array(data).T, columns=las_file.point_format.dimension_names)
    return df

def _write_df_to_csv(df, name, address):
    df.to_csv(Path(f'{address}')/f'{name}.csv')

if __name__ == '__main__':
    las_file = laspy.read('../data/test.las')
    df = las_to_df(las_file)
    print(df)
    _write_df_to_csv(df,'tt','../data/')
