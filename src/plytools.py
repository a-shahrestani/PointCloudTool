import pandas as pd
import numpy as np
import open3d as o3d
from pathlib import Path
from plyfile import PlyData, PlyElement


def ply_to_df(ply_file):
    data = np.array(ply_file.elements[0].data.tolist())
    column_names = [ply_file.elements[0].properties[i].name for i in range(len(ply_file.elements[0].properties))]
    df = pd.DataFrame(data, columns=column_names)
    return df


def _write_df_to_csv(df, name, address):
    df.to_csv(Path(f'{address}') / f'{name}.csv')


if __name__ == '__main__':
    # pcd = o3d.io.read_point_cloud('../data/test.ply')
    # print(pcd)
    ply_data = PlyData.read('../data/test.ply')
    df = ply_to_df(ply_data)
    _write_df_to_csv(df, 'ttply', '../data/')
