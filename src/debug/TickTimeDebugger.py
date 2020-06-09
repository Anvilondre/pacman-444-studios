#import matplotlib.pyplot as plt
import threading

import random
from itertools import count
from time import sleep

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from src.data import Constants

class TickTimeDebugger(object):
    """How to use: call .run() in init and then call .update() in main loop"""

    def __init__(self):
        # [[%actual data%], (%max number of values%)]
        self.max_displayed_t = Constants.GLOBAL_TICK_RATE*10
        self.data = {"physics_data": [0 for i in range(self.max_displayed_t)],
                     "ai_data": [0 for i in range(self.max_displayed_t)],
                     "render_data": [0 for i in range(self.max_displayed_t)]}
        self.x = [i for i in range(self.max_displayed_t)]
        self.index = count()


    def delete_overflowed_data(self):
        # while len(self.x) >= self.max_displayed_t:
        #     self.x.pop()

        for datalist in list(self.data.values()):
            while len(datalist) >= self.max_displayed_t:
                datalist.pop(0)

    def update(self, physics_exec_time, ai_exec_time, render_exec_time):
        self.delete_overflowed_data()

        # update x
        #self.x.append(next(self.index))

        # update y
        self.data["physics_data"].append(physics_exec_time)
        self.data["ai_data"].append(ai_exec_time)
        self.data["render_data"].append(render_exec_time)



    def _run(self):
        plt.figure(figsize=(15, 3))
        plt.style.use('fivethirtyeight')
        plt.ylabel("Execution time")

        def animate(i):
            plt.cla()

            for item in self.data.items():
                plt.plot(self.x, item[1], label=item[0])
                plt.yscale('log')

            plt.legend(loc='upper left')
            plt.tight_layout()

        ani = FuncAnimation(plt.gcf(), animate, interval=1/Constants.GLOBAL_TICK_RATE*1000)

        plt.tight_layout()
        plt.show()

    def run(self):
        plot = threading.Thread(target=self._run, args=())
        plot.daemon = True  # Daemonize thread
        plot.start()