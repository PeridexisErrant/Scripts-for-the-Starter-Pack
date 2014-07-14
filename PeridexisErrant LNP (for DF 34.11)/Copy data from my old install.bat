@ECHO OFF
SETLOCAL

ECHO This script copies across save data from your last install of Dwarf Fortress. 
ECHO It's designed to work with older versions of the 'PeridexisErrant LNP', and also has untested support for 
ECHO   the old classic 'Lazy Newb Pack [v15]', the advanced version of that pack, and even the vanilla game.
echo. 
echo All of these depend on the name of the folder staying default, and this new version being in the same folder as the old one.  
echo.
pause

rem abort the whole thing if there are already save files in place, overwriting would be BAD
IF NOT EXIST "%CD%\Dwarf Fortress 0.34.11\data\save\region*" goto no_saves_here

    ECHO There are already save files in this folder!  
ECHO.
ECHO To avoid overwriting your data, this script will do nothing when save files are here.  
pause
GOTO end
:no_saves_here


REM - this bit copies from 
rem get this pack's version number
rem get this folder's name, of form 'peridexiserrant' 'lnp' 'r#'
for %%* in (.) do set CurrDirName=%%~n*
rem split name up by spaces, and keep the last set as a variable
for /f "tokens=1,2,3 delims= " %%a in ("%CurrDirName%") do set release_r#=%%a& set release_r#=%%b& set release_r#=%%c
rem now we have "r<version#>" as a variable, add an r to the end...
set "release##=%release_r#%r"
rem ... and trim off the first and last characters.  Inelegant but flexible.  
set "release#=%release##:~1,-1%
rem subtract 1 from current version to avoid circular copies
SET /A "result=%release#% - 1"
rem count down versions from current to 1
FOR /L %%G IN (%result%,-1,1) DO (
	IF EXIST "%CD%\..\PeridexisErrant LNP r%%G\" (
		set "previous_version=%CD%\..\PeridexisErrant LNP r%%G\"
		goto PeridexisErrant_LNP_found	
        )
	)

rem now look for packs that aren't PeridexisErrant LNP whatever:  
rem LucusUP's classic LNP:  
IF EXIST "%CD%\..\LazyNewbPack [0.34.11] [V15]\" (
    set "previous_version=%CD%\..\LazyNewbPack [0.34.11] [V15]\"
    GOTO classic_LNP
    )
IF EXIST "%CD%\..\LazyNewbPack Advanced [0.34.11] [V15]\" (
    set "previous_version=%CD%\..\LazyNewbPack Advanced [0.34.11] [V15]\"
    GOTO classic_LNP_advanced
    )
rem Vanilla DF:
IF EXIST "%CD%\..\df_34_11_win\" (
    set "previous_version=%CD%\..\df_34_11_win\"
    GOTO vanilla_DF
    )
rem no compatible pack found?
GOTO no_pack_found

:PeridexisErrant_LNP_found
rem copying from peridexiserrant LNP...
ECHO.
ECHO Copying the gamelog ...
COPY "%previous_version%Dwarf Fortress 0.34.11\gamelog.txt" "%CD%\Dwarf Fortress 0.34.11\gamelog.txt"
ECHO.
ECHO Copying the save folders...
ROBOCOPY "%previous_version%Dwarf Fortress 0.34.11\data\save" "%CD%\Dwarf Fortress 0.34.11\data\save" /e /NFL /NDL /NJH /NJS /nc /ns /xo
ECHO.
ECHO Copying user generated content...
ROBOCOPY "%previous_version%User Generated Content" "%CD%\User Generated Content" /e /NFL /NDL /NJH /NJS /nc /ns /xo
ECHO.
IF EXIST "%previous_version%LNP\utilities\soundSense r42\packs" (
	ECHO Copying the music and sound files for soundSense...
	ROBOCOPY "%previous_version%LNP\utilities\soundSense r42\packs" "%CD%\LNP\utilities\soundsense\packs" /e /NFL /NDL /NJH /NJS /nc /ns /xo
)
IF EXIST "%previous_version%LNP\utilities\soundsense\packs" (
	ECHO Copying the music and sound files for soundSense...
	ROBOCOPY "%previous_version%LNP\utilities\soundsense\packs" "%CD%\LNP\utilities\soundsense\packs" /e /NFL /NDL /NJH /NJS /nc /ns /xo
)
ECHO.
rem in r53, now using symlinks back instead of folders - so it's in the user content copy
if %result% < 53 (
	ECHO Copying Quickfort blueprints and .dfmap files...
	ROBOCOPY "%previous_version%\LNP\utilities\Quickfort 2.04\blueprints" "%CD%\User Generated Content\User Blueprints\" /e /NFL /NDL /NJH /NJS /nc /ns /xo
	COPY "%previous_version%\LNP\utilities\Overseer 0.70.1\*.dfmap" "%CD%\User Generated Content\Overseer Map Files\"
	)
