import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

file_path1 = "D:\\final_project\\02_code\\mobi-ros\\02_Duc\\data\\19_10_2023\\storeData.csv"
df1 = pd.read_csv(file_path1)

file_path2 = "D:\\final_project\\02_code\\mobi-ros\\02_Duc\\data\\19_10_2023\\storeData1.csv"
df2 = pd.read_csv(file_path2)

distance = ((df2['XCoordinate'] - df1['XCoordinate'])**2 + (df2['YCoordinate'] - df1['YCoordinate'])**2).apply(lambda x: x**0.5)
print(distance.mean())

dX = df2['XCoordinate'] - df1['XCoordinate']
dY = df2['YCoordinate'] - df1['YCoordinate']
angle = np.arctan2(dY, dX)
print(angle.mean())

df1['x2'] = df1.apply(lambda row: row['XCoordinate'] + 115.421 * math.cos(0.908233), axis=1)
df1['y2'] = df1.apply(lambda row: row['YCoordinate'] + 115.421 * math.sin(0.908233), axis=1)










fig, ax = plt.subplots(2, 2)
# fig, ax = plt.subplots()
ax[0, 0].scatter(df1['XCoordinate'],df1['YCoordinate'],s=0.1,c='green')
ax[0, 0].scatter(0, 0, s=30, c = 'red')
ax[0, 0].set_xlim(-400, 400)
ax[0, 0].set_ylim(-400, 400)

ax[0, 1].scatter(df2['XCoordinate'],df2['YCoordinate'],s=0.1,c='green')
ax[0, 1].scatter(0, 0, s=30, c = 'red')
ax[0, 1].set_xlim(-400, 400)
ax[0, 1].set_ylim(-400, 400)

ax[1, 0].scatter(df1['XCoordinate'],df1['YCoordinate'],s=0.1,c='green')
ax[1, 0].scatter(df2['XCoordinate'],df2['YCoordinate'],s=0.1,c='red')
ax[1, 0].scatter(0, 0, s=30, c = 'red')
ax[1, 0].set_xlim(-400, 400)
ax[1, 0].set_ylim(-400, 400)

ax[1, 1].scatter(df1['XCoordinate'],df1['YCoordinate'],s=0.1,c='green')
ax[1, 1].scatter(df2['XCoordinate'],df2['YCoordinate'],s=0.1,c='red')
ax[1, 1].scatter(df1['x2'],df1['y2'],s=0.1,c='blue')
ax[1, 1].scatter(0, 0, s=30, c = 'red')
ax[1, 1].set_xlim(-400, 400)
ax[1, 1].set_ylim(-400, 400)

# ax.scatter(df1['XCoordinate'],df1['YCoordinate'],s=0.1,c='green')
# ax.scatter(df2['XCoordinate'],df2['YCoordinate'],s=0.1,c='red')
# ax.scatter(0, 0, s=30, c = 'red')
# ax.set_xlim(-400, 400)
# ax.set_ylim(-400, 400)

# ax.scatter(df1['XCoordinate'],df1['YCoordinate'],s=0.1,c='green')
# ax.scatter(df2['XCoordinate'],df2['YCoordinate'],s=0.1,c='red')
# ax.scatter(df1['x2'],df1['y2'],s=0.1,c='blue')
# ax.scatter(0, 0, s=30, c = 'red')
# ax.set_xlim(-400, 400)
# ax.set_ylim(-400, 400)
plt.show()