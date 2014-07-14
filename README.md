Scripts for the Starter Pack
============================

A collection of simple scripts written to enhance the [DF Starter Pack](http://www.bay12forums.com/smf/index.php?topic=126076).  I've published them here for public review, to enable contributions, and because publishing encourages me to comment properly ;)

Unless noted otherwise in the description or at the top of the .bat file itself, they are used from the root folder of the Starter Pack.  Scripts for the 34.11 pack have their own folder, the others are for 40.x

=================================

/Copy data from an older Starter Pack.bat
-----------------------------------------
If run from `/foo/... r6/`, it checks for `/foo/... r5/`, `/foo/... r4/`, etc and will copy saves and user content to the newer pack.  

Requires substantial updating for 40.x, which is a work in progress.  

/_Run Me First (make folders and symlinks).bat
----------------------------------------------
I was told late in the 34.11 days that symlinks do not survive compression - and I rely on them to put user-created application data in the User Content folder while also below some utilities.  This script simply recreates the symlinks after unzipping, and should be run first-thing - *especially* before the content-pulling script.  

 
=================================

Legacy scripts from 34.11
-------------------------

The Starter Pack for DF 34.11 can be found [here](http://dffd.wimbli.com/file.php?id=8687).  

`Copy data from an older Starter Pack.bat` and `_Run Me First (make folders and symlinks).bat` work as described above, with slight differences to match the circumstances of the pack.  

/Dwarf Fortress 34.11/_Move .dfmap files for Overseer.bat
---------------------------------------------------------
Copies all files of form `*.dfmap` to `User Generated Content/Overseer map files/`.  These files are exported with the dfhack command `mapexport`, and used by the utility Fortress Overseer.  They are *much* easier to find with the GUI if placed in a subfolder (created by symlink per above).

/LNP/utilities/dfterm3 v0.3.1/call-dfterm3.bat
----------------------------------------------
Placed in a folder with `dfterm3-0.3.1-setup.exe`, this script is designed to replace the dfterm entry in the utilities list - it installs dfterm3 if it's not already installed, or launches it if it is.  
