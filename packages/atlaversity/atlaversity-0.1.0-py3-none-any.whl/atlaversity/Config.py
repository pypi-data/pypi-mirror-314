import tomllib
from Logging import *

class Config:
    def __init__(self, filename):
        with open(filename, "rb") as configfile:
            data = tomllib.load(configfile)
        if not 'start_turn' in data or not isinstance(data['start_turn'], int):
            raise ValueError(f'Error: No or incorrect "start_turn" config specified in {filename}\nError: Use the form "start_turn = <int>"')
        if not 'factions' in data or not isinstance(data['factions'], list):
            raise ValueError(f'Error: No or incorrect "factions" config specified in {filename}\nError: Use the form "factions = [<int>;, ...]"')
        if 'data_dir' in data and not isinstance(data['data_dir'], str):
            raise ValueError(f'Error: Incorrect "data_dir" config specified in {filename}\nError: Use the form "data_dir = <str>"')
        self.start_turn = data['start_turn']
        self.factions = data['factions']
        if 'data_dir' in data:
            self.data_dir = data['data_dir']
        else:
            self.data_dir = '.'
        if self.data_dir[len(self.data_dir) - 1] != '/':
            self.data_dir += '/'
