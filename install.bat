@echo off
rem OpenDash extras: copies the HD art next to opendash.exe.
rem Put this folder inside the OpenDash folder (or drop the OpenDash folder on this file) and run it.
setlocal
set "TARGET=%~1"
if "%TARGET%"=="" if exist "%~dp0..\opendash.exe" set "TARGET=%~dp0.."
if "%TARGET%"=="" if exist "%~dp0opendash.exe" set "TARGET=%~dp0"
if "%TARGET%"=="" set /p "TARGET=OpenDash folder (the one with opendash.exe): "
if not exist "%TARGET%\opendash.exe" (
    echo opendash.exe was not found in "%TARGET%".
    pause
    exit /b 1
)
xcopy /e /i /y /q "%~dp0assets" "%TARGET%\assets" >nul
echo Done: the HD art is in "%TARGET%\assets".
pause
