import pytest
import unittest.mock as mock

from src.atlaversity.Skill import Skill

def test_string_to_skill():
    assert Skill.string_to_skill('PATT').name == 'PATT'
    assert Skill.string_to_skill('DEMO').name == 'DEMO'
