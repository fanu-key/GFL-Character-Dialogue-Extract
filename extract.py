# Import libraries
import os
import glob
import shutil

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

# Ascii handling, replace � with a space
fixedMerged = open('fixedMerged.txt', 'w+', encoding='utf8')

for line in allText:
    line.replace('�', ' ')
    fixedMerged.write(line)

# Extract all AK-12 dialogue and put into a text file
readFixedMerged = open('fixedMerged.txt', 'r+', encoding='utf8')
ak12Dialogue = open('ak12Dialogue.txt', 'w+', encoding='utf8')

for line in readFixedMerged:
    if line.startswith('AK-12:'):
        ak12Dialogue.write(line[7:])
        #ak12Dialogue.write(f"{line}\n")

# Close files so we can move them into folders
fixedMerged.close()
readFixedMerged.close()
ak12Dialogue.close()

# Move both fixedMerged and ak12Dialogue to their respective folders
fixedMergedSourceFolder = r'fixedMerged.txt'
ak12DialogueSourceFolder = r'ak12Dialogue.txt'

fixedMergedDestFolder = r'Output/Inputlines/fixedMerged.txt'
ak12DialogueDestFolder = r'Output/CharacterLines/ak12Dialogue.txt'

shutil.move(fixedMergedSourceFolder, fixedMergedDestFolder)
shutil.move(ak12DialogueSourceFolder, ak12DialogueDestFolder)

# I dont know how to convert dialogue text to csv without getting errors
# Just copy all text from text file and paste into csv