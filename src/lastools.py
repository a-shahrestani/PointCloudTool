import pandas as pd
import numpy as np
import laspy
from pathlib import Path

from laspy import PointFormat
from laspy.header import Version

_standard_classes = {'never classified': [0], 'unclassified': [1], 'ground': [2], 'low vegetation': [3],
                     'medium vegetation': [4], 'high vegetation': [5], 'building': [6], 'low point': [7],
                     'high point': [8], 'water': [9], 'rail': [10], 'road surface': [11], 'bridge deck': [12],
                     'wire-guard': [13], 'wire-conductor': [14], 'transmission tower': [15],
                     'wire-structure connector': [16]}


def _las_to_df(las_file):
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


def _json_class_mapping(file):
    pass


def _las_class_standardization(df: pd.DataFrame, classes_file=None, classes_json=None,
                               classes=None) -> pd.DataFrame:
    return df


def _df_intensity_reduction(df: pd.DataFrame, percentage=None, count=None) -> pd.DataFrame:
    if percentage is not None:
        remove_n = len(df) // 100 * percentage
    elif count is not None:
        remove_n = count
    else:
        raise Exception("Either count of the points or the percentage of dropped points should be set")
    drop_indices = np.random.choice(df.index, remove_n, replace=False)
    df_subset = df.drop(drop_indices)
    return df_subset


def _df_to_las_conversion(df, address, name, las_version=(1, 4), las_format=7, data_columns=[]):
    header = laspy.header.LasHeader(version=Version(las_version[0], las_version[1]),
                                    point_format=PointFormat(las_format))
    mins = np.floor(np.min(df[['X', 'Y', 'Z']].values, axis=0))
    header.offset = mins
    header.scale = [0.01, 0.01, 0.01]
    las = laspy.LasData(header)
    for column in data_columns:
        las[column] = df[column].values
    las.write(str(Path(f'{address}') / f'{name}.las'))
    print(f'The LAS file has been created at address {Path(address)}')


if __name__ == '__main__':
    las_file = laspy.read('../data/ttlaz.laz')
    df = _las_to_df(las_file)
    # print(df)
    # _write_df_to_csv(df, '../data/', 'ttlaz')
    # _laz_to_las_conversion(las_file, '../data/', 'ttlas')
    _df_to_las_conversion(df, address='../data/', name='ttlas2',
                          data_columns=['X', 'Y', 'Z', 'intensity', 'classification'])
