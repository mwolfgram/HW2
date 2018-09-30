## SI 364
## Winter 2018
## HW 2 - Part 1
#matthew wolfgram

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required

import requests
import json

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################

class AlbumEntryForm(FlaskForm):
    album_name = StringField('enter the name of an album you like:')
    sentiment = RadioField('how do you feel about the album? (1 low, 3 high)', choices = [('1', '1'), ('2', '2'), ('3','3')], validators = [Required()])
    submit = SubmitField('submit')

####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

@app.route('/artistform')
def artist_form_function():
    return render_template('artistform.html')

@app.route('/artistinfo', methods = ['GET', 'POST'])
def artist_stuff():

    the_artist_name = request.args.get('artist', "")
    parameters = {'term' : the_artist_name, 'entity' : 'musicTrack'}
    baseurl = "https://itunes.apple.com/search?"
    itunes_response = requests.get(baseurl, params = parameters).json()['results']

    return render_template('artist_info.html', objects = itunes_response)

@app.route('/artistlinks')
def links():
    return render_template('artist_links.html')

@app.route('/specific/song/<artist_name>', methods = ['GET', 'POST'])
def specific_song(artist_name):
    parameters = {'term' : artist_name, 'entity' : 'musicTrack'}
    baseurl = "https://itunes.apple.com/search?"
    response = requests.get(baseurl, params = parameters).json()['results']
    return render_template('specific_artist.html', results = response)

@app.route('/album_entry')
def album_entry():
    album_entry_form = AlbumEntryForm()
    return render_template('album_entry.html', form = album_entry_form)

@app.route('/album_result', methods = ['GET', 'POST'])
def result_function():
    form = AlbumEntryForm()

    if request.method == 'POST' and form.validate_on_submit():
        album = form.album_name.data #from class!!
        likes = form.sentiment.data

        return render_template('album_data.html', album_name = album, sentiment = likes)

if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
