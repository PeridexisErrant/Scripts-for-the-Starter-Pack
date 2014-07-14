@echo off


mklink >nul 2>&1
if errorlevel 9009 if not errorlevel 9010 (
    echo 'mklink' is not supported on this operating system.
    echo This is expected on windows xp and older
    echo It is also expected if running under WINE.
    echo The helpful symlinks for keeping custom content
    echo in the "User Generated Content" folder will not work
    timeout /t 30
    exit /b
)

REM ensure the current directory is the one that contains this batch file:
cd /D "%~dp0"

setlocal enabledelayedexpansion

set name[0]=User Blueprints
set source[0]=%CD%\LNP\utilities\Quickfort 2.04\blueprints\User Blueprints
set dest[0]=%CD%\User Generated Content\User Blueprints

echo Creating Symlinks...
echo.

call :CreateSymlink "!name[0]!" "!source[0]!" "!dest[0]!"
)

timeout /t 30
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


