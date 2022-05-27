# -*- coding: utf-8 -*-
import pytest

from zwdocs.utils import *

@pytest.mark.parametrize(
    'txt, r', (
        ('  Zhaowei  is NO1, 一天吃 1 顿 ， 1 顿 吃 一 天 ', 'Zhaowei is NO1,一天吃1顿，1顿吃一天'),
    )
)
def test_remove_space_in_sentence(txt, r):
    o = rmexblank(txt)
    assert o == r