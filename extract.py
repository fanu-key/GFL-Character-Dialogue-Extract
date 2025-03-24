# Import libraries
import os
import glob
import shutil
import pandas as pd
import sys
import threading
import time

def firearmFix(x):
    # Firearms copyright fix
    copyrightFix = x
    
    # If input character in list, append Gr to front
    hkFirarms = ['MP7', 'G41', 'G3', 'G36', 'Mk23', 'G36c',
                 'MG5', 'PSG-1', 'G11', 'MG4', 'USP Compact', 'G28',
                 'HK45', 'MG23', 'MG36', 'HK33', 'P30', 'SL8']
    
    # If input character in list, append FF to front
    fnFirearms = ['FN49', 'FNC', 'M249SAW', 'FNP9', 'F2000']
    
    # If input character in list, append Fr to front
    masFirearms = ['FAMAS']
    
    if copyrightFix in hkFirarms:
        copyrightFix = 'Gr {}'.format(copyrightFix)

    if copyrightFix in fnFirearms:
        copyrightFix = 'FF {}'.format(copyrightFix)

    if copyrightFix in masFirearms:
        copyrightFix = 'Fr {}'.format(copyrightFix)
    
    return copyrightFix

def continueQuestion():
    # Asks user if they would like to run the program again
    yesInput = ["YES", 'Y']
    noInput = ["NO", "N"]
    
    continueProgram = input("Would you like to extract again? [Y/N]: ")
    for accept in yesInput:
        if continueProgram.upper() == accept.upper():
            print("...Running Program Again...")
            main() # Run again if yes

    for decline in noInput:
        if continueProgram.upper() == decline.upper():
            print("...Exiting Program in 5 seconds...")
            time.sleep(5)
            sys.exit() # Exit if no

    else:
        print("...Invalid input...\n")
        continueQuestion() #Loop back if invalid input

def extract(x):
    # Start timer
    startTime = time.perf_counter()

    # Input for which character to extract dialogue for
    inputCharacter = x
    
    # Check if input included copyright fix
    inputCharacter = firearmFix(inputCharacter)

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
    #savePath = r'Output\InputLines'

    # This will list all text files in the input folder, only use for debugging
    """for file in glob.glob(dirPath, recursive=True):
        print(file)
    print('\n')"""

    # Read each text file in input folder and write each file to one big combined text file
    inputFolder = glob.glob(dirPath, recursive=True)
    mergedInput = open("merged.txt", "w+", encoding='utf8')
    
    # Threadlock to make sure all files are read
    lock = threading.Lock()
    lock.acquire()

    for file in inputFolder:
        with open('{}'.format(file), 'r+', encoding='utf8') as input:
            mergedInput.write(input.read())

    lock.release()
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
    
    charLinesCounter = 0

    # Threadlocking so we don't have a race condition error
    lock.acquire()

    for line in readFixedMerged:
        if line.startswith('{}:'.format(inputCharacter)):
            index = line.find(characterCheck)
            characterDialogue.write(line[index + 2:])
            characterLines.append(line[index + 2:].rstrip('\n'))
            charLinesCounter += 1
            #ak12Dialogue.write(f"{line}\n")
            
    characterDialogue.close()
    lock.release()
    
    print("Total {} lines extracted:".format(inputCharacter), charLinesCounter)

    # Reading all lines in characterLines for debugging
    """for lines in characterLines:
        print(lines)"""

    # This shit is the reason why some characters did not work for extraction
    # Commenting until I can fix it (May 13 2023)
    # May 15 2023 - Fixed it
    # Possible explanation after sleeping on it: Race condition
    # Check if text file is empty, if yes delete file and exit program
    if os.path.getsize('{}_Dialogue.txt'.format(inputCharacter)) == 0:
        print('{} does not exist in story files. Dialouge file is empty. Check if input is typed correctly\n'.format(inputCharacter))
        os.remove('{}_Dialogue.txt'.format(inputCharacter))
        continueQuestion()

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
        print('Extract Failure.\n')
        
    # Print out total time program takes to execute
    endTime = time.perf_counter()
    elapsedTime = str(endTime - startTime)
    print(elapsedTime[:7], 'seconds to extract.\n')

    continueQuestion()

def main():
    # Input for which character to extract dialogue for
    inputCharacter = input('\nEnter character name: ')
    extract(inputCharacter)

if __name__ == "__main__":
    main()
