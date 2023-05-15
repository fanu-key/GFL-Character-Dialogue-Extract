# Import libraries
import os
import glob
import shutil
import pandas as pd
import sys

# Input for which character to extract dialogue for
character = input('Enter character name: ')

# Make directories for output
pathOutputInput = './Output/InputLines'
pathOutputCharacter = './Output/CharacterLines'

try:
    os.makedirs(pathOutputInput)
    os.makedirs(pathOutputCharacter)
except FileExistsError:
    print('\nFolders already exist. No need to create again.')
    
success = False

# path to text files to be read
dirPath = r'Input\**\*.txt'
savePath = r'Output\InputLines'

"""# This will list all text files in the input folder, only use for debugging
for file in glob.glob(dirPath, recursive=True):
    print(file)"""

# Read each text file in input folder and write each file to one big combined text file
inputFolder = glob.glob(dirPath, recursive=True)
mergedInput = open("merged.txt", "wb")

with mergedInput as output:
    for file in inputFolder:
        with open(file, "rb") as input:
            output.write(input.read())

# Move the combined text file to output folder
sourceFolder = r'merged.txt'
destinationFolder = r'Output/InputLines/merged.txt'
shutil.move(sourceFolder, destinationFolder)

# Open merged file to read
allTextPath = r'Output/InputLines/merged.txt'
allText = open(allTextPath, 'r', encoding='utf8')

# Ascii handling, replace � with a space and move to output folder
fixedMerged = open('fixedMerged.txt', 'w+', encoding='utf8')

for line in allText:
    line.replace('�', ' ')
    fixedMerged.write(line)

fixedMerged.close()

fixedMergedSourceFolder = r'fixedMerged.txt'
fixedMergedDestFolder = r'Output/Inputlines/fixedMerged.txt'
shutil.move(fixedMergedSourceFolder, fixedMergedDestFolder)


# Extract all character dialogue and put into a text file and into a list
fixedMergedPath = r'Output/InputLines/fixedMerged.txt'
readFixedMerged = open(fixedMergedPath, 'r+', encoding='utf8')
characterDialogue = open('{}Dialogue.txt'.format(character), 'w+', encoding='utf8')
characterLines = []

characterCheck = ':'

for line in readFixedMerged:
    if line.startswith('{}:'.format(character)):
        index = line.find(characterCheck)
        characterDialogue.write(line[index + 2:])
        characterLines.append(line[index + 2:].rstrip('\n'))
        #ak12Dialogue.write(f"{line}\n")

"""# Reading all lines in ak12Lines for debugging
for lines in ak12Lines:
    print(lines)"""

# Check if text file is empty, if yes exit program and delete file
if os.path.getsize('{}Dialogue.txt'.format(character)) == 0:
    print('File is empty! Character does not exist. Check if input is typed correctly')
    characterDialogue.close()
    os.remove('{}Dialogue.txt'.format(character))
    sys.exit()

# Convert lines in list to csv file
characterCsv = open('{}Dialogue.csv'.format(character), 'w+', encoding='utf8')

dataFrame = pd.DataFrame(data = characterLines)
dataFrame.to_csv('{}Dialogue.csv'.format(character), header=False, index=False, encoding='utf8')

# Close files so we can move them into folders
fixedMerged.close()
readFixedMerged.close()
characterDialogue.close()
characterCsv.close()
mergedInput.close()
allText.close()

# Move characterDialogue.txt, and characterDialogue.csv to their respective folders
characterDialogueTxtSourceFolder = r'{}Dialogue.txt'.format(character)
characterDialogueCsvSourceFolder = r'{}Dialogue.csv'.format(character)

characterDialogueTxtDestFolder = r'Output/CharacterLines/{}Dialogue.txt'.format(character)
characterDialogueCsvDestFolder = r'Output/CharacterLines/{}Dialogue.csv'.format(character)


shutil.move(characterDialogueTxtSourceFolder, characterDialogueTxtDestFolder)
shutil.move(characterDialogueCsvSourceFolder, characterDialogueCsvDestFolder)

success=True

# If success, print message to console, else print failure
if success==True:
    print("\nExtract Success. Check Output folder.")

if success==False:
    print('\nExtract Failure.')