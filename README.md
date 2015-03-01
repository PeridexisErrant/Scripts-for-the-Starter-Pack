Scripts for the Starter Pack
============================

A collection of simple scripts written to enhance the [DF Starter Pack](http://www.bay12forums.com/smf/index.php?topic=126076).  I've published them here for public review, to enable contributions, and because publishing encourages me to comment and structure my code properly ;)

Unless noted otherwise in the description or at the top of the .bat file itself, they are used from the root folder of the Starter Pack.  Contributions are very welcome.

=================================

#### /Copy data from an older Starter Pack.bat
A tool designed to make updating to a newer release of the Starter Pack as painless as possible.  It does not recognise older packages with incompatible saves; there you must copy any desired files across yourself.  

It assumes that the target pack is in the same parent folder as the destination pack (from which the script is run).  It checks for compatible packs; iterating through possible candidates by minor DF release, then pack release number - treating vanilla DF as pack release zero.  

When the first compatible pack is found, it copies the gamelog and save folder from the target to the destination, and if copying from a Starter Pack also copies the `User Generated Content` folder and the soundsense sound files to avoid a slow re-download.  

#### /LNP/utilities/World Viewer/World Viewer.bat
A batch file that checks whether the system is 32 or 64 bit, and launches the appropriate version of World Viewer.  Simplifies the utilities list when you show this instead of two executables.  
