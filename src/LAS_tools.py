import pandas as pd
import numpy as np
import laspy
from pathlib import Path

from src.manipulation_tools import _df_to_las_conversion


def _las_to_df(las_file: laspy.LasData) -> pd.DataFrame:
    data = []
    columns = list(las_file.point_format.dimension_names)
    columns[:3] = ['x','y','z']
    for column in columns:
        data.append(np.array(las_file[column]))
    df = pd.DataFrame(np.array(data).T, columns=columns)
    return df


# compressing a LAS file into LAZ and vise versa
def _las_to_laz_conversion(las_file: laspy.LasData, address: str, name: str, do_compress: bool = True):
    if do_compress:
        las_file.write(do_compress=do_compress, destination=Path(f'{address}') / f'{name}.laz')
    else:
        las_file.write(do_compress=do_compress, destination=Path(f'{address}') / f'{name}.las')


if __name__ == '__main__':
    las_file = laspy.read('../../datasets/Tile 1 2.laz')
    df = _las_to_df(las_file)
    # df = pd.read_csv('../data/testdf.csv')
    print(df)
    print(df.columns)
    # _write_df_to_csv(df, '../data/', 'ttlaz')
    # _laz_to_las_conversion(las_file, '../data/', 'ttlas')
    # _df_to_las_conversion(df, address='../data/', name='ttlas3',
    #                       data_columns=['X', 'Y', 'Z', 'intensity', 'classification'])

