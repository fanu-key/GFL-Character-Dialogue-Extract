# Girl's Frontline (GFL) dialogue extract
Python code to extract dialogue spoken by a specified character from the hit game Girl's Frontline.

Just run extract.py

Disclaimers:
- Some characters speak under two names.
- For example: RO635 is both RO and RO635 in dialogue. Same problem for Ange, she is both Ange and Angelia.
- For this edge case, run the program again to cover dialogue for both aliases.

~~In theory this also works for other characters if you edit the code a bit~~

Works for all characters now yay!!!


All event text copy pasted from https://gfl.amaryllisworks.pw/
- Disclaimer: All chapters not included yet, im too lazy to copy them all.


To-Do (Most important to least important):
- ~~read all dialogue text files from separate folder (Prob have to import os)~~ done
- ~~output specific character dialogue text files to separate folder~~ done... kinda
- ~~handle ascii characters or at least this thing: �~~ done
- ~~figure out how to convert from text file to csv without errors~~ done
- ~~dynamic character dialogue extracting, specify which character to extract dialogue for on program start~~ done
- Still creates a dialogue file for characters that don't exist, if character does not exist -> dont make the file and quit program or return to beginning
- Maybe incorporate functions / defs
- GUI

![AK-12](https://cdn.discordapp.com/attachments/923718033942401065/1106834144849313792/upscaledAK12edit_2.png)

Was originally going to be used to extract only AK-12 dialogue.

But I figured I could do better than that.
