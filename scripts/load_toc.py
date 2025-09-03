"""
This script is used to load the results of time optimal control (TOC).
"""
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_loader import DataLoader

def main(file):
    dataloader = DataLoader()
    roots, track, flatten_track, local_states, global_states = dataloader.read_data(file=file)
    print("Roots path: ", roots)

if __name__ == "__main__":
    file = str(1118)  # the index of the file to visualize
    main(file=file)