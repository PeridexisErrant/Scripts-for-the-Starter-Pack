@echo off
setlocal

for /f "tokens=4-5 delims=. " %%i in ('ver') do set VERSION=%%i
if "%version%" == "5" do (
	echo Warning!  Windows XP is not supported by dfterm3!
	echo.
	echo Now closing...
	timeout /t 10
	goto end

If exist "C:\Program Files (x86)\Dfterm3\dfterm3.exe" (
	CD "C:\Program Files (x86)\Dfterm3\"
	dfterm3.exe
	GOTO end)

If exist "C:\Program Files\Dfterm3\dfterm3.exe" (
	CD "C:\Program Files\Dfterm3\"
	dfterm3.exe
	GOTO end)

Echo dfterm3 is a webserver application that allows you to share a game of Dwarf Fortress with anyone across the internet.
echo.
SET /P ANSWER=Would you like to install dfterm3 (y/n)?
if /i {%ANSWER%}=={y} (goto :install)
goto end

:install
echo.
Echo For dfterm to work in the LNP, it needs to be installed in "C:\Program Files (x86)\Dfterm3\" or "C:\Program Files\Dfterm3\"- this will allow this option in the utilities list to open it next time.
echo.
echo You can set dfterm to run automatically every time by ticking the launch box in the utilities list, and putting "start-dftem3" in dfhack.init
pause

dfterm3-0.3.1-setup.exe

:end