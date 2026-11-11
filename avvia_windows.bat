@echo off
rem Avvia la coreografia: pianifica con A* (Python 3) ed esegue le mosse con il Python 2 di Choregraphe.
rem Uso:  avvia_windows.bat PORTA      (porta: Choregraphe > Edit > Preferences > Virtual Robot)
set PORTA=%1
if "%PORTA%"=="" set /p PORTA=Porta del robot virtuale: 
cd /d "%~dp0"
set PY3=python
where py >NUL 2>NUL && set PY3=py -3
if exist "%USERPROFILE%\anaconda3\python.exe" set PY3="%USERPROFILE%\anaconda3\python.exe"
%PY3% main.py 127.0.0.1 %PORTA%
pause
