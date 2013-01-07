# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# ## Import sensor data

# <codecell>

import pandas
from pandas import read_csv
import numpy
from pylab import *

output_number = 0

# <codecell>

accel_data = read_csv('./data/Accel.csv',names=['time','x','y','z'],skiprows=1)
gyro_data = read_csv('./data/Gyro.csv',names=['time','x','y','z','roll','pitch','yaw'],skiprows=1)
time_data = read_csv('./data/Timestamp.csv',names=['time','exposure_time','is_blurred'],skiprows=1)

# <codecell>

accel_data.describe()

# <codecell>

gyro_data.describe()

# <codecell>

accel_data[['x','y','z']].plot()
savefig('./out/'+str(output_number)+'.png')
output_number += 1
# <codecell>

gyro_data[['x','y','z']].plot()
savefig('./out/'+str(output_number)+'.png')
output_number += 1
gyro_data[['roll','pitch','yaw']].plot()
savefig('./out/'+str(output_number)+'.png')
output_number += 1
# <markdowncell>

# ## Timing slices

# <codecell>

import matplotlib.image as mpimg
import glob

# <markdowncell>

# ### ■ Blurred Picture

# <codecell>

# param
span = 0.1
ylim_accel = 0.6
ylim_gyro = 3.0

# <codecell>

i = 0
std_accel_blurred_list = []
std_gyro_blurred_list = []
std_exposure_blurred_list = []
for time in time_data['time']:

    if time_data['is_blurred'][i] == 0:
        i  += 1
        continue

    begin_time = time - span
    index = (accel_data['time'] > begin_time) & (accel_data['time'] < time)

    picture_filepath = glob.glob('./data/picture/'+str('%.5f' %time)+'*')
    print picture_filepath
    image = mpimg.imread(picture_filepath[0])
    plt.imshow(image)
    figure()

    subplot(121)
#    norm_accel = sqrt(accel_data[index]['x']**2+accel_data[index]['y']**2+accel_data[index]['z']**2)
    norm_accel = sqrt(accel_data[index]['x']**2+accel_data[index]['y']**2)
    std_accel_blurred_list.append(norm_accel.mean())
    ylim(0,ylim_accel)
    norm_accel.plot()
    xlabel('Time *0.1[s]',size=15)
    ylabel('Accelerometer', size=15)

    subplot(122)
    norm_gyro = sqrt(gyro_data[index]['x']**2+gyro_data[index]['y']**2+gyro_data[index]['z']**2)
    std_gyro_blurred_list.append(norm_gyro.mean())
    ylim(0,ylim_gyro)
    norm_gyro.plot()
    xlabel('Time *0.1[s]',size=15)
    ylabel('Gyroscope', size=15)

    savefig('./out/'+str(output_number)+'.png')
    output_number += 1

    std_exposure_blurred_list.append(time_data['exposure_time'][i])

    i += 1

# <markdowncell>

# ### ■ Non Blurred Picture

# <codecell>

i = 0
std_accel_nonblurred_list = []
std_gyro_nonblurred_list = []
std_exposure_nonblurred_list = []
for time_raw in time_data['time']:

    if time_data['is_blurred'][i] == 1:
        i  += 1
        continue

    time = ((time_raw*1000.0)//10.0)/100.0
    begin_time = time - span
    index = (accel_data['time'] > begin_time) & (accel_data['time'] < time)

    picture_filepath = glob.glob('./data/picture/'+str('%.5f' %time_raw)+'*')
    print picture_filepath
    image = mpimg.imread(picture_filepath[0])
    plt.imshow(image)
    figure()

    subplot(121)
#    norm_accel = sqrt(accel_data[index]['x']**2+accel_data[index]['y']**2+accel_data[index]['z']**2)
    norm_accel = sqrt(accel_data[index]['x']**2+accel_data[index]['y']**2)
    std_accel_nonblurred_list.append(norm_accel.mean())
    ylim(0,ylim_accel)
    norm_accel.plot()
    xlabel('Time *0.1[s]',size=15)
    ylabel('Accelerometer', size=15)

    subplot(122)
    norm_gyro = sqrt(gyro_data[index]['x']**2+gyro_data[index]['y']**2+gyro_data[index]['z']**2)
    std_gyro_nonblurred_list.append(norm_gyro.mean())
    ylim(0,ylim_gyro)
    norm_gyro.plot()
    xlabel('Time *0.1[s]',size=15)
    ylabel('Gyroscope', size=15)
    savefig('./out/'+str(output_number)+'.png')
    output_number += 1

    std_exposure_nonblurred_list.append(time_data['exposure_time'][i])

    i += 1

# <markdowncell>

# ## Plot mean (blue is nonblurred, red is blurred picture)

# <codecell>

figure(facecolor="w")
#xlim(0,0.2)
#ylim(0,0.5)
scatter(std_accel_blurred_list, std_gyro_blurred_list,color='r')
scatter(std_accel_nonblurred_list, std_gyro_nonblurred_list,color='b')
#label
xlabel('accelerometer',size=15)
ylabel('gyro',size=15)
savefig('./out/'+str(output_number)+'.png')
output_number += 1

# <codecell>

figure(facecolor="w")
#xlim(0,0.2)
#ylim(0,0.5)
scatter(std_exposure_blurred_list, std_gyro_blurred_list,color='r')
scatter(std_exposure_nonblurred_list, std_gyro_nonblurred_list,color='b')
#label
xlabel('accelerometer',size=15)
ylabel('exposure time[s]',size=15)
savefig('./out/'+str(output_number)+'.png')
output_number += 1

# <codecell>

# return mean of list
def mean(list):
    sum = 0.0
    count = 0
    for i in list:
        if i > 0:
            sum = sum + i
            count += 1
        else:
            continue
    return sum / count

# <codecell>

print mean(std_gyro_blurred_list)
print mean(std_gyro_nonblurred_list)

# <codecell>


