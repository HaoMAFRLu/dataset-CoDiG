"""The dataloader module for loading and processing datasets.
"""
import pickle

from src.utils import *

root = get_parent_path(lvl=1)

class DataLoader:
    """
    """
    def __init__(self): 
        self.path = os.path.join(root, 'data', 'TOC')
        # list all files in the folder
        self.files = os.listdir(self.path)
    
    def load_data(self, path: str, is_load_states: bool=False):
        """Read data of the toc root solution.
        """
        with open(path, 'rb') as f:
            data = pickle.load(f)
        
        if is_load_states is False:
            roots = data['roots']
            track = data['map']
            flatten_track = data['flatten_map']
            # find the root solution and load the states
            states = self.load_data(os.path.join(self.path, roots[0]), is_load_states=True)
            return roots, track, flatten_track, states['local_states'], states['global_states']
        else:
            return data['states']

    def read_data(self, file: str):
        """Read data from file, including the 
        track information and the solution.
        """
        if file not in self.files:
            raise ValueError(f"File {file} not found in {self.path}.")
        else:
            return self.load_data(os.path.join(self.path, file))
