from imports import *
from config import *

app = Quart(__name__)

@app.route('/')
async def hello():
    return 'hello'

app.run()
