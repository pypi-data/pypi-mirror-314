import pytest

from src.atlaversity.Turn import *

@pytest.fixture
def mages():
    mages = []
    for i in range(12):
        mages.append(Mage(100 + i, f'mage{100 + i}'))
    return mages

def test_simple_turn(mages):
    turn = Turn(mages, 'FORC,FORC,FORC,FORC,FORC,FORC,FORC,FORC,FORC,FORC,FORC,FORC', 10)
    assert turn.num == 10
    for mi,mage in enumerate(turn.end_mages):
        assert mage.get_skill_days('FORC') == 30
        assert turn.is_teaching(mi) == False
        assert turn.get_taught_by_num(mage) == -1
        assert turn.is_taught(mi) == False
        assert turn.get_teacher_num_by_mage(mage) == -1

def test_teaching_no_students(mages):
    turn = Turn(mages, 'FORC,TEACH,FORC,FORC,FORC,FORC,FORC,FORC,FORC,FORC,FORC,FORC', 10)
    for mi,(s_mage,e_mage) in enumerate(zip(turn.start_mages, turn.end_mages)):
        assert turn.get_taught_by_num(s_mage) == -1
        assert turn.is_taught(mi) == False
        if mi == 1:
            assert e_mage.get_skill_days('FORC') == 0
            assert turn.is_teaching(mi) == True
            assert turn.get_teacher_num_by_mage(s_mage) == 0
        else:
            assert e_mage.get_skill_days('FORC') == 30
            assert turn.is_teaching(mi) == False
            assert turn.get_teacher_num_by_mage(e_mage) == -1

def test_teaching_ten_students(mages):
    mages[1].train('FORC', 30)
    turn = Turn(mages, 'FORC,TEACH,FORC,FORC,FORC,FORC,FORC,FORC,FORC,FORC,FORC,PATT', 10)
    for mi,(s_mage,e_mage) in enumerate(zip(turn.start_mages, turn.end_mages)):
        if mi == 1:
            assert e_mage.get_skill_days('FORC') == 30
            assert turn.is_teaching(mi) == True
            assert turn.get_teacher_num_by_mage(s_mage) == 0
            assert turn.get_taught_by_num(s_mage) == -1
            assert turn.is_taught(s_mage) == False
        elif mi == 11:
            assert e_mage.get_skill_days('PATT') == 30
            assert turn.is_teaching(mi) == False
            assert turn.get_teacher_num_by_mage(e_mage) == -1
            assert turn.get_taught_by_num(s_mage) == -1
            assert turn.is_taught(s_mage) == False
        else:
            assert e_mage.get_skill_days('FORC') == 60
            assert turn.is_teaching(mi) == False
            assert turn.get_teacher_num_by_mage(e_mage) == -1
            assert turn.get_taught_by_num(s_mage) == 0
            assert turn.is_taught(s_mage) == True

def test_teaching_with_no_teach(mages):
    mages[1].train('FORC', 30)
    expected_students = [mages[2], mages[4], mages[5], mages[6], mages[7], mages[8], mages[9], mages[10]]
    turn = Turn(mages, 'FORC,TEACH-100-103,FORC,FORC,FORC,FORC,FORC,FORC,FORC,FORC,FORC,PATT', 10)
    for mi,(s_mage,e_mage) in enumerate(zip(turn.start_mages, turn.end_mages)):
        if mi == 0 or mi == 3:
            assert e_mage.get_skill_days('FORC') == 30
            assert turn.is_teaching(mi) == False
            assert turn.get_teacher_num_by_mage(s_mage) == -1
            assert turn.get_taught_by_num(s_mage) == -1
            assert turn.is_taught(s_mage) == False
        elif mi == 1:
            assert e_mage.get_skill_days('FORC') == 30
            assert turn.is_teaching(mi) == True
            assert turn.get_teacher_num_by_mage(s_mage) == 0
            assert turn.get_taught_by_num(s_mage) == -1
            assert turn.is_taught(s_mage) == False
        elif mi == 11:
            assert e_mage.get_skill_days('PATT') == 30
            assert turn.is_teaching(mi) == False
            assert turn.get_teacher_num_by_mage(e_mage) == -1
            assert turn.get_taught_by_num(s_mage) == -1
            assert turn.is_taught(s_mage) == False
        else:
            assert e_mage.get_skill_days('FORC') == 60
            assert turn.is_teaching(mi) == False
            assert turn.get_teacher_num_by_mage(e_mage) == -1
            assert turn.get_taught_by_num(s_mage) == 0
            assert turn.is_taught(s_mage) == True

def test_teaching_with_no_teach(mages):
    mages[1].train('FORC', 30)
    expected_students = [mages[2], mages[4], mages[5], mages[6], mages[7], mages[8], mages[9], mages[10]]
    turn = Turn(mages, 'FORC,TEACH-100-103,FORC,FORC,FORC,FORC,FORC,FORC,FORC,FORC,FORC,PATT', 10)
    for mi,(s_mage,e_mage) in enumerate(zip(turn.start_mages, turn.end_mages)):
        if mi == 0 or mi == 3:
            assert e_mage.get_skill_days('FORC') == 30
            assert turn.is_teaching(mi) == False
            assert turn.get_teacher_num_by_mage(s_mage) == -1
            assert turn.get_taught_by_num(s_mage) == -1
            assert turn.is_taught(s_mage) == False
        elif mi == 1:
            assert e_mage.get_skill_days('FORC') == 30
            assert turn.is_teaching(mi) == True
            assert turn.get_teacher_num_by_mage(s_mage) == 0
            assert turn.get_taught_by_num(s_mage) == -1
            assert turn.is_taught(s_mage) == False
        elif mi == 11:
            assert e_mage.get_skill_days('PATT') == 30
            assert turn.is_teaching(mi) == False
            assert turn.get_teacher_num_by_mage(e_mage) == -1
            assert turn.get_taught_by_num(s_mage) == -1
            assert turn.is_taught(s_mage) == False
        else:
            assert e_mage.get_skill_days('FORC') == 60
            assert turn.is_teaching(mi) == False
            assert turn.get_teacher_num_by_mage(e_mage) == -1
            assert turn.get_taught_by_num(s_mage) == 0
            assert turn.is_taught(s_mage) == True

def test_incorrect_order_length(mages):
    with pytest.raises(ValueError):
        turn = Turn(mages, ',,', 10)
