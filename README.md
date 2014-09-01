Scripts for the Starter Pack
============================

A collection of simple scripts written to enhance the [DF Starter Pack](http://www.bay12forums.com/smf/index.php?topic=126076).  I've published them here for public review, to enable contributions, and because publishing encourages me to comment and structure my code properly ;)

Unless noted otherwise in the description or at the top of the .bat file itself, they are used from the root folder of the Starter Pack.  Scripts for the 34.11 pack have their own folder, the others are for 40.xx

Contributions are very welcome; please send pull requests to the development branch.  

=================================

#### /Copy data from an older Starter Pack.bat
A tool designed to make updating to a newer release of the Starter Pack as painless as possible.  It does not recognise older packages with incompatible saves; there you must copy any desired files across yourself.  

It assumes that the target pack is in the same parent folder as the destination pack (from which the script is run).  It checks for compatible packs; iterating through possible candidates by minor DF release, then pack release number - treating vanilla DF as pack release zero.  

When the first compatible pack is found, it copies the gamelog and save folder from the target to the destination, and if copying from a Starter Pack also copies the `User Generated Content` folder and the soundsense sound files to avoid a slow re-download.  

#### /LNP/utilities/World Viewer/World Viewer.bat
A batch file that checks whether the system is 32 or 64 bit, and launches the appropriate version of World Viewer.  Simplifies the utilities list when you show this instead of two executables.  

#### ../pack_update_script.py
NOT INTENDED FOR END USERS; published here because someone might be interested and version control is good for me.  

A python script I wrote to help avoid forgetting to update various parts of the pack when a new version of DF is released.  Run from the parent folder of the starter pack, it will check various configuration files are up to date and other files exist.  It's been upgraded from check list to assistant, it can now update some configuration files (mostly paths to the DF folder, which includes a version string.  

If everything is OK, zip the pack, and finalise documentation for this version (calculate the checksum, insert that in the file, and write most of my forum post).

=================================

## Legacy scripts from 34.11

The Starter Pack for DF 34.11 can be found [here](http://dffd.wimbli.com/file.php?id=8687).  

`Copy data from an older Starter Pack.bat` works as described above, with slight differences to match the circumstances of the pack.  

#### /Dwarf Fortress 34.11/_Move .dfmap files for Overseer.bat
Copies all files of form `*.dfmap` to `User Generated Content/Overseer map files/`.  These files are exported with the dfhack command `mapexport`, and used by the utility Fortress Overseer.  They are *much* easier to find with the GUI if placed in a subfolder (created by symlink per above).

#### /LNP/utilities/dfterm3 v0.3.1/call-dfterm3.bat
Placed in a folder with `dfterm3-0.3.1-setup.exe`, this script is designed to replace the dfterm entry in the utilities list - it installs dfterm3 if it's not already installed, or launches it if it is.  