goto finished_copying

:classic_LNP
ECHO.
ECHO Copying the gamelog ...
COPY "%previous_version%Dwarf Fortress 0.34.11\gamelog.txt" "%CD%\Dwarf Fortress 0.34.11\gamelog.txt"
ECHO.
ECHO Copying the save folders...
ROBOCOPY "%previous_version%Dwarf Fortress 0.34.11\data\save" "%CD%\Dwarf Fortress 0.34.11\data\save" /e /NFL /NDL /NJH /NJS /nc /ns /xo
ECHO.
ECHO Copying the music and sound files for soundSense...
ROBOCOPY "%previous_version%LNP\Utilities\1-Newb\soundSense r35\packs" "%CD%\LNP\utilities\soundsense\packs" /e /NFL /NDL /NJH /NJS /nc /ns /xo
goto finished_copying

:classic_LNP_advanced
ECHO.
ECHO Copying the gamelog ...
COPY "%previous_version%Dwarf Fortress 0.34.11\gamelog.txt" "%CD%\Dwarf Fortress 0.34.11\gamelog.txt"
ECHO.
ECHO Copying the save folders...
ROBOCOPY "%previous_version%Dwarf Fortress 0.34.11\data\save" "%CD%\Dwarf Fortress 0.34.11\data\save" /e /NFL /NDL /NJH /NJS /nc /ns /xo
ECHO.
ECHO Copying the music and sound files for soundSense...
ROBOCOPY "%previous_version%LNP\Utilities\1-Newb\soundSense r35\packs" "%CD%\LNP\utilities\soundsense\packs" /e /NFL /NDL /NJH /NJS /nc /ns /xo
ECHO.
ECHO Copying Quickfort blueprints...
ROBOCOPY "%previous_version%\LNP\Utilities\2-Advanced\Quickfort\Quickfort 2.04\blueprints" "%CD%\User Generated Content\User Blueprints" /e /NFL /NDL /NJH /NJS /nc /ns /xo
goto finished_copying

:vanilla_DF
ECHO.
ECHO Copying the gamelog ...
COPY "%previous_version%gamelog.txt" "%CD%\Dwarf Fortress 0.34.11\gamelog.txt"
ECHO.
ECHO Copying the save folders...
ROBOCOPY "%previous_version%data\save" "%CD%\Dwarf Fortress 0.34.11\data\save" /e /NFL /NDL /NJH /NJS /nc /ns /xo
goto finished_copying

:finished_copying
echo.
echo. 
echo Finished copying you data to this pack, from %previous_version%
echo. 
echo Keep the old pack until you're sure everything has made it across - this didn't copy settings, only content.  
pause
goto end

:no_pack_found
echo.
ECHO No compatible pack was found!  This only works when your old install still has the default name, and is in the same folder as this install!
echo So far, it only supports 
echo     - the vanilla game (in folder "df_34_11_win"), 
echo     - the old Lazy Newb Packs (in "LazyNewbPack [0.34.11] [V15]" or
echo                                   "LazyNewbPack Advanced [0.34.11] [V15]"), 
echo     - previous versions of the PeridexisErrant LNP.  
echo.
echo You can still keep save data and the gamelog from other packs or if you changed the name - you'll just need to copy-paste them by hand :(
pause
GOTO end

:end