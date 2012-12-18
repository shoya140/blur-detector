# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# ## Import sensor data

# <codecell>

import pandas
from pandas import read_csv

# <codecell>

accel_data = read_csv('./data/2012-12-15_14:10:28_+0000_Accel.csv',names=['time','x','y','z'],skiprows=1)
gyro_data = read_csv('./data/2012-12-15_14:10:28_+0000_Gyro.csv',names=['time','x','y','z','roll','pitch','yaw'],skiprows=1)
time_data = read_csv('./data/2012-12-15_14:10:28_+0000_Timestamp.csv',names=['time'],skiprows=1)

# <codecell>

accel_data.describe()

# <codecell>

gyro_data.describe()

# <codecell>

accel_data[['x','y','z']].plot()

# <codecell>

gyro_data[['x','y','z']].plot()
gyro_data[['roll','pitch','yaw']].plot()

# <markdowncell>

# ## Timing slices

# <codecell>

for time in time_data['time']:
    begin_time = time - 0.2
    index = (accel_data['time'] > begin_time) & (accel_data['time'] < time)
    norm_accel = sqrt(accel_data[index]['x']**2+accel_data[index]['y']**2+accel_data[index]['z']**2)
#    ylim(0,0.20)
    norm_accel.plot()

# <codecell>
