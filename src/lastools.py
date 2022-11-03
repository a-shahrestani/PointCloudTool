import pandas as pd
import numpy as np
import laspy
from pathlib import Path

from laspy import PointFormat
from laspy.header import Version


def las_to_df(las_file):
    data = []
    for column in list(las_file.point_format.dimension_names):
        data.append(np.array(las_file[column]))
    df = pd.DataFrame(np.array(data).T, columns=las_file.point_format.dimension_names)
    return df


def _write_df_to_csv(df, address, name):
    df.to_csv(Path(f'{address}') / f'{name}.csv')


def _las_to_laz_conversion(las_file, address, name):
    las_file.write(do_compress=True, destination=Path(f'{address}') / f'{name}.laz')


def _laz_to_las_conversion(laz_file, address, name):
    laz_file.write(do_compress=False, destination=Path(f'{address}') / f'{name}.las')


def _df_to_las_conversion(df, address, name, las_version=(1, 4), las_format=7, data_columns=[]):
    header = laspy.header.LasHeader(version=Version(las_version[0], las_version[1]),
                                    point_format=PointFormat(las_format))
    mins = np.floor(np.min(df[['x', 'y', 'z']].values, axis=1))
    header.offset = mins
    header.scale = [0.01, 0.01, 0.01]
    las = laspy.LasData(header)
    for column in data_columns:
        las[column] = df[column].values
    las.write(str(Path(f'{address}') / f'{name}.las'))
    print(f'The LAS file has been created at address {Path(address)}')


if __name__ == '__main__':
    las_file = laspy.read('../data/ttlaz.laz')
    df = las_to_df(las_file)
    # print(df)
    # _write_df_to_csv(df, '../data/', 'ttlaz')
    # _laz_to_las_conversion(las_file, '../data/', 'ttlas')
    _df_to_las_conversion(df, address='../data/', name='ttlas2',
                          data_columns=['X', 'Y', 'Z', 'intensity', 'classification'])
