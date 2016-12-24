from flask import render_template, request
from app import app
import json

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/recipe', methods=['POST'])
def recipe():
    if request.method == 'POST':
        recipe = request.form['recipe_name']
        return recipe
