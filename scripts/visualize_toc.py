"""
This script is used to visualize the results of time optimal control (TOC).
"""
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_loader import DataLoader
from src.visualizer import Visualizer

def main(file):
    dataloader = DataLoader()
    visualizer = Visualizer() 
    roots, track, flatten_track, local_states, global_states = dataloader.read_data(file=file)
    visualizer.import_map(**track)
    visualizer.import_toc_solution(global_states[0, :],  # x of the solution
                                   global_states[1, :],  # y of the solution 
                                   global_states[2, :],  # yaw of the solution
                                   global_states[3, :],  # dyaw of the solution
                                   global_states[4, :],  # vx of the solution
                                   global_states[5, :],  # vy of the solution
                                   global_states[6, :],  # torque of the solution
                                   global_states[7, :])  # steer of the solution
    visualizer.init_plot()
    visualizer.plot_xy_plane(obstacle=True)

if __name__ == "__main__":
    file = str(9686)  # the index of the file to visualize
    main(file=file)