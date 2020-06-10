# import matplotlib.pyplot as plt
import threading
from itertools import count
import PyQt5

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.figure import Figure

from src.data import Constants
from src.data.Constants import *


# class TickTimeDebugger(FigureCanvas):
#
#     def __init__(self, parent=None):
#         # Init figure as widget
#         self.fig = Figure(figsize=(18, 3))
#         self.fig.set_facecolor(PLOT_WINDOW_BACKGROUND_COLOR)
#         FigureCanvas.__init__(self, self.fig)
#         self.setParent(parent)
#         FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
#         FigureCanvas.updateGeometry(self)
#
#         # Init axes
#         self.ax = None
#         self.create_axes()
#         self.init_default_boundaries()
#         # self.ax.set_title(r"Ця програма будує графік функції $r=a\cdot e^{b\varphi }$", **{'fontname':'Calibri'})
#         self.fig.tight_layout()
#
#         # Init parameters
#         self.a, self.b = None, None
#         self.phi = None
#         self.r = None
#         self.x, self.y = None, None
#         self.range = None
#         self.step = None
#
#         self.grid_on = False
#         self.dots_on = True
#         self.last_point_on = False
#
#         self.lx, self.ly = None, None
#         self.rx, self.ry = None, None
#
#         # Plots
#         self.spiral = None
#         self.ldot, self.rdot = None, None
#
#     def create_axes(self):
#         # Creating axes
#         self.ax = self.fig.add_subplot("111")
#         self.ax.set_aspect('equal', adjustable='box')
#         self.ax.set_facecolor(PLOT_WINDOW_BACKGROUND_COLOR)
#
#         # Moving the origin (0,0) to the center of the screen
#         # self.ax.spines['top'].set_color('none')
#         # self.ax.spines['bottom'].set_position('zero')
#         # self.ax.spines['left'].set_position('zero')
#         # self.ax.spines['right'].set_color('none')
#
#         for tick_x, tick_y in zip(self.ax.xaxis.get_major_ticks(), self.ax.yaxis.get_major_ticks()):
#             tick_x.label.set_fontsize(PLOTWINDOW_TEXT_SIZE)
#             tick_y.label.set_fontsize(PLOTWINDOW_TEXT_SIZE)
#
#     def init_default_boundaries(self):
#         # Setting up boundaries
#         xy_lim = INITIAL_XY_LIMITS
#         self.ax.set_xlim([-xy_lim, xy_lim])
#         self.ax.set_ylim([-xy_lim, xy_lim])
#
#     def show_grid(self, toggle=False):
#         if toggle:
#             self.grid_on = not self.grid_on
#         self.ax.grid(self.grid_on)
#         self.draw()
#
#     def update_boundaries(self):
#         # Calculating spiral graph boundaries
#         self.abs_max = max(max(self.x), max(self.y), -min(self.x), -min(self.y))
#         if self.abs_max >= 1:
#             self.xy_lim = self.abs_max * PLOT_SCALING_LIMITS_FACTOR + 1
#         elif 0 < self.abs_max < 1:
#             self.xy_lim = self.abs_max * PLOT_SCALING_LIMITS_FACTOR * PLOT_SCALING_LIMITS_UNIT_FACTOR
#         elif self.abs_max == 0:
#             self.xy_lim = INITIAL_XY_LIMITS
#         elif 0 > self.abs_max > -1:
#             self.xy_lim = -self.abs_max * PLOT_SCALING_LIMITS_FACTOR * PLOT_SCALING_LIMITS_UNIT_FACTOR
#         else:
#             self.xy_lim = -self.abs_max * PLOT_SCALING_LIMITS_FACTOR + 1
#
#         # Setting up spiral graph boundaries
#         self.ax.set_xlim([-self.xy_lim, self.xy_lim])
#         self.ax.set_ylim([-self.xy_lim, self.xy_lim])
#
#     def update_spiral_plot(self):
#         if self.range[0] != self.range[1]:
#             self.spiral = self.ax.plot(self.x, self.y, color='b', label="Логарифмічна спіраль", zorder=0)
#             self.show_dots()
#         else:
#             self.spiral = self.ax.scatter(self.x, self.y, color='b', label="Логарифмічна спіраль", zorder=0)
#         self.ax.legend(prop={'size': 9})
#
#         self.show_grid()
#
#     def plot_spiral(self, a=1, b=0.1, range=[0, 4 * np.pi], step=DEFAULT_PLOT_PRECISION):
#         # Deleting previous axes and creating new one
#         self.ax.remove()
#         self.create_axes()
#         self.range = range
#         self.a, self.b = a, b
#         self.step = step
#
#         # Setting up polar coordinates needed for further calculations
#         if range[0] != range[1]:
#             self.phi = np.arange(range[0], range[1], step)
#         else:
#             self.phi = np.array([range[0], range[1]])
#         self.r = a * np.e ** (b * self.phi)
#
#         # and converting them into cartesian coordinates
#         self.x = self.r * (np.cos(self.phi))
#         self.y = self.r * (np.sin(self.phi))
#
#         self.update_dots()
#
#         self.update_boundaries()
#         self.update_spiral_plot()
#         self.force_last_point(is_plotted_first_time=True)


class TickTimeDebugger(object):
    """This class plots graphs of execution time, tick time, etc.
    How to use: call .run() in init and then call .update() in main loop"""

    def __init__(self):
        # [[%actual data%], (%max number of values%)]
        self.max_displayed_t = Constants.GLOBAL_TICK_RATE * 10
        self.data = {"physics_data": [0 for i in range(self.max_displayed_t)],
                     "ai_data": [0 for i in range(self.max_displayed_t)],
                     "render_data": [0 for i in range(self.max_displayed_t)],
                     "tick_time": [0 for i in range(self.max_displayed_t)]}
        self.x = [i for i in range(self.max_displayed_t)]
        self.index = count()
        self.data_updated = False

    def delete_overflowed_data(self):
        for datalist in list(self.data.values()):
            while len(datalist) >= self.max_displayed_t:
                datalist.pop(0)

    def update(self, physics_exec_time, ai_exec_time, render_exec_time, tick_time=0):
        self.delete_overflowed_data()

        # update y
        self.data["physics_data"].append(physics_exec_time)
        self.data["ai_data"].append(ai_exec_time)
        self.data["render_data"].append(render_exec_time)
        self.data["tick_time"].append(tick_time)

        self.data_updated = True

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
        #matplotlib.use('QT5Agg')
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1)
        self.fig.set_size_inches(12,3)
        self.fig.tight_layout()
        self.fig.canvas.manager.window.wm_geometry("+%d+%d" % (0, 0))
        self.ax1.set_facecolor(PLOT_WINDOW_BACKGROUND_COLOR)
        self.ax2.set_facecolor(PLOT_WINDOW_BACKGROUND_COLOR)

        self.ax1.set_ylim([0, 1])
        self.ax2.set_ylim([0, 1])

        self.ax1.set_ylabel("Execution time")
        self.ax2.set_ylabel("Tick time")

        #self.fig.draw()

        ani = FuncAnimation(self.fig, lambda x: self._animate(), interval= 1 / Constants.GLOBAL_TICK_RATE * 1000)
        # while True:
        #     print("INSIDE THREAD-2 WHILE LOOP")
        #     if self.data_updated:
        #         self._animate()
        #         self.data_updated = False
        plt.show()

    def run(self):
        plot = threading.Thread(target=self._run, args=())
        plot.daemon = True  # Daemonize thread
        plot.start()
