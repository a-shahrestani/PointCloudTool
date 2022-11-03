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


def _df_to_las_conversion(df, address, name, las_version=(1, 4), las_format=7):
    hdr = laspy.header.LasHeader(version=Version(las_version[0], las_version[1]), point_format=PointFormat(las_format))
    mins = np.floor(np.min(df[['x', 'y', 'z']].values, axis=1))
    hdr.offset = mins
    hdr.scale = [0.01, 0.01, 0.01]
    outfile = laspy.file.File(Path(f'{address}') / f'{name}.las', mode="w", header=hdr)


if __name__ == '__main__':
    las_file = laspy.read('../data/ttlaz.laz')
    # df = las_to_df(las_file)
    # print(df)
    # _write_df_to_csv(df, '../data/', 'ttlaz')
    _laz_to_las_conversion(las_file, '../data/', 'ttlas')
