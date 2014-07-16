@echo off


mklink >nul 2>&1
if errorlevel 9009 if not errorlevel 9010 (
    echo 'mklink' is not supported on this operating system.
    echo This is expected on windows xp and older
    echo It is also expected if running under WINE.
    echo The helpful symlinks for keeping custom content
    echo in the "User Generated Content" folder will not work
    pause
    exit /b
)

REM ensure the current directory is the one that contains this batch file:
cd /D "%~dp0"

setlocal enabledelayedexpansion

set name[0]=User Blueprints
set source[0]=LNP\utilities\Quickfort 2.04\blueprints\User Blueprints
set dest[0]=User Generated Content\User Blueprints
set name[1]=Overseer map files
set source[1]=LNP\utilities\Overseer 0.70.1\_Map Files for Overseer
set dest[1]=User Generated Content\Overseer map files

echo Creating Symlinks...
echo.

for /l %%n in (0,1,1) do (
call :CreateSymlink "!name[%%n]!" "!source[%%n]!" "!dest[%%n]!"
)

pause
exit /b

:::

:CreateSymlink
SETLOCAL

set "name=%~1"
set "source=%~2"
set "target=%~3"

echo :%name%:
echo ::Removing target symlink or directory::

rmdir /s/q "%source%"  >NUL 2>NUL

echo ::Attempting to create symlink::

mklink /D "%source%" "%target%" >NUL 2>NUL
if NOT ERRORLEVEL 1 goto success

echo ::Could not create directory symbolic link. That is normal.::
echo ::Attempting directory junction.::

mklink /J "%source%" "%target%"  >NUL 2>NUL
if NOT ERRORLEVEL 1 goto success

echo ::Failure::

goto endoffunc

:success
echo ::Successful::

:endoffunc

ENDLOCAL
exit /b


