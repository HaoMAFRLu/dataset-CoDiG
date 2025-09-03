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
    visualizer.import_track(**track)
    visualizer.import_flatten_track(flatten_track)
    visualizer.import_toc(global_states[0, :],  # x of the solution
                          global_states[1, :],  # y of the solution 
                          global_states[2, :],  # vx of the solution
                          global_states[3, :],  # vy of the solution
                          global_states[4, :],  # yaw of the solution
                          global_states[5, :],  # dyaw of the solution
                          global_states[6, :],  # torque of the solution
                          global_states[7, :])  # steer of the solution
    visualizer.import_local_toc(local_states[0, :],  # local x of the solution
                                local_states[1, :],  # local y of the solution 
                                local_states[2, :],  # local vx of the solution
                                local_states[3, :],  # local vy of the solution
                                local_states[4, :],  # local yaw of the solution
                                local_states[5, :],  # local dyaw of the solution
                                local_states[6, :],  # local torque of the solution
                                local_states[7, :])  # local steer of the solution
    visualizer.plot_xy_plane(dcat=50)
    visualizer.plot_flatten()
    # print the path of roots
    print("Roots path: ", roots)

if __name__ == "__main__":
    file = str(1118)  # the index of the file to visualize
    main(file=file)