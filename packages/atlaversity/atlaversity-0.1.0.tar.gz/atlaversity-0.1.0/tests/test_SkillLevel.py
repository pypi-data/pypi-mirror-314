import pytest
import unittest.mock as mock

from src.atlaversity.SkillLevel import SkillLevel

def test_train():
    lvl = SkillLevel('PATT', 30)
    assert lvl.level == 1
    lvl.train(59)
    assert lvl.level == 1
    lvl.train(1)
    assert lvl.level == 2
