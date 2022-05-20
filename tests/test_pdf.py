# -*- coding: utf-8 -*-
import pytest
import shutil
from pathlib import Path
from zwdocs.pdf import Pdf

BASE_PATH = Path('tests/data/pdf')
TEMP_PATH = BASE_PATH / 'tmp'

def setup_module():
    shutil.rmtree(TEMP_PATH, ignore_errors=True)

def teardown_module():
    shutil.rmtree(TEMP_PATH, ignore_errors=True)

@pytest.mark.parametrize(
    'pth', (
        '2022年中观产业链中期展望：寻找最优解-20220430-西部证券-20页.pdf',
    )
)
def test_pdf2html(pth):
    o = Pdf(BASE_PATH/pth)
    r = o.pdf2html(outpath=TEMP_PATH/(f'{o.pth.stem}.html'), exclude_re=r'起点财经')
    assert len(r) > 0

@pytest.mark.parametrize(
    'pth', (
        '2022年中观产业链中期展望：寻找最优解-20220430-西部证券-20页.pdf',
    )
)
def test_pdf2txt(pth):
    o = Pdf(BASE_PATH/pth)
    r = o.pdf2txt(outpth=TEMP_PATH/(f'{o.pth.stem}.txt'))
    assert len(r) > 0

@pytest.mark.parametrize(
    'pth, rtn', (
        ('2022年中观产业链中期展望：寻找最优解-20220430-西部证券-20页.pdf', 8),
    )
)
def test_pdf2png(pth, rtn):
    o = Pdf(BASE_PATH/pth)
    r = o.pdf2png(outdir=TEMP_PATH)
    assert len(r) == rtn