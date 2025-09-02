"""
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from src.utils import *

class Visualizer():
    """A class for visualizing the toc solutions."""
    def __init__(self):
        """Some constants for visualization.
        """
        self.car_dim = 0.07 /np.sqrt(2)
        self.corners = self.get_corners(self.car_dim, self.car_dim)
        self.x_min, self.x_max = -2.0, 2.0
        self.y_min, self.y_max = -2.0, 2.0
        self.yaw_min, self.yaw_max = -np.inf, np.inf
        self.vx_min, self.vx_max = 0.0, 5.0
        self.vy_min, self.vy_max = -2.0, 2.0
        self.dyaw_min, self.dyaw_max = -10.0, 10.0
        self.theta_min, self.theta_max =-1.0, np.inf
        self.torque_min, self.torque_max =  -1.0, 1.0
        self.steer_min, self.steer_max = -0.4, 0.4
        self.T_s_min, self.T_s_max = 0.0, 1.0
        self.dtheta_min, self.dtheta_max = 0.0, np.inf
        self.dtorque_min, self.dtorque_max = -5.0, 5.0
        self.dsteer_min, self.dsteer_max = -4.0, 4.0
        self.dT_s_min, self.dT_s_max = -0.02, 0.02
    
    @staticmethod
    def get_corners(l: float, w: float):
        """Get the corners of the car for visualization.
        """
        return np.array([[ l,  w],
                         [ l, -w],
                         [-l, -w],
                         [-l,  w]])
    
    def import_map(self, 
                   TRACK_WIDTH,
                   x_original, 
                   y_original, 
                   x_rate, 
                   y_rate,
                   obstacles) -> None:
        """Import the map information, including track path
        and obstacles.
        """
        self.TRACK_WIDTH = TRACK_WIDTH
        self.x_original  = x_original
        self.y_original  = y_original
        self.x_rate      = x_rate
        self.y_rate      = y_rate
        self.obstacles   = obstacles
    
    # def import_local_toc_solution(self,
    #                               x, 
    #                               y, 
    #                               yaw,
    #                               vx, 
    #                               vy, 
    #                               dyaw, 
    #                               theta, 
    #                               torque, 
    #                               steer, 
    #                               Ts,
    #                               dtheta, 
    #                               dtorque, 
    #                               dsteer, 
    #                               dTs) -> None:
    #     """Import the localized toc solutions.
    #     """
    #     self.local_idx_list = idx_list
    #     self.local_x = x
    #     self.local_y = y
    #     self.local_yaw = yaw
    #     self.local_vx = vx
    #     self.local_vy = vy
    #     self.local_dyaw = dyaw
    #     self.local_theta = theta
    #     self.local_torque = torque
    #     self.local_steer = steer
    #     self.local_Ts = Ts
    #     self.local_dtheta = dtheta
    #     self.local_dtorque = dtorque
    #     self.local_dsteer = dsteer
    #     self.local_dTs = dTs

    def import_flatten_map(self, flatten_map):
        """Import the flatten map
        """
        self.flatten_map = flatten_map

    def import_toc_solution(self, 
                            x, 
                            y, 
                            yaw,
                            dyaw,
                            vx, 
                            vy, 
                            torque, 
                            steer):
        """Import the toc solutions.
        """
        self.x = x
        self.y = y
        self.yaw = yaw
        self.vx = vx
        self.vy = vy
        self.dyaw = dyaw
        self.torque = torque
        self.steer = steer
    
    @staticmethod
    def plot_track_path(ax: Axes, 
                        x: np.ndarray, 
                        y: np.ndarray,
                        x_rate: np.ndarray, 
                        y_rate: np.ndarray, 
                        TRACK_WIDTH: float) -> None:
        """Plot the track path without obstacles
        """
        # plot the start line
        ax.vlines(x[0], ymin=y[0]-TRACK_WIDTH/2, ymax=y[0]+TRACK_WIDTH/2, colors='g', linestyles='--', linewidth=1.5, label='Start Line')
        ax.plot(x, y, "b--", label="Nominal Track", linewidth=0.5)
        ax.plot(
            x + y_rate * TRACK_WIDTH / 2,
            y - x_rate * TRACK_WIDTH / 2,
            "k-", linewidth=0.5
        )
        ax.plot(
            x - y_rate * TRACK_WIDTH / 2,
            y + x_rate * TRACK_WIDTH / 2,
            "k-", linewidth=0.5
        )

    @staticmethod
    def plot_one_obstacle(ax: Axes, 
                          obs: np.ndarray) -> None:
        """Plot one obstacle.
        """
        # ax.scatter(obs[:, 0], obs[:, 1], color='saddlebrown', s=0.01)  # 'saddlebrown' 
        ax.plot(obs[:, 0], obs[:, 1], color='saddlebrown', linewidth=0.30)  # 'saddlebrown' 

    def plot_obstacles(self, ax: Axes, 
                       obstacles: list) -> None:
        """Plot all the obstacles.
        """
        for obs in obstacles:
            self.plot_one_obstacle(ax, obs)

    def init_plot(self):
        """Initalize the plot for xy plane.
        """
        self.fig_xy_plane, self.ax = plt.subplots(1, 1, figsize=(8, 8))
        set_axes_format(self.ax, r'x', r'y')
        set_axes_equal_2d(self.ax)

    @staticmethod
    def plot_center_line(ax: Axes, x, y):
        ax.scatter(x, y, color='red', s=5)

    @staticmethod
    def get_rotation(yaw):
        return np.array([[np.cos(yaw), -np.sin(yaw)],
                         [np.sin(yaw),  np.cos(yaw)]])
    
    @staticmethod
    def _plot_car(ax: Axes, 
                  x: float, 
                  y: float, 
                  corners: list, 
                  arrow_x: list, 
                  arrow_y: list,
                  is_heading: bool=False) -> None:
        """Plot one car at (x, y) with given corners and heading arrow.
        """
        ax.scatter(x, y, color='gray', s=1)
        if is_heading:
            ax.plot(*np.append(corners, [corners[0]], axis=0).T, color='gray')
            ax.arrow(x, 
                     y, 
                     arrow_x - x, 
                     arrow_y - y, 
                     head_width=0.05,
                     head_length=0.1,
                     length_includes_head=False, 
                     fc='gray',
                     ec='gray',
                     linewidth=1.5,
                     alpha=0.8)

    def plot_car(self, 
                 ax: Axes, 
                 x: np.ndarray, 
                 y: np.ndarray, 
                 yaw: np.ndarray) -> None:
        """Plot the car along the trajectory.
        """
        for _x, _y, _yaw in zip(x, y, yaw):
            R = self.get_rotation(_yaw)
            corners = np.dot(self.corners, R.T) + np.array([_x, _y])
            arrow_length = self.car_dim + 0.01  
            arrow_x = _x + arrow_length * np.cos(_yaw)
            arrow_y = _y + arrow_length * np.sin(_yaw)
            self._plot_car(ax, _x, _y, corners, arrow_x, arrow_y)

    def plot_xy_plane(self,
                      is_track: bool=True,
                      is_obs: bool=True,
                      is_center_line: bool=True,
                      dline: int=10,
                      is_car: bool=True,
                      is_heading: bool=True,
                      dcat: int=10) -> None:
        self.init_plot()
        if is_track:
            self.plot_track_path(self.ax, 
                                 self.x_original, 
                                 self.y_original, 
                                 self.x_rate, 
                                 self.y_rate, 
                                 self.TRACK_WIDTH)
        if is_obs:
            self.plot_obstacles(self.ax, self.obstacles)
        if is_center_line:
            self.plot_center_line(self.ax, self.x[::dline], self.y[::dline])
        if is_car:
            self.plot_car(self.ax, self.x[::dcat], self.y[::dcat], self.yaw[::dcat], is_heading)
        plt.show()