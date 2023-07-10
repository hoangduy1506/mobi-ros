import serial
import time
import math
import numpy as np
import matplotlib.pyplot as plt
# from mpl_toolkits import mplot3d
import csv
import pandas as pd
from matplotlib.animation import FuncAnimation

### Create a csv file ###
header = ['x', 'y', 'z', 'robot_x', 'robot_y', 'robot_z']
with open('storeData.csv', 'w', encoding='UTF8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)

### Create a struct ###
class my2DStruct:
    def __init__ (self, value1, value2):
        self.value1= value1
        self.value2= value2

### Create a two dimension array to store and implement filter
array_2d = [[my2DStruct(0.0, 0.0) for _ in range(5000)] for _ in range(5)]
xAxes=[]
yAxes=[]
posArray= []

# Define function drawing 3D Mapping 
def drawing3D():
    # myFigure = plt.figure(dpi=200, figsize=(10,10))
    # ax = plt.axes(projection ='3d')
    xAxes=[]
    yAxes=[]
    zAxes=[]
    
    xAxes1=[]
    yAxes1=[]
    zAxes1=[]
    
    xAxes2=[]
    yAxes2=[]
    zAxes2=[]
    
    limit_of_data = True
    changePOV= True
    with open("data3D.txt", "a") as file:
       while limit_of_data:
           while arduino.in_waiting == 0:
                pass
           dataPacket = arduino.readline()
           dataPacket  = str(dataPacket, 'utf-8')    
           dataPacket  = dataPacket.strip('\r\n')
           if (dataPacket == 'End Data'):
                limit_of_data = False
           else:
                splitData = dataPacket.split(',')
                dist    = float(splitData[2])
                pitch   = float(splitData[1]) *3.14/180
                yaw     = float(splitData[0]) *3.14/180
                
                xAxes.append(dist*(np.cos(pitch))*(np.cos(yaw)))
                yAxes.append(dist*(np.cos(pitch))*(np.sin(yaw)))
                zAxes.append(dist*(np.sin(pitch)))
                
                if(yaw>0 and yaw<=3.14):
                    xAxes1.append(dist*(np.cos(pitch))*(np.cos(yaw)))
                    yAxes1.append(dist*(np.cos(pitch))*(np.sin(yaw)))
                    zAxes1.append(dist*(np.sin(pitch)))
                    
                elif(yaw>3.14 and yaw<=6.28):
                    xAxes2.append(dist*(np.cos(pitch))*(np.cos(yaw)))
                    yAxes2.append(dist*(np.cos(pitch))*(np.sin(yaw)))
                    zAxes2.append(dist*(np.sin(pitch)))

                
                xTemp= dist*(np.cos(pitch))*(np.cos(yaw))               
                yTemp= dist*(np.cos(pitch))*(np.sin(yaw))
                zTemp= dist*(np.sin(pitch))
                
                print(xTemp,yTemp,zTemp, dist)
                
                file.write(str(xTemp) + " " + str(yTemp) + " " + str(zTemp))
                file.write('\n')
    
    # loop to input and display user-defined elev, azim, roll
    while changePOV:
        # get user input for elev, azim, roll
        elev = input("Enter the elevation angle in degrees: ")
        if elev == 'end':
            changePOV= False
            break
        elev = int(elev)

        azim = input("Enter the azimuth angle in degrees: ")
        if azim == 'end':
            changePOV= False
            break
        azim = int(azim)

        roll = input("Enter the roll angle in degrees: ")
        if roll == 'end':
            changePOV= False
            break
        roll = int(roll)
        
        POVMode= input("Enter the POVMode: ")
        if POVMode== 'end':
            changePOV= False
            break
        POVMode= int(POVMode) 
        # POVMode=1 to view 0-180 || POVMode=2 to view 180-360 || POVMode=0 To view full
        
        
        if(1==POVMode):
            myFigure = plt.figure(dpi=200, figsize=(10,10))
            ax1 = plt.axes(projection ='3d')
            ax1.view_init(elev, azim, roll)  
            ax1.scatter(xAxes1,yAxes1,zAxes1,s=0.1,c='green')
            ax1.scatter(xAxes1[0], yAxes1[0], zAxes1[0], s=30, c = 'red')
            plt.title('Elevation: %d°, Azimuth: %d°, Roll: %d°' % (elev, azim, roll))
            # display the plot
            plt.show()
            
        elif(2==POVMode):
            myFigure = plt.figure(dpi=200, figsize=(10,10))
            ax2 = plt.axes(projection ='3d')
            ax2.view_init(elev, azim, roll)  
            ax2.scatter(xAxes2,yAxes2,zAxes2,s=0.1,c='green')
            ax2.scatter(xAxes2[0], yAxes2[0], zAxes2[0], s=30, c = 'red')
            plt.title('Elevation: %d°, Azimuth: %d°, Roll: %d°' % (elev, azim, roll))
            # display the plot
            plt.show()
        
        else:
            myFigure = plt.figure(dpi=200, figsize=(10,10))
            ax = plt.axes(projection ='3d')
            ax.view_init(elev, azim, roll)  
            ax.scatter(xAxes,yAxes,zAxes,s=0.1,c='green')
            ax.scatter(xAxes[0], yAxes[0], zAxes[0], s=30, c = 'red')
            plt.title('Elevation: %d°, Azimuth: %d°, Roll: %d°' % (elev, azim, roll))
            # display the plot
            plt.show()       

# Use for collect only 1 yawDegree
def checkInArray(value):
    idx=0
    if(len(posArray)==0):
         posArray.append(value)
    else:
        for idx in range(len(posArray)):
            if(value== posArray[idx]):
                return 0
        return 1


# Define function process an array 
def processArray():
    idx=0
    for idx in range(4000):
        if(checkInArray(array_2d[0][idx].value1)==1):
            posArray.append(array_2d[0][idx].value1)

# Function to calculate rootMeanSquare of each 
def calculateRootMeanSquare(value):
    idxRow=0
    idxCollum=0
    count=1
    RMS=0
    for idxRow in range(3):
        for idxCollum in range(4000):
            if(array_2d[idxRow][idxCollum].value1== value and array_2d[idxRow][idxCollum].value2 !=0 and array_2d[idxRow][idxCollum].value2 <500):
                RMS= RMS + array_2d[idxRow][idxCollum].value2* array_2d[idxRow][idxCollum].value2
                count= count+1
                break
    return math.sqrt(RMS/count)

                

# Function to call each yawDegree to calculate rootMeanSquare       
def rootMeanSquare():
    idx=0
    RMSResult=0
    for idx in range(len(posArray)):
        RMSResult=calculateRootMeanSquare(posArray[idx])
        xAxes.append(RMSResult*(np.cos(posArray[idx]*3.14/180)))
        yAxes.append(RMSResult*(np.sin(posArray[idx]*3.14/180)))
    

# Define function drawing 2D Mapping
def drawing2D():

    # Create a new figure
    fig, ax = plt.subplots()
    limit_of_data = True
    rowOfArray=0
    collumOfArray=0


    while limit_of_data:
        while arduino.in_waiting == 0:
            pass
        dataPacket = arduino.readline()
        dataPacket  = str(dataPacket, 'utf-8')    
        dataPacket  = dataPacket.strip('\r\n')
        
        if (dataPacket == 'End Data'):
            limit_of_data = False
        elif (dataPacket == 'Round Up'):
            rowOfArray= rowOfArray+1
            collumOfArray=0            
        else:
            splitData = dataPacket.split(',')
            yawDegree= float(splitData[0])
            dist    = float(splitData[2])

            array_2d[rowOfArray][collumOfArray].value1= yawDegree
            array_2d[rowOfArray][collumOfArray].value2= dist

            writeList = [array_2d[rowOfArray][collumOfArray].value1 , array_2d[rowOfArray][collumOfArray].value2 ]
            with open('storeData.csv', 'a', encoding='UTF8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(writeList)
            
            collumOfArray= collumOfArray+1
            print(yawDegree,dist)

            ax.clear

    processArray()
    rootMeanSquare()
    #### Use for test collect yawDegree

    # idxTest=0
    # for idxTest in range(len(posArray)):
    #     print(posArray[idxTest])

    #### End use for test collect yawDegree


    ax.scatter(xAxes,yAxes,s=0.1,c='green')
    ax.scatter(0, 0, s=30, c = 'red')
    ax.set_xlim(-400, 400)
    ax.set_ylim(-400, 400)
    plt.show()

#### Begin Main Thread Program ####

arduino = serial.Serial(
    port='COM7',
    baudrate=115200
)
time.sleep(1)

programWorking= True

while programWorking:
    # Three modes: 0: Stop Lidar || 1: 2D 5 rounds || 2: 3D 90 degree pitch (Test may be 20 degree )
    print("Waiting for input number: ")
    modeWorking = input("Enter a mode working: ") # Taking input from user
    robot_pos_x = float(input("Enter robot x_position: "))
    robot_pos_y = float(input("Enter robot y_position: "))
    robot_pos_z = float(input("Enter robot z_position: "))
    arduino.write(bytes(modeWorking, 'utf-8'))
    time.sleep(0.05)
    if(modeWorking== '0'):
        programWorking= False
    elif (modeWorking== '1'):
        drawing2D()
    elif (modeWorking== '2'):
        drawing3D()
    
#### End Main Thread Program ####