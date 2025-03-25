from imports import *
from config import *
from extract import *

app = Quart(__name__)

@app.route('/')
async def home():
    return await render_template('home.html')

@app.route('/extract', methods=['POST'])
async def extract():
    form = await request.form
    character_name = form.get('character')
    
    if not character_name:
        return jsonify({'error': 'Character name is required'}), 400
    
    try:
        count_lines = await task_scheduler(character_name)
        return jsonify({
            'character': character_name,
            'lines_extracted': count_lines
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

