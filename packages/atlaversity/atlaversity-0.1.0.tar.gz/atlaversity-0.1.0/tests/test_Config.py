import pytest
import unittest.mock as mock

from src.atlaversity.Config import Config

def test_missing_file():
    with pytest.raises(FileNotFoundError):
        Config('invalid')

def test_missing_start_turn():
    with mock.patch('builtins.open', mock.mock_open(read_data=b'factions = [20, 34, 39, 47, 62, 64, 80]')):
        with pytest.raises(ValueError) as valerror:
            Config('filename')
        assert str(valerror.value) == f'Error: No or incorrect "start_turn" config specified in filename\nError: Use the form "start_turn = <int>"'

def test_incorrect_start_turn():
    with mock.patch('builtins.open', mock.mock_open(read_data=b'start_turn=\'1\'\nfactions = [20, 34, 39, 47, 62, 64, 80]')):
        with pytest.raises(ValueError) as valerror:
            Config('filename')
        assert str(valerror.value) == f'Error: No or incorrect "start_turn" config specified in filename\nError: Use the form "start_turn = <int>"'

def test_missing_factions():
    with mock.patch('builtins.open', mock.mock_open(read_data=b'start_turn=1')):
        with pytest.raises(ValueError) as valerror:
            Config('filename')
        assert str(valerror.value) == f'Error: No or incorrect "factions" config specified in filename\nError: Use the form "factions = [<int>;, ...]"'

def test_incorrect_factions():
    with mock.patch('builtins.open', mock.mock_open(read_data=b'start_turn=1\nfactions = 62')):
        with pytest.raises(ValueError) as valerror:
            Config('filename')
        assert str(valerror.value) == f'Error: No or incorrect "factions" config specified in filename\nError: Use the form "factions = [<int>;, ...]"'

def test_missing_data_dir():
    with mock.patch('builtins.open', mock.mock_open(read_data=b'start_turn=1\nfactions = [20, 34, 39, 47, 62, 64, 80]')):
        c = Config('filename')
        assert c.data_dir == './'

def test_incorrect_data_dir():
    with mock.patch('builtins.open', mock.mock_open(read_data=b'start_turn=1\nfactions = [20, 34, 39, 47, 62, 64, 80]\ndata_dir=1')):
        with pytest.raises(ValueError) as valerror:
            Config('filename')
        assert str(valerror.value) == f'Error: Incorrect "data_dir" config specified in filename\nError: Use the form "data_dir = <str>"'

def test_config_ok():
    with mock.patch('builtins.open', mock.mock_open(read_data=b'start_turn=1\nfactions = [20, 34, 39, 47, 62, 64, 80]\ndata_dir=\'data\'')):
        c = Config('filename')
        assert c.start_turn == 1
        assert c.factions == [20, 34, 39, 47, 62, 64, 80]
        assert c.data_dir == 'data/'
