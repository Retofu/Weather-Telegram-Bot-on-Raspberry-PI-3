@echo off
if not exist .venv (
  py -3 -m venv .venv
)
call .venv\Scripts\activate.bat
pip install -r requirements.txt
if not exist .env copy env.example .env >nul
python -m src.bot


