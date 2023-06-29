import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from threading import Thread

fig, ax = plt.subplots()
df_origin = pd.read_csv("storeData.csv")
df = df_origin.copy()

def update_chart(i):
    # Get the latest data
    new_data = df_origin[0+i:8000+i]   

    # # Append the new data to the dataframe
    # df.loc[i] = new_data

    # Clear the previous plot
    ax.cla()

    # Plot the updated data
    ax.plot(new_data['0'], new_data['0.1'])   

    # Optionally set axis limits
    ax.set_xlim(-400, 400)
    ax.set_ylim(-400, 400)   

    # Add labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Real-Time Chart')

def start_animation():
    anim = FuncAnimation(fig, update_chart, interval=5)
    plt.show()

# def animation_thread():
start_animation()

# def print_ok():
#     print("OK")

# try:
#     t1 = Thread(target= animation_thread)
#     t2 = Thread(target= print_ok)
#     t1.start()
#     t2.start()
#     t1.join()
#     t2.join()
# except:
#     print("Error")