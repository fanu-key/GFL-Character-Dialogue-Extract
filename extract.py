from imports import *
from config import *

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