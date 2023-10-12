#!/bin/bash

./activate-venv.sh

watchfiles --ignore-paths "venv" --filter="python" 'venv/Scripts/python main.py'