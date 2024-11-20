@echo off

start cmd /k "conda activate clean-tf && python model_api.py"

start cmd /k "cd /d %~dp0frontend && npm start"
