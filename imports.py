import os
import aiofiles
import time
import asyncio
import csv
from concurrent.futures import ThreadPoolExecutor
from quart import Quart
from config import dirPath, OUTPUT_CHARACTER_LINES, app