import enum
import threading
from itertools import count

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation

from src.data import Constants


class Modes(enum.Enum):
    LiveView = 0
    Store = 1


class TickTimeDebugger(object):
    """This class plots graphs of execution time, tick time, etc.
    How to use: call .run() in init and then call .update() in main loop"""

    def __init__(self, mode=Modes.LiveView):
        matplotlib.use('TKAgg')
        self.mode = mode
        self.max_displayed_x = Constants.GLOBAL_TICK_RATE * 10
        self.index = count()

        if self.mode == Modes.LiveView:

            # Stores all received data
            self.displayed_data = {"physics_execution_time": [0 for i in range(self.max_displayed_x)],
                         "ai_execution_time": [0 for i in range(self.max_displayed_x)],
                         "render_execution_time": [0 for i in range(self.max_displayed_x)],
                         "tick_time": [0 for i in range(self.max_displayed_x)]}
            self.displayed_x = [next(self.index) for i in range(self.max_displayed_x)]

            # Stores only necessary for displaying amount of data (len<max_displayed_x)
            self.data = {"physics_execution_time": [],
                                   "ai_execution_time": [],
                                   "render_execution_time": [],
                                   "tick_time": []}
            self.x = []

        else:
            # Stores all received data
            self.data = {"physics_execution_time": [],
                         "ai_execution_time": [],
                         "render_execution_time": [],
                         "tick_time": []}
            self.x = []

    def delete_overflowed_data(self):
        for datalist in list(self.displayed_data.values()):
            while len(datalist) >= self.max_displayed_x:
                datalist.pop(0)

    def update(self, physics_exec_time, ai_exec_time, render_exec_time, tick_time=0):
        if self.mode == Modes.LiveView:
            self.delete_overflowed_data()

        # update x
        self.x.append(next(self.index))

        # update y
        self.data["physics_execution_time"].append(physics_exec_time)
        self.data["ai_execution_time"].append(ai_exec_time)
        self.data["render_execution_time"].append(render_exec_time)
        self.data["tick_time"].append(tick_time)

        if self.mode == Modes.LiveView:
            self.displayed_data["physics_execution_time"].append(physics_exec_time)
            self.displayed_data["ai_execution_time"].append(ai_exec_time)
            self.displayed_data["render_execution_time"].append(render_exec_time)
            self.displayed_data["tick_time"].append(tick_time)

    def save_as_image(self, path=Constants.DEFAULT_GRAPH_SAVEPATH):
        if path:
            self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1)
            self.fig.set_size_inches(50, 10)
            self.fig.tight_layout()
            self.fig.canvas.manager.window.wm_geometry("+%d+%d" % (0, 0))
            self.ax1.set_facecolor("#eeeeee")
            self.ax2.set_facecolor("#eeeeee")

            self.ax1.set_ylim([0, 1.33 * 1/Constants.GLOBAL_TICK_RATE])
            self.ax2.set_ylim([0, 2 * 1/Constants.GLOBAL_TICK_RATE])

            self.ax1.set_ylabel("Execution time")
            self.ax2.set_ylabel("Tick time")

            for i_key in range(len(self.data.keys())):
                if i_key <= 2:
                    self.ax1.plot(self.x, self.data[list(self.data.keys())[i_key]],
                                  label=list(self.data.keys())[i_key])
                if i_key >= 3:
                    self.ax2.plot(self.x, self.data[list(self.data.keys())[i_key]],
                                  label=list(self.data.keys())[i_key])

            self.ax1.legend(loc='upper left')
            self.ax2.legend(loc='upper left')

            self.fig.savefig(path, dpi=200, facecolor="#eeeeee", edgecolor="#eeeeee",
                                                             orientation='landscape', papertype=None, format=None,
                                                             transparent=False, bbox_inches='tight', pad_inches=0.2,
                                                             metadata=None, figsize = (100, 20))
            pyplot.close(self.fig)

    def _animate(self):
        self.ax1.cla()
        self.ax2.cla()

        for i_key in range(len(self.displayed_data.keys())):
            if i_key <= 2:
                self.ax1.plot(self.displayed_x, self.displayed_data[list(self.displayed_data.keys())[i_key]],
                              label=list(self.displayed_data.keys())[i_key])
            if i_key >= 3:
                self.ax2.plot(self.displayed_x, self.displayed_data[list(self.displayed_data.keys())[i_key]],
                              label=list(self.displayed_data.keys())[i_key])

        self.ax1.legend(loc='upper left')
        self.ax2.legend(loc='upper left')

    def _run(self):
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1)
        self.fig.set_size_inches(12, 3)
        self.fig.tight_layout()
        self.fig.canvas.manager.window.wm_geometry("+%d+%d" % (0, 0))
        self.ax1.set_facecolor("#eeeeee")
        self.ax2.set_facecolor("#eeeeee")

        self.ax1.set_ylim([0, 1])
        self.ax2.set_ylim([0, 1])

        self.ax1.set_ylabel("Execution time")
        self.ax2.set_ylabel("Tick time")

        ani = FuncAnimation(self.fig, lambda x: self._animate(), interval=1 / Constants.GLOBAL_TICK_RATE * 1000)

        plt.show()

    def run(self):
        if self.mode == Modes.LiveView:
            plot = threading.Thread(target=self._run, args=())
            plot.daemon = True  # Daemonize thread
            plot.start()
