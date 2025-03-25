from imports import *
from config import *
from api import app
from extract import *

config = Config()
config.bind = ["0.0.0.0:5000"]
if __name__ == "__main__":
    print("-------------------------------")
    print("\n\n Commander, open the site http://localhost:5000/ or you can open extractCLI.py if you are sick of sites. \n\n")
    print("-------------------------------")
    asyncio.run(serve(app, config))