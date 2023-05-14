# Import libraries
import os
import glob
import shutil
import pandas as pd

# Make directories for output
pathOutputInput = './Output/InputLines'
pathOutputCharacter = './Output/CharacterLines'

try:
    os.makedirs(pathOutputInput)
    os.makedirs(pathOutputCharacter)
except FileExistsError:
    print('Folders already exist.')
    
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

# Ascii handling, replace � with a space
fixedMerged = open('fixedMerged.txt', 'w+', encoding='utf8')

for line in allText:
    line.replace('�', ' ')
    fixedMerged.write(line)

# Extract all AK-12 dialogue and put into a text file and into a list
readFixedMerged = open('fixedMerged.txt', 'r+', encoding='utf8')
ak12Dialogue = open('ak12Dialogue.txt', 'w+', encoding='utf8')
ak12Lines = []

for line in readFixedMerged:
    if line.startswith('AK-12:'):
        ak12Dialogue.write(line[7:])
        ak12Lines.append(line[7:].rstrip('\n'))
        #ak12Dialogue.write(f"{line}\n")

"""# Reading all lines in ak12Lines for debugging
for lines in ak12Lines:
    print(lines)"""

# Convert lines in list to csv file
ak12Csv = open('ak12Dialogue.csv', 'w+', encoding='utf8')

dataFrame = pd.DataFrame(data=ak12Lines)
dataFrame.to_csv('ak12Dialogue.csv', header=False, index=False, encoding='utf8')

# Close files so we can move them into folders
fixedMerged.close()
readFixedMerged.close()
ak12Dialogue.close()
ak12Csv.close()
mergedInput.close()
allText.close()

# Move fixedMerged, ak12Dialogue.txt, and ak12Dialogue.csv to their respective folders
fixedMergedSourceFolder = r'fixedMerged.txt'
ak12DialogueTxtSourceFolder = r'ak12Dialogue.txt'
ak12DialogueCsvSourceFolder = r'ak12Dialogue.csv'

fixedMergedDestFolder = r'Output/Inputlines/fixedMerged.txt'
ak12DialogueTxtDestFolder = r'Output/CharacterLines/ak12Dialogue.txt'
ak12DialogueCsvDestFolder = r'Output/CharacterLines/ak12Dialogue.csv'

shutil.move(fixedMergedSourceFolder, fixedMergedDestFolder)
shutil.move(ak12DialogueTxtSourceFolder, ak12DialogueTxtDestFolder)
shutil.move(ak12DialogueCsvSourceFolder, ak12DialogueCsvDestFolder)

success=True

# If success, print message to console, else print failure
if success==True:
    print("Extract Success. Check Output folder.")

if success==False:
    print('Extract Failure.')