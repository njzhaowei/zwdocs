cd .. 
rmdir "dist" /S /Q
REM .venv\Scripts\python setup.py sdist bdist_wheel
.venv\Scripts\python setup.py bdist_wheel 
@REM .venv\Scripts\python -m twine upload dist/* -r pipdev
@echo off
pause