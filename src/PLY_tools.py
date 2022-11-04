import pandas as pd
import numpy as np
import open3d as o3d
from pathlib import Path

from plyfile import PlyData, PlyElement


# A function to convert PLY point cloud data to pandas Dataframe
def _ply_to_df(ply_file: PlyData) -> pd.DataFrame:
    data = np.array(ply_file.elements[0].data.tolist())
    column_names = [ply_file.elements[0].properties[i].name for i in range(len(ply_file.elements[0].properties))]
    df = pd.DataFrame(data, columns=column_names)
    return df


if __name__ == '__main__':
    ply_data = PlyData.read('../data/test.ply')
    df = _ply_to_df(ply_data)
