@echo OFF
SETLOCAL

echo This script copies across save data from your last install of Dwarf Fortress. 
echo It's designed to work with older versions of the Dwarf Fortress Strter Pack, 
echo and can import saves from a copy of the vanilla game too.  
echo. 
echo All of these depend on the name of the folder staying default, and this new pack being in the same folder as the old one.  
echo.
timeout /t 60


::gives 'Dwarf Fortress %major_DF_version%_%minor_DF_version% Starter Pack r%release#%' - aim is to reverse this
for %%* in ("%CD%") do set CurrDirName=%%~n*

:: split name up by spaces, and keep the numbers as interim variables (not working yet)
for /f "tokens=1,2,3,4,5,6 delims= " %%a in ("%CurrDirName%") do (
    set "version_string=%%c"
    set "release_r#=%%f"
)
::split version_string into major and minor version numbers
for /f "tokens=1,2 delims=_" %%a in ("%version_string%") do (
    set "major_DF_version=%%a"
    set "minor_DF_version=%%b"
)
rem strip 'r' from release # by adding to end and stripping a character from each side
set "release##=%release_r#%r"
set "release#=%release##:~1,-1%

::we now have interger variables for major and minor DF version, and pack release number.

::find an older pack...
:: subtract 1 from current version to avoid circular copies
SET /A "result=%release#% - 1"
:: count down pack releases from current to 1
FOR /L %%G IN (%result%,-1,0) do (
    IF EXIST "%CD%\..\Dwarf Fortress %version_string% Starter Pack r%%G\" (
        set "previous_version=%CD%\..\Dwarf Fortress %version_string% Starter Pack r%%G\"
        goto Starter_Pack_found
    )
)

::special case, r1 used 40.01 instead of 40_01 which messed up parsing somehow
IF EXIST "%CD%\..\Dwarf Fortress 40.01 Starter Pack r1\" (
    set "previous_version=%CD%\..\Dwarf Fortress 40.01 Starter Pack r1\"
    goto Starter_Pack_found
)

rem Vanilla DF:
IF EXIST "%CD%\..\df_34_11_win\" (
    set "previous_version=%CD%\..\df_34_11_win\"
    GOTO vanilla_DF
    )
rem no compatible pack found?
GOTO no_pack_found

rem abort the whole thing if there are already save files in place, overwriting would be BAD
IF NOT EXIST "%CD%\Dwarf Fortress 0.%major_DF_version%.%minor_DF_version%\data\save\region*" goto no_saves_here
echo There are already save files in this pack!  
echo.
echo To avoid overwriting your data, this script will do nothing when save files are found.  
GOTO finish
:no_saves_here

:Starter_Pack_found
echo.
echo Copying the gamelog ...
COPY "%previous_version%Dwarf Fortress 0.%major_DF_version%.%minor_DF_version%\gamelog.txt" "%CD%\Dwarf Fortress 0.%major_DF_version%.%minor_DF_version%\gamelog.txt"
echo.
echo Copying the save folders...
ROBOCOPY "%previous_version%Dwarf Fortress 0.%major_DF_version%.%minor_DF_version%\data\save" "%CD%\Dwarf Fortress 0.%major_DF_version%.%minor_DF_version%\data\save" /e /NFL /NDL /NJH /NJS /nc /ns /xo
echo.
echo Copying user generated content...
ROBOCOPY "%previous_version%User Generated Content" "%CD%\User Generated Content" /e /NFL /NDL /NJH /NJS /nc /ns /xo
echo.
echo Copying the music and sound files for soundSense...
ROBOCOPY "%previous_version%LNP\utilities\soundsense\packs" "%CD%\LNP\utilities\soundsense\packs" /e /NFL /NDL /NJH /NJS /nc /ns /xo
)
echo.
goto finished_copying

:vanilla_DF
echo.
echo Copying the gamelog ...
COPY "%previous_version%gamelog.txt" "%CD%\Dwarf Fortress 0.34.11\gamelog.txt"
echo.
echo Copying the save folders...
ROBOCOPY "%previous_version%data\save" "%CD%\Dwarf Fortress 0.34.11\data\save" /e /NFL /NDL /NJH /NJS /nc /ns /xo
goto finished_copying

:finished_copying
echo.
echo. 
echo Finished copying your data to this pack, from %previous_version%
echo. 
echo Keep the old pack until you're sure everything has made it across - this didn't copy settings, only content.  
goto finish

:no_pack_found
echo.
echo No compatible pack was found!  This only works when your old install still has the default name, and is in the same folder as this install!
echo.
echo You can still keep save data and the gamelog from other packs or if you changed the name - you'll just need to copy-paste them by hand :(
GOTO finish

:finish
timeout /t 60
