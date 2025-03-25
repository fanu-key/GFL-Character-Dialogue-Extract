from imports import *
from config import *

app = Quart(__name__)

@app.route('/')
async def home():
    return await render_template('home.html')

@app.route('/extract', methods=['POST'])
async def extract():
    form = await request.form

    character_name = form.get('character')
    if not character_name:
        return redirect(url_for('home'))
    
    result = "Okay, puppy, just wait..."
    return result

# If you see this, don't pay attention, I just write code and it goes to the repository. Check back later!
app.run()
