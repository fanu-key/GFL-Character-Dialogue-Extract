# Girl's Frontline (GFL) Character Dialogue Extract – Async Edition with Planned Analytics

This project extracts dialogue spoken by a specified character from the game **Girl's Frontline**. Our new asynchronous version dramatically improves performance and code clarity while maintaining the original functionality. In addition, we plan to add advanced analytics (e.g., verbosity, word frequency) in future releases.

---

## What’s Implemented

- **Asynchronous File Operations**  
  - Uses `asyncio` and `aiofiles` to asynchronously search for, read, and write text files.
  - Offloads CSV writing to a separate thread (using `ThreadPoolExecutor`) to avoid blocking the main async loop.

- **Flexible Character Name Handling**  
  - Converts both user input and dictionary keys to lowercase for case-insensitive matching.
  - Supports partial matches (e.g., input “usp” returns “Gr USP Compact”), while preserving the original formatting from the dictionary.

- **Workflow Orchestration**  
  - Modular functions to search files, read file content, extract dialogue lines (removing unwanted symbols like `�`), and write outputs.
  - The overall workflow is coordinated by an asynchronous `task_scheduler` function.

- **Improved Error Handling & Directory Setup**  
  - The `make_dir` function creates the output directory with error handling (handling `FileExistsError`, `PermissionError`, etc.) and provides informative messages in our signature “Commander!” style.

- **User Interaction**  
  - Uses synchronous `input()` calls for user prompts (acceptable for this console-based use case).
  - After processing, the user is asked whether to extract dialogue again.

- **Performance Boost**  
  - The asynchronous version is approximately 2.5× faster than the previous synchronous implementation.

---

## Planned & Future Features

- **Analytics on Dialogue Data**  
  - *Verbosity Measurement*: Calculate and compare the average number of words per dialogue line for each character.
  - *Word Frequency Analysis*: Identify the most frequently used words by a character (with stop-word filtering)..
  - *Event-based Grouping*: Group dialogues by event to analyze character activity during different in-game scenarios.
  - etc...

- **Additional Export Options**  
  - Extend output formats (e.g., JSON) for easier integration with further analytical tools.

---

## How to Use

1. **Run the Program:**  
   Run the script via command line:  
   ```bash
   python your_script_name.py
   ```

2. Enter a Character Name:

3.Input is flexible—case-insensitive and supports partial names (e.g., type "famas" or "usp").

Outputs Generated:

A text file (*_Dialogue.txt) containing the extracted dialogue.

A CSV file (*_Dialogue.csv) with structured dialogue data.

(Future releases: additional analytics outputs)

Technical Details
Asynchronous Architecture:
All file operations (search, read, write) are performed asynchronously to minimize waiting time during I/O.

Modular Workflow:
Functions are separated into small, single-responsibility components for improved maintainability and readability.

Enhanced Character Lookup:
The copyright_fix function uses a case-insensitive lookup with partial-match support to ensure that user input like “usp” correctly matches “USP Compact” and returns it in its original format.

Error Handling:
Specific exceptions (e.g., FileExistsError, PermissionError, OSError) are handled with themed messages, ensuring the user receives clear feedback if something goes wrong.

Conclusion
This refactored asynchronous version not only improves performance and code readability but also lays the groundwork for advanced dialogue analysis features. While the current version focuses on extraction and basic file output, planned future enhancements (analytics, additional export formats, GUI) will make this tool even more valuable.

“Because why settle for clunky synchronous code when you can have an async masterpiece with room to grow?”

Feel free to open issues or contribute further improvements!
