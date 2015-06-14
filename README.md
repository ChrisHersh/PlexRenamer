# PlexRenamer
Renames files so the Plex Media Server can process them more correctly

I am not responsible for anything this script may do, you use it at your own risk. I reccomend at least doing a dry run and make sure you're okay with all of the changes it will make

This scipt is designed for renaming the episodes to a sXX eYY format so plex has a greater chance of indexing the seasons properly. It was designed for a root folder that has N directories each representing 1 season

#Running
To run this you will need python3 installed. Then open a terminal (Mac OSX, Linux) or cmd.exe (Windows) and run `python plexRenamer.py <path>` where <path> is the full path to the folder of the content you want to rename, if it has spaces put the entire path in quotes, eg: "D:\TV Shows\The Simpsons"

There are a number of flags you really should look at, such as the prefix for the new names. If you don't change any flags in the code this probably will not work. See the .py file for what you may need to change

#TODO
	+Allow the episode counter to be independant of the season
	+Allow renaming within a single directory (no seasons)
