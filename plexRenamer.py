from os import listdir, rename
from os.path import join, isfile
import sys
import re


#######################################################
## FLAGS THAT NEED TO BE LOOKED AT BEFORE RUNNING
#######################################################

#dryRun will not change any files, it will print out what it would have changed
dryRun = True

#Change to fit needs, if no subtitle files set boolean below to false
#If you don't know if you have subtitle files, you probably don't
videoFiletype = "mkv"
subtitleFiletype = "ass"

#Are there any subtitle files (.ass/.sas) that should be renamed?
renameSubtitleFiles = True

#This will be before the season and episode count
# eg: Ginatama-s01e003.mkv
renamedFilePrefix = "Gintama - "

#This is used to make the regex more likely to grab the correct number from the title
currentEpisodePrefix = "[RG Genshiken] Gintama - "

#How many digits are the current episode numbers?
episodeNumberLength = 2

#################################
## END OF FLAGS
#################################


###### You can safely ignore everything below this #######


#episodeRegex will get the episode number for normal episodes
#multiRegex will catch episodes with multiple episodes
episodeRegex = re.compile(r"" + re.escape(currentEpisodePrefix) + r"(\d{" + str(episodeNumberLength) + r"}).*")
multiRegex = re.compile(r"" + re.escape(currentEpisodePrefix) + 
	r"(\d{" + str(episodeNumberLength) + r"}-\d{" + str(episodeNumberLength) + r"}).*")




def renameFile(seasonCounter, seasonPath, currEpisodeName, epNum, filetype):
	newName = renamedFilePrefix + "s" + str(seasonCounter) + "e" + epNum
	if(filetype[0] == "."):
		newName = newName + filetype
	else:
		newName = newName + "." + filetype

	if(dryRun):
		print(currEpisodeName + " --> " + newName)
	else:
		try:
			rename(join(seasonPath, currEpisodeName), join(seasonPath, newName))
		except Exception as e:
			print(str(e))


def printError(msg):
	sys.stderr.write(msg)

def printProcessingError(episode, season):
	printError("Could not process file: " + episode + "\n\tIn directory: " + season + "\n")


def renameFiles(filetype, seasonDirs):
	#TODO
	seasonCounter = 0
	for s in seasonDirs:
		seasonPath = join(basePath, s)
		seasonCounter += 1

		#get all episodes in the current directory that are of the proper filetype
		episodes = [ f for f in listdir(seasonPath) if ( isfile(join(seasonPath,f)) and (f.endswith(filetype)) ) ]
		episodes.sort()

		for e in episodes:
			#Try the multi first as it's the most restrictive
			try:
				epNum = multiRegex.match(e).group(1)
				renameFile(seasonCounter, seasonPath, e, epNum, filetype)
			#Then see if it's a valid normal episode
			except AttributeError:
				#Python cannot catch any errors in this except without another try block
				try:
					epNum = episodeRegex.match(e).group(1)
					renameFile(seasonCounter, seasonPath, e, epNum, filetype)
					#Finally warn user of invalid file and where it's located
				except:
					printProcessingError(e, s)
			except:
				printProcessingError(e, s)



#Get all directories, ignore files
def runRename():
	seasonDirs = [ f for f in listdir(basePath) if (not isfile(join(basePath,f))) ]
	seasonDirs.sort()

	#Rename the video files and the subtitle files if applicable
	renameFiles(videoFiletype, seasonDirs)

	if(renameSubtitleFiles):
		try:
			renameFiles(subtitleFiletype, seasonDirs)
		except:
			printError("Could not process subtitle files correctly")




if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Please give a path to the root of the series")
		sys.exit()

	basePath = sys.argv[1];

	runRename()