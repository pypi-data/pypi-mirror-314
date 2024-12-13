import pytest
import unittest.mock as mock

from src.atlaversity.Game import Game
from src.atlaversity.Config import Config
import src.atlaversity.Config

def test_read_mages():
    with mock.patch('builtins.open', mock.mock_open(read_data=b'start_turn=1\nfactions = [20, 34, 39, 47, 62, 64, 80]\ndata_dir=\'data\'')):
        config = Config('file')
    game = Game(config)
    data ='''Skill,1 One,2 Two,3 Three
    FORC,30,0,0
    PATT,0,60,0
    SPIR,0,0,90'''
    with mock.patch('builtins.open', mock.mock_open(read_data=data)) as m:
        game.read_mages_from_file(62, 10)
        m.assert_called_once_with('data/mages6210.csv', 'r')
    assert len(game.all_mages) == 3
    assert game.all_mages[0].id == 1
    assert game.all_mages[0].name == 'One'
    assert game.all_mages[1].id == 2
    assert game.all_mages[1].name == 'Two'
    assert game.all_mages[2].id == 3
    assert game.all_mages[2].name == 'Three'
    assert game.all_mages[0].get_skill_level_and_days('FORC') == '1(30)'
    assert game.all_mages[1].get_skill_level_and_days('PATT') == '1(60)'
    assert game.all_mages[2].get_skill_level_and_days('SPIR') == '2(90)'
    assert game.all_mages[0].get_skill_level_and_days('PATT') == '0(0)'

def test_read_mages_multiple():
    with mock.patch('builtins.open', mock.mock_open(read_data=b'start_turn=1\nfactions = [20, 34, 39, 47, 62, 64, 80]\ndata_dir=\'data\'')):
        config = Config('file')
    game = Game(config)
    data1 ='''Skill,1 One,2 Two
'''
    data2 ='''Skill,3 Three,4 Four
'''
    with mock.patch('builtins.open', mock.mock_open(read_data=data1)) as m:
        game.read_mages_from_file(62, 10)
        m.assert_called_once_with('data/mages6210.csv', 'r')
    with mock.patch('builtins.open', mock.mock_open(read_data=data2)) as m:
        game.read_mages_from_file(64, 10)
        m.assert_called_once_with('data/mages6410.csv', 'r')
    assert len(game.all_mages) == 4
    assert game.all_mages[0].id == 1
    assert game.all_mages[1].id == 2
    assert game.all_mages[2].id == 3
    assert game.all_mages[3].id == 4

def test_add_turn_one_mage():
    with mock.patch('builtins.open', mock.mock_open(read_data=b'start_turn=1\nfactions = [20, 34, 39, 47, 62, 64, 80]\ndata_dir=\'data\'')):
        config = Config('file')
    game = Game(config)
    data ='''Skill,1 One
'''
    with mock.patch('builtins.open', mock.mock_open(read_data=data)) as m:
        game.read_mages_from_file(62, 11)
        m.assert_called_once_with('data/mages6211.csv', 'r')
    assert len(game.all_turns) == 0
    game.add_new_turn()
    assert len(game.all_turns) == 1
    assert len(game.all_turns[0].start_mages) == 1
    assert len(game.all_turns[0].end_mages) == 1
    assert game.all_turns[0].study[0] == ''

def test_add_turn_two_mages():
    with mock.patch('builtins.open', mock.mock_open(read_data=b'start_turn=1\nfactions = [20, 34, 39, 47, 62, 64, 80]\ndata_dir=\'data\'')):
        config = Config('file')
    game = Game(config)
    data ='''Skill,1 One,2 Two
'''
    with mock.patch('builtins.open', mock.mock_open(read_data=data)) as m:
        game.read_mages_from_file(62, 10)
        m.assert_called_once_with('data/mages6210.csv', 'r')
    assert len(game.all_turns) == 0
    game.add_new_turn()
    assert len(game.all_turns) == 1
    assert len(game.all_turns[0].start_mages) == 2
    assert len(game.all_turns[0].end_mages) == 2
    assert game.all_turns[0].study[0] == ''
    assert game.all_turns[0].study[1] == ''

def test_read_and_write_plan():
    with mock.patch('builtins.open', mock.mock_open(read_data=b'start_turn=1\nfactions = [20, 34, 39, 47, 62, 64, 80]\ndata_dir=\'data\'')):
        config = Config('file')
    game = Game(config)
    data ='''Skill,1 One,2 Two
'''
    with mock.patch('builtins.open', mock.mock_open(read_data=data)) as m:
        game.read_mages_from_file(62, 10)
        m.assert_called_once_with('data/mages6210.csv', 'r')
    plandata = '''1,2
#One,Two
#DRAG,ARTI
FORC,PATT
#comment
PATT,FORC
#another comment
'''
    with mock.patch('builtins.open', mock.mock_open(read_data=plandata)):
        game.read_plan_from_file('plan', 10)
    assert game.all_turns[0].num == 10
    assert game.all_turns[1].num == 11
    assert game.all_turns[0].study == ['FORC','PATT']
    assert game.all_turns[1].study == ['PATT','FORC']
    with mock.patch('builtins.open') as m:
        game.save_to_file('plan')
    write_data = ''
    for c in m.mock_calls:
        if c[0] == '().write':
            write_data += c[1][0]
    assert write_data == plandata
