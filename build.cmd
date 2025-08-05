@echo off
REM === Step 1: cur dir ===
cd /d %~dp0

REM === Step 2: main  ===
set MAIN_FILE=main.py

REM === Step 3: Conda env ===
set CONDA_ENV_NAME=tk-dlp

REM === Step 4: activate conda env ===
CALL conda activate  %CONDA_ENV_NAME%
REM 

REM === Step 5: get customtkinter dir ===
FOR /F "usebackq delims=" %%i IN (`python -c "import customtkinter, os; print(os.path.dirname(customtkinter.__file__))"`) DO (
    SET "CUSTOMTKINTER_PATH=%%i"
)

REM === Step 6: buid PyInstaller cmd ===
SET BUILD_CMD=pyinstaller ^
 --noconfirm ^
 --onedir ^
 --windowed ^
 --add-data "config.ini;." ^
 --add-data "language;language" ^
 --add-data "image;image" ^
 --add-data "%CUSTOMTKINTER_PATH%;customtkinter" ^
 %MAIN_FILE%

REM === Step 7: run ===
echo 🔧 Build command:
echo %BUILD_CMD%
%BUILD_CMD%

REM === Step 8: done ===
echo ✅ Pkg done.
pause
