# All events + dialogue in order of timeline
singularity = open('singularity.txt', 'r', encoding="utf-8")
continuum = open('continuumTurbulence.txt', 'r', encoding="utf-8")
isomer = open('isomer.txt', 'r', encoding="utf-8")
shattered = open('shatteredConnexion.txt', 'r', encoding="utf-8")
polarized = open('polarizedLight.txt', 'r', encoding="utf-8")
dualRandomness = open('dualRandomness.txt', 'r', encoding="utf-8")
mirrorStage = open('mirrorStage.txt', 'r', encoding="utf-8")
adjutant = open('adjutantLines.txt', 'r', encoding="utf-8")

# Create text file to combine all event dialogue
outputAllEvents = open('allEvents.txt', 'w', encoding="utf-8")

allEvents = ['singularity.txt', 'continuumTurbulence.txt', 'isomer.txt', 
             'shatteredConnexion.txt', 'polarizedLight.txt', 'dualRandomness.txt', 
             'mirrorStage.txt', 'adjutantLines.txt']

# Combine event dialogue into one text file
for eventName in allEvents:
    with open(eventName, 'r', encoding="utf-8") as infile:
        for line in infile:
            outputAllEvents.write(line)

ak12Lines = []
ak12LinesNoAK12 = []

outputWith = open('ak12dialogueWithAK-12.txt', 'w')
outputWithout = open('ak12dialogueWithoutAK-12.txt', 'w')

readAllEvents = open('allEvents.txt', 'r', encoding="utf-8")

# Read AK-12: lines from all events and put into list
for line in readAllEvents:
    if line.startswith("AK-12:"):
        ak12Lines.append(line.rstrip('\n'))
        ak12LinesNoAK12.append(line.rstrip('\n')[7:])

# Manually adding adjutant lines to list because my code does not want to for some unknown reason, stupid fucking code work dammit
for line in adjutant:
    if line.startswith("AK-12:"):
        ak12Lines.append(line.rstrip('\n'))
        ak12LinesNoAK12.append(line.rstrip('\n')[7:])

# Write AK-12 lines to text file and include AK-12: part
for line in ak12Lines:
    outputWith.write(f"{line}\n")

# Write AK-12 lines to text file but excludes AK-12: part
for line in ak12LinesNoAK12:
    outputWithout.write(f"{line}\n")

# Close all files
singularity.close()
continuum.close()
isomer.close()
shattered.close()
polarized.close()
dualRandomness.close()
mirrorStage.close()
adjutant.close()

outputWith.close()
outputWithout.close()

readAllEvents.close()