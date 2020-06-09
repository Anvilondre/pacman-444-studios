#import matplotlib.pyplot as plt
import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class TickTimeDebugger(object):

    def __init__(self, desired_tick_time):
        self.desired_tick_time = desired_tick_time
        # [[%actual data%], (%max number of values%)]
        self.data = {"physics_data": [], "ai_data": [], "render_data": []}
        self.data_boundaries = {"physics_data": 20, "ai_data": 10, "render_data": 5}
        # self.physics_data = []
        # self.ai_data = []
        # self.render_data = []

    def update_data(self):
        pass

    def update(self, physics_tick_time, ai_tick_time, render_tick_time):
        pass

    def show(self):
        plt.style.use('fivethirtyeight')

        x_vals = []
        y_vals = []

        index = count()

        def animate(i):
            data = pd.read_csv('data.csv')
            x = data['x_value']
            y1 = data['total_1']
            y2 = data['total_2']

            plt.cla()

            plt.plot(x, y1, label='Channel 1')
            plt.plot(x, y2, label='Channel 2')

            plt.legend(loc='upper left')
            plt.tight_layout()

        ani = FuncAnimation(plt.gcf(), animate, interval=1000)

        plt.tight_layout()
        plt.show()


db = TickTimeDebugger(0.017)
db.show()