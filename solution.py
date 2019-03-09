from glob import glob
import re
import h5py
from datetime import datetime
import pytz
import pandas as pd
import numpy as np
from scipy.signal import medfilt
import matplotlib.pyplot as plt

#### PART ONE #####

filename = glob('*.h5')[0]
# nanoseconds -> rounded to nearest second
timestamp = round(int(re.match(r'\d+',filename).group())/(10**9))
utc = pytz.utc
cern_timezone = pytz.timezone('Europe/Zurich')
utc_dt = utc.localize(datetime.utcfromtimestamp(timestamp))
cern_dt = utc_dt.astimezone(cern_timezone)

print('PART ONE')
print('File name:',filename)
print('Timestamp:',timestamp)
print('Date-time (UTC):',utc_dt)
print('Date-time (CERN local time):',cern_dt)



#### PART TWO #####

file = h5py.File(filename, 'r')


data = {}

def getrow(path, element):
  if isinstance(element, h5py.Dataset):
    try:
      data_type = element.dtype
    except Exception as e:
      data_type = str(e)
    data[path] = ['Dataset', element.size, element.shape, data_type]
  else:
    data[path] = ['Group', '','','']

file.visititems(getrow)

df = pd.DataFrame.from_dict(data,orient='index',
            columns=['element_type','size','shape','data_type'])

df.to_csv('data.csv', sep=',')
print('\n\nPART TWO')
print('Saved requested data in data.csv')



### PART THREE ###

streakImageData = file['/AwakeEventData/XMPP-STREAK/StreakImage/streakImageData'][:]
streakImageHeight = file['/AwakeEventData/XMPP-STREAK/StreakImage/streakImageHeight'][0]
streakImageWidth = file['/AwakeEventData/XMPP-STREAK/StreakImage/streakImageWidth'][0]

image = np.reshape(streakImageData,(streakImageHeight,streakImageWidth))
filtered_image = medfilt(image)

fig = plt.figure(figsize=(streakImageWidth/100,streakImageHeight/100))

ax = fig.add_subplot(111)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_frame_on(False)
plt.imshow(filtered_image)
plt.savefig('streakImage.png',bbox_inches='tight')

print('\n\nPART THREE')
print('Saved image to streakImage.png')