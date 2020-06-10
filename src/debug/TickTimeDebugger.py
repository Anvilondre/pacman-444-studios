import threading
from itertools import count

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from src.data import Constants


class TickTimeDebugger(object):
    """This class plots graphs of execution time, tick time, etc.
    How to use: call .run() in init and then call .update() in main loop"""

    def __init__(self):
        self.max_displayed_t = Constants.GLOBAL_TICK_RATE * 10
        self.data = {"physics_execution_time": [0 for i in range(self.max_displayed_t)],
                     "ai_execution_time": [0 for i in range(self.max_displayed_t)],
                     "render_execution_time": [0 for i in range(self.max_displayed_t)],
                     "tick_time": [0 for i in range(self.max_displayed_t)]}
        self.x = [i for i in range(self.max_displayed_t)]
        self.index = count()

    def delete_overflowed_data(self):
        for datalist in list(self.data.values()):
            while len(datalist) >= self.max_displayed_t:
                datalist.pop(0)

    def update(self, physics_exec_time, ai_exec_time, render_exec_time, tick_time=0):
        self.delete_overflowed_data()

        # update y
        self.data["physics_execution_time"].append(physics_exec_time)
        self.data["ai_execution_time"].append(ai_exec_time)
        self.data["render_execution_time"].append(render_exec_time)
        self.data["tick_time"].append(tick_time)

    def _animate(self):
        self.ax1.cla()
        self.ax2.cla()

        for i_key in range(len(self.data.keys())):
            if i_key <= 2:
                self.ax1.plot(self.x, self.data[list(self.data.keys())[i_key]],
                                          label=list(self.data.keys())[i_key])
            if i_key >= 3:
                self.ax2.plot(self.x, self.data[list(self.data.keys())[i_key]],
                                          label=list(self.data.keys())[i_key])

        self.ax1.legend(loc='upper left')
        self.ax2.legend(loc='upper left')

    def _run(self):
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1)
        self.fig.set_size_inches(12,3)
        self.fig.tight_layout()
        self.fig.canvas.manager.window.wm_geometry("+%d+%d" % (0, 0))
        self.ax1.set_facecolor(Constants.PLOT_WINDOW_BACKGROUND_COLOR)
        self.ax2.set_facecolor(Constants.PLOT_WINDOW_BACKGROUND_COLOR)

        self.ax1.set_ylim([0, 1])
        self.ax2.set_ylim([0, 1])

        self.ax1.set_ylabel("Execution time")
        self.ax2.set_ylabel("Tick time")

        ani = FuncAnimation(self.fig, lambda x: self._animate(), interval= 1 / Constants.GLOBAL_TICK_RATE * 1000)

        plt.show()

    def run(self):
        plot = threading.Thread(target=self._run, args=())
        plot.daemon = True  # Daemonize thread
        plot.start()
