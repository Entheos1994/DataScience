from flask import render_template, request, Response
from app import app
from cuisine import recipe_cuisine
import recipe_suggestion
import os
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

@app.route('/cuisine', methods=['POST'])
def cuisine():
    if request.method == 'POST':

        recipe_name = request.form['recipe_name']
        cuisine = recipe_cuisine.cuisine_relate(str(recipe_name))
        resp = Response(response=cuisine,
                        status=200,
                        mimetype="application/json")
        return resp
