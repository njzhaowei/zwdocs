#!/bin/bash
../.venv/bin/python -m pip install --upgrade pip
../.venv/bin/pip install -U -r ../docs/requirements.txt
../.venv/bin/pip install -U -r ../requirements_dev.txt
../.venv/bin/pip install -U -r ../requirements.txt