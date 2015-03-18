#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sys
from flask import Flask, render_template, request, jsonify
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import json
import tablib
import os

sys.path.insert(0, 'scripts/Team16')
sys.path.insert(0, 'scripts/KnowledgeBase')
from autograder import main as autograder_main
from scrape import get_recipe
from main import main


#import main
#from KnowledgeBase import *


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
#db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
dataset = tablib.Dataset()
with open(os.path.join(os.path.dirname(__file__),'scripts/Team16/parsegrades.csv')) as f:
    dataset.csv = f.read()

@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')

@app.route('/', methods=['POST'])
def home_post():
    recipe_url = request.form['recipe_url']
    mutation = request.form['transformation']
    #return json.dumps(main(mutation, recipe_url))
    #return jsonify(main(mutation, recipe_url))
    return recipe_submitted(mutation, recipe_url)

@app.route('/recipe', methods = ['POST'])
def recipe_submitted(mutation, recipe_url):
    recipe = get_recipe(recipe_url)
    new_recipe = main(mutation, recipe_url)
    context = {}
    context['recipe_url'] = recipe_url
    context['recipe_name'] = recipe['title']
    context['time'] = recipe['time']
    context['servings'] = recipe['servings']
    context['primary_cooking_method'] = recipe['primary cooking method']
    context['cooking_methods'] = recipe['cooking methods']
    context['cooking_tools'] = recipe['cooking tools']
    context['ingredients'] = (recipe['ingredients'])
    context['new_ingredients'] = (new_recipe['ingredients'])

    return render_template('pages/recipe.html', context = context)

@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')

@app.route('/autograder')
def autograde():
    return dataset.html

@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)



# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
