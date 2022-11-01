import pandas as pd
import numpy as np
import laspy

las = laspy.read('../data/test.las')
print(np.unique(las.classification))

# for getting the dimention names
list(las.point_format.dimension_names)
# for reading a column
las['X'] # x for values in double
las.X

# accessing the header
las.header


# creation

las = laspy.read("some_file.laz")

new_las = laspy.LasData(las.header)
new_las.points[las.classification == 2].copy()
new_las.write("ground.laz")

new_hdr = laspy.LasHeader(version="1.4", point_format=6)
# You can set the scales and offsets to values tha suits your data
new_hdr.scales = np.array([1.0, 0.5, 0.1])
new_las = laspy.LasData(new_hdr)