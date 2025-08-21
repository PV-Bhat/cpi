@echo off
setlocal enabledelayedexpansion

REM ===== Config =====
set "PAUSE_BETWEEN_RUNS_SECONDS=5"
set "PROBLEM=%~1"  REM P1 or P2
if "%PROBLEM%"=="" set "PROBLEM=P1"

REM Paths relative to this script
set "ROOT=%~dp0..\.."
set "REPO=%ROOT%\harness\problems\%PROBLEM%"
set "OUT=%ROOT%\traces\%PROBLEM%-runs"
if not exist "%OUT%" mkdir "%OUT%"
pushd "%REPO%"

:main_loop
    REM Reset working copy to clean HEAD to avoid state accumulation
    git reset --hard
    if defined GIT_CLEAN if "%GIT_CLEAN%"=="1" git clean -fdx

    REM Timestamp ISO-like yyyy-mm-dd_HH-MM-SS
    for /f "tokens=1-5 delims=:. " %%a in ("%time%") do (set hh=%%a& set nn=%%b& set ss=%%c)
    for /f "tokens=1-3 delims=/" %%a in ("%date%") do (set dd=%%a& set mm=%%b& set yyyy=%%c)
    set "timestamp=%yyyy%-%mm%-%dd%_%hh%-%nn%-%ss%"
    set "LOG_FILE=%OUT%\%PROBLEM%_!timestamp!.txt"

    if /I "%PROBLEM%"=="P1" (
        echo === RUN P1 !timestamp! === > "!LOG_FILE!"
        python run.py >> "!LOG_FILE!" 2>&1
    ) else (
        echo === RUN P2 !timestamp! === > "!LOG_FILE!"
        python deletekeys.py >> "!LOG_FILE!" 2>&1
    )

    timeout /t %PAUSE_BETWEEN_RUNS_SECONDS% /nobreak
goto main_loop
