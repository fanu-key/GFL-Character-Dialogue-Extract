# Import libraries
import os
import glob
import shutil
import pandas as pd
import sys
import threading

# Input for which character to extract dialogue for
inputCharacter = input('Enter character name: ')

# Make directories for output
pathOutputInput = './Output/InputLines'
pathOutputCharacter = './Output/CharacterLines'

try:
    os.makedirs(pathOutputInput)
    os.makedirs(pathOutputCharacter)
except FileExistsError:
    print()

success = False

# path to text files to be read
dirPath = r'Input\**\*.txt'
savePath = r'Output\InputLines'

# This will list all text files in the input folder, only use for debugging
"""for file in glob.glob(dirPath, recursive=True):
    print(file)"""

# Read each text file in input folder and write each file to one big combined text file
inputFolder = glob.glob(dirPath, recursive=True)
mergedInput = open("merged.txt", "w+", encoding='utf8')

for file in inputFolder:
    with open('{}'.format(file), 'r+', encoding='utf8') as input:
        mergedInput.write(input.read())

mergedInput.close()

# Move the combined text file to output folder
sourceFolder = r'merged.txt'
destinationFolder = r'Output/InputLines/merged.txt'
shutil.move(sourceFolder, destinationFolder)

# Open merged file to read
allTextPath = r'Output/InputLines/merged.txt'
allText = open(allTextPath, 'r+', encoding='utf8')

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
characterDialogue = open('{}_Dialogue.txt'.format(inputCharacter), 'w+', encoding='utf8')
characterLines = []

characterCheck = ':'

# Threadlocking so we don't have a race condition error

lock = threading.Lock()
lock.acquire()

for line in readFixedMerged:
    if line.startswith('{}:'.format(inputCharacter)):
        index = line.find(characterCheck)
        characterDialogue.write(line[index + 2:])
        characterLines.append(line[index + 2:].rstrip('\n'))
        #ak12Dialogue.write(f"{line}\n")
        
characterDialogue.close()
lock.release()

# Reading all lines in characterLines for debugging
"""for lines in characterLines:
    print(lines)"""

# This shit is the reason why some characters did not work for extraction
# Commenting until I can fix it (May 13 2023)
# May 15 2023 - Fixed it
# Explanation after sleeping on it: Race condition
# Check if text file is empty, if yes delete file and exit program
if os.path.getsize('{}_Dialogue.txt'.format(inputCharacter)) == 0:
    print('Character does not exist. File is empty. Check if input is typed correctly')
    os.remove('{}_Dialogue.txt'.format(inputCharacter))
    sys.exit()

# Convert lines in list to csv file
characterCsv = open('{}_Dialogue.csv'.format(inputCharacter), 'w+', encoding='utf8')

dataFrame = pd.DataFrame(data = characterLines)
dataFrame.to_csv('{}_Dialogue.csv'.format(inputCharacter), header=False, index=False, encoding='utf8')

# Close files so we can move them into folders
fixedMerged.close()
readFixedMerged.close()
characterDialogue.close()
characterCsv.close()
mergedInput.close()
allText.close()

# Move character_Dialogue.txt, and character_Dialogue.csv to their respective folders
characterDialogueTxtSourceFolder = r'{}_Dialogue.txt'.format(inputCharacter)
characterDialogueCsvSourceFolder = r'{}_Dialogue.csv'.format(inputCharacter)

characterDialogueTxtDestFolder = r'Output/CharacterLines/{}_Dialogue.txt'.format(inputCharacter)
characterDialogueCsvDestFolder = r'Output/CharacterLines/{}_Dialogue.csv'.format(inputCharacter)

shutil.move(characterDialogueTxtSourceFolder, characterDialogueTxtDestFolder)
shutil.move(characterDialogueCsvSourceFolder, characterDialogueCsvDestFolder)

success=True

# If success, print message to console, else print failure
if success==True:
    print("Extract Success. Check Output folder.")

if success==False:
    print('Extract Failure.')

sys.exit()
