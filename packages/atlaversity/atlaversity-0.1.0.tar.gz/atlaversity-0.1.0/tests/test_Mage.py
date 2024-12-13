import pytest

from Mage import *

LEVEL_1_DAYS = 30
LEVEL_2_DAYS = 90
LEVEL_3_DAYS = 180
LEVEL_4_DAYS = 300
LEVEL_5_DAYS = 450

@pytest.fixture
def mage():
    return Mage(123, 'foo')

def test_trained_skill_level(mage):
    assert mage.has_skill('COMB') == False
    mage.add_skill(SkillLevel('COMB', LEVEL_3_DAYS - 1))
    assert mage.has_skill('COMB') == True
    assert mage.has_skill_level('COMB', 2) == True
    assert mage.has_skill_level('COMB', 3) == False
    assert mage.get_skill_level('COMB') == 2
    assert mage.get_skill_days('COMB') == LEVEL_3_DAYS - 1

def test_untrained_skill_level(mage):
    assert mage.has_skill('PATT') == False
    assert mage.has_skill_level('PATT', 0) == True
    assert mage.has_skill_level('PATT', 1) == False
    assert mage.get_skill_level('PATT') == 0
    assert mage.get_skill_days('PATT') == 0

def test_invalid_skill_level(mage):
    assert mage.has_skill('invalid') == False
    assert mage.has_skill_level('invalid', 0) == True
    assert mage.has_skill_level('invalid', 1) == False
    assert mage.get_skill_level('invalid') == 0
    assert mage.get_skill_days('invalid') == 0

def test_can_study_foundations(mage):
    with pytest.raises(ValueError):
        assert mage.can_study('invalid') == False
    assert mage.can_study('FORC') == (True, '')
    assert mage.can_study('PATT') == (True, '')
    assert mage.can_study('SPIR') == (True, '')

def test_can_study_max_level(mage):
    mage.add_skill(SkillLevel('FORC', LEVEL_5_DAYS))
    assert mage.can_study('FORC') == (False, 'Already at skill level 5.')

def test_can_study_simple_prereq(mage):
    assert mage.can_study('FIRE') == (False, 'Missing prerequisite: FORC1. ')
    mage.add_skill(SkillLevel('FORC', LEVEL_3_DAYS))
    assert mage.can_study('FIRE') == (True, '')
    assert mage.can_study(Skill.string_to_skill('FIRE')) == (True, '')

def test_can_study_simple_prereq_nok(mage):
    mage.add_skill(SkillLevel('FORC', LEVEL_3_DAYS))
    assert mage.can_study('FIRE') == (True, '')
    mage.add_skill(SkillLevel('FIRE', LEVEL_3_DAYS))
    assert mage.can_study('FIRE') == (False, 'Missing prerequisite: FORC4. ')

def test_can_study_advanced_prereq_nok1(mage):
    assert mage.can_study('DRAG') == (False, 'Missing prerequisite: BIRD3. Missing prerequisite: WOLF3. ')
    mage.add_skill(SkillLevel('WOLF', LEVEL_3_DAYS - 1))
    mage.add_skill(SkillLevel('BIRD', LEVEL_3_DAYS))
    assert mage.can_study('DRAG') == (False, 'Missing prerequisite: WOLF3. ')

def test_can_study_advanced_prereq_nok2(mage):
    assert mage.can_study('DRAG') == (False, 'Missing prerequisite: BIRD3. Missing prerequisite: WOLF3. ')
    mage.add_skill(SkillLevel('WOLF', LEVEL_3_DAYS))
    mage.add_skill(SkillLevel('BIRD', LEVEL_3_DAYS - 1))
    assert mage.can_study('DRAG') == (False, 'Missing prerequisite: BIRD3. ')

def test_can_study_advanced_prereq_ok(mage):
    assert mage.can_study('DRAG') == (False, 'Missing prerequisite: BIRD3. Missing prerequisite: WOLF3. ')
    mage.add_skill(SkillLevel('WOLF', LEVEL_3_DAYS))
    mage.add_skill(SkillLevel('BIRD', LEVEL_3_DAYS))
    assert mage.can_study('DRAG') == (True, '')

def test_train(mage):
    assert mage.get_skill_level('PATT') == 0
    mage.train('PATT', LEVEL_3_DAYS)
    assert mage.get_skill_level('PATT') == 3
    assert mage.get_skill_days('PATT') == LEVEL_3_DAYS
    mage.train('PATT', LEVEL_5_DAYS - LEVEL_3_DAYS - 1)
    assert mage.get_skill_level('PATT') == 4
    assert mage.get_skill_days('PATT') == LEVEL_5_DAYS - 1
    mage.train('PATT', 1)
    assert mage.get_skill_level('PATT') == 5
    assert mage.get_skill_days('PATT') == LEVEL_5_DAYS

def test_can_teach(mage):
    mage.train('PATT', LEVEL_3_DAYS - 1)
    student = Mage(456, 'bar')
    student.train('PATT', LEVEL_2_DAYS - 1)
    assert mage.can_teach(student, 'PATT') == True
    student.train('PATT', 1)
    assert mage.can_teach(student, 'PATT') == False
    mage.train('PATT', 1)
    assert mage.can_teach(student, 'PATT') == True

def test_can_study_list_basic(mage):
    assert mage.get_can_study_list() == ['', 'PATT', 'FORC', 'SPIR']

def test_can_study_list_advanced(mage):
    mage.train('FORC', LEVEL_1_DAYS)
    assert mage.get_can_study_list() == ['', 'PATT', 'FORC', 'SPIR', 'FIRE', 'FSHI', 'ESHI']
