import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

file_path = "D:\\final_project\\02_code\\mobi-ros\\02_Duc\\data\\2023_10_26\\storeDataCalculated.csv"
df = pd.read_csv(file_path)
num_rows, num_columns = df.shape

the0 = df['Degree0_rad']
x0 = df['XCoordinate0']
y0 = df['YCoordinate0']

the1 = df['Degree1_rad']
x1 = df['XCoordinate1']
y1 = df['YCoordinate1']

d_theta = []

for i in range(1):
    finding_beta = 0
    min_d_cos_beta = 5
    for j in range(num_rows-1):        
        distance_ = math.sqrt(x0[i]**2+y0[i]**2)
        cos_beta = (distance_ * math.cos(the0[i]) - x0[i] + x1[j]) / distance_
        d_cos_beta = abs(cos_beta - math.cos(the1[j]))
        if(d_cos_beta < min_d_cos_beta):
            min_d_cos_beta = d_cos_beta
            print(the1[j])
            print(the0[i])
            finding_beta = the1[j] - the0[i]
    d_theta.append(round(finding_beta, 2))


# print(d_theta)