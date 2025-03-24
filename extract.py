import os
import aiofiles
import time
import asyncio
import csv

OUTPUT_CHARACTER_LINES = r'./Output/CharacterLines'
dirPath = r'Input'

# Fixing character name to include firearm origin for clarity (e.g., MP7 becomes "Gr MP7")
async def copyright_fix(char_name: str) -> str:
    char_name_lower = char_name.lower()

    firearms_dict = {
        'MP7': 'Gr', 'G41': 'Gr', 'G3': 'Gr', 'G36': 'Gr', 'Mk23': 'Gr', 'G36c': 'Gr',
        'MG5': 'Gr', 'PSG-1': 'Gr', 'G11': 'Gr', 'MG4': 'Gr', 'USP Compact': 'Gr', 'G28': 'Gr',
        'HK45': 'Gr', 'MG23': 'Gr', 'MG36': 'Gr', 'HK33': 'Gr', 'P30': 'Gr', 'SL8': 'Gr',
        'FN49': 'FF', 'FNC': 'FF', 'M249SAW': 'FF', 'FNP9': 'FF', 'F2000': 'FF',
        'FAMAS': 'Fr'
    }

    firearms_dict_lower = {key.lower(): key for key in firearms_dict}

    for key in firearms_dict_lower:
        if char_name_lower in key:  # "usp" === "USP Compact"
            original_name = firearms_dict_lower[key]
            return f"{firearms_dict[original_name]} {original_name}"

    return char_name


# At breakneck speed (almost) we search for txt files
async def search_files() -> list:
    loop = asyncio.get_event_loop()
    files = await loop.run_in_executor(None, lambda: [
    os.path.join(root, file) 
    for root, _, filenames in os.walk(dirPath) 
    for file in filenames if file.endswith(".txt")
])
    return files

# We read files into memory at the same speed
async def read_files(files: list) -> list:
    content_in_files = []

    for file_path in files:
        async with aiofiles.open(file_path, mode='r', encoding='utf-8') as file:
            content = await file.read()
            content_in_files.append(content)

    return content_in_files

# Extract lines where the character speaks, removing any unwanted symbols (like '�')
async def extract_lines(character_name: str, content: list) -> list:
    character_lines = []
    count_lines = 0

    for chapter in content:
        for line in chapter.split("\n"):
            if line.startswith(f"{character_name}:"):
                line.replace('�', ' ')
                character_lines.append(line.split(":", 1)[1].strip())
                count_lines += 1

    return character_lines, count_lines

# Synchronously write to a CSV file in a separate thread to avoid blocking the main thread
def write_csv_sync(file_path, content):
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for line in content:
            writer.writerow([line])

# We write txt and csv files at a furious speed (probably)
async def write_files(character_name: str, character_content: list):
    async with aiofiles.open(f"{OUTPUT_CHARACTER_LINES}/{character_name}_Dialogue.txt", mode='w', encoding='utf-8') as file:
        await file.write("\n".join(character_content))

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, write_csv_sync, f"{OUTPUT_CHARACTER_LINES}/{character_name}_Dialogue.csv", character_content)

# Manage tasks like Caesar, call all the necessary functions
# Orchestrate the entire workflow: fix character name, search files, extract lines, and write output
async def task_scheduler(character_name: str) -> str:
    character_name = await copyright_fix(character_name)
    files = await search_files()
    content = await read_files(files)
    character_content, count_lines = await extract_lines(character_name, content)
    await write_files(character_name, character_content)

    return count_lines

# We could have simply included main() in the While loop, but it was decided that making a separate function would be more interesting and convenient
# Separate this function to allow the user to easily continue the process or quit
async def continue_main():
    yesInput = ["yes", 'y']


    continueProgram = input("Would you like to extract again? [Y/N]: ")
    if continueProgram.lower() not in yesInput:
        print("Okay, Goodbye, Commander!")
        return
    
    print("\nOkay, Commander, let's do it again!\n")
    await main()

# And let's make another asynchronous synchronous function with input! Yes, we just create a folder and do checks
# Create output directory if it doesn't already exist, with error handling
async def make_dir():
    try:
        os.makedirs(OUTPUT_CHARACTER_LINES)
    except FileExistsError:
        pass
    except PermissionError:
        print("Oh... Commander, You don't have permission to create the directory.")
    except OSError as e:
        print(f"Commaaaaander! Operating system error occurred: {e}")
    except Exception as e:
        print(f"Commaaaaander! An unexpected error occurred: {e}")

# The entry point to our program, we will calculate the execution time (which is ~2.5 times less compared to the previous synchronous version)
# Main entry point of the program. Calculates execution time and orchestrates the entire flow
async def main():
    await make_dir()

    character_name = input('\nEnter character name: ')
    print("\n\nThank you, Commander!\n\n")

    startTime = time.perf_counter()

    count_lines = await task_scheduler(character_name)
    print("\n\nCommander! All tasks were completed on time!\n\n")
    print("Total {} lines extracted:".format(character_name), count_lines)

    endTime = time.perf_counter()
    elapsedTime = str(endTime - startTime)
    print(elapsedTime[:3], 'seconds to extract.\n')

    await continue_main()

if __name__ == "__main__":
    asyncio.run(main())
