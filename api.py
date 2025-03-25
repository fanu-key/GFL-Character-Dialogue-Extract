from imports import *
from config import *

app = Quart(__name__)

@app.route('/')
async def hello():
    return 'hello'

# If you see this, don't pay attention, I just write code and it goes to the repository. Check back later!
app.run()
