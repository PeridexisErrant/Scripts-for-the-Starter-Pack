@echo OFF
SETLOCAL

echo This script copies across save data from your last install of Dwarf Fortress. 
echo It's designed to work with older versions of the Dwarf Fortress Starter Pack, 
echo and can import saves from a copy of the vanilla game too.  
echo. 
echo All of these depend on the name of the folder staying default, and this new pack being in the same folder as the old one.  
echo.
timeout /t 60

call:get_future_pack_info
echo New pack is "%major_DF_version%_%minor_DF_version% r%release#%"
echo.

:: abort the whole thing if there are already save files in place, overwriting would be BAD
IF EXIST "Dwarf Fortress 0.%major_DF_version%.%minor_DF_version%\data\save\region*" (
    echo There are already save files in this pack!  
    echo.
    echo To avoid overwriting your data, this script will do nothing when save files are found.  
    GOTO finish
)

::find an older pack...
set minor_DF_version_int=%minor_DF_version% rem because for can't take zero-padded numbers
for /L %%G in (1,1,10) do (
    if "%minor_DF_version%" == "0%%G" set minor_DF_version_int=%%G
)
set /a "past_release#=%release#% - 1"

FOR /L %%F IN (%minor_DF_version_int%,-1,3) do (       rem     iterate down through minor DF versions to 03, since lower is not save-compatible
	set "past_minor_DF_version=%%F"
	if %%F LEQ 9 ( set "past_minor_DF_version=0%%F" ) rem zero-pad single digits for string comparisons
    if not "%minor_DF_version%" == "%past_minor_DF_version%" (
        set "past_release#=10"        rem 10 should work for some time given bugfix DF releases
        :: can add magic numbers here to iterate the correct number of times (ie # of packs for each minor version
        :: eg:  '''if "%%F" == "02" set "past_release#=1" rem there were 1 pack releases for 40_02'''
    )
    FOR /L %%G IN (%past_release#%,-1,1) do (         rem     iterate down through pack versions to r1 (resets to this each DF update)
        set "previous_version=..\Dwarf Fortress %major_DF_version%_%past_minor_DF_version% Starter Pack r%%G\"
		IF EXIST %previous_version% (
            set "old_DF_folder=%previous_version%Dwarf Fortress 0.%major_DF_version%.%past_minor_DF_version%\"
			echo Past pack is "%major_DF_version%_%past_minor_DF_version% r%%G"
            call:copy_saves_and_gamelog
            call:copy_UGC_and_symlinked_data
            call:done_copying
            goto finish
        )
    )
    set "previous_version=..\df_%major_DF_version%_%past_minor_DF_version%_win\" rem vanilla DF
	IF EXIST %previous_version% (
        set "old_DF_folder=%previous_version%"
		echo Past pack is "Vanilla DF %major_DF_version%_%past_minor_DF_version%"
        call:copy_saves_and_gamelog
        call:done_copying
        goto finish
    )
)
echo.
echo No compatible pack was found!  This script only works when your old install still has the default name, and is in the same folder as this install.
echo.
echo You can still keep save data and the gamelog from other packs or if you changed the name - you'll just need to copy-paste them by hand.
echo.
echo If you're trying to copy from before a big update, saves from before DF 0.40.03 are not compatible, so prior packs will not be detected.

:finish
echo.
timeout /t 60
exit

::-------------------------
::----    functions    ----
::-------------------------

:get_future_pack_info
::Our pack is 'Dwarf Fortress %major_DF_version%_%minor_DF_version% Starter Pack r%release#%' - let's find the numbers
:: get name of folder as string
for %%* in ("%CD%") do set CurrDirName=%%~n*
:: split name up by spaces, and keep the numbers as interim variables
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
::we now have variables for major and minor DF version, and pack release number.
:: nb- a zero padded number (eg '04') is treated as a string, not an integer (affects minor version)
goto:EOF

:copy_saves_and_gamelog
echo.
echo Copying the gamelog ...
COPY "%old_DF_folder%gamelog.txt" "Dwarf Fortress 0.%major_DF_version%.%minor_DF_version%\gamelog.txt"
echo.
echo Copying the save folders...
ROBOCOPY "%old_DF_folder%data\save" "Dwarf Fortress 0.%major_DF_version%.%minor_DF_version%\data\save" /e /NFL /NDL /NJH /NJS /nc /ns /xo
goto:EOF

:copy_UGC_and_symlinked_data
echo.
echo Copying user generated content and symlinked data...
ROBOCOPY "%previous_version%User Generated Content" "User Generated Content" /e /NFL /NDL /NJH /NJS /nc /ns /xo
echo.
echo Copying the music and sound files for soundSense...
ROBOCOPY "%previous_version%LNP\utilities\soundsense\packs" "LNP\utilities\soundsense\packs" /e /NFL /NDL /NJH /NJS /nc /ns /xo
goto:EOF

:done_copying
echo. 
echo Finished copying your data to this pack, from:
echo "%previous_version%"
echo.
echo Keep the old pack until you're sure everything has made it across - this didn't copy settings, only content.  
goto:EOF
