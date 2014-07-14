@echo off
setlocal
echo.

:: This script is designed to be placed in the Dwarf Fortress folder, and copies *.dfmap files
::  to the symlinked User Content folder, from which they are accessible to Fortress Overseer

if not exist "%CD%\*.dfmap" (
	echo No .dfmap files found!  You can export them with the dfhack command "mapexport".
	timeout /t 20
	goto finish
)

move "%CD%\*.dfmap" "%CD%\..\User Generated Content\Overseer Map Files\"
echo dfmap files moved to the User Content folder
timeout /t 20

:finish
