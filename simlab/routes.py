from flask import render_template, redirect, url_for, flash, abort

from simlab import app

@app.route('/')
def landing_page():
    return render_template('landing.html')


@app.route('/home')
def home():
    return render_template('home.html', title='HOME')
    
    
# in the same fashion go on adding respective html files and route to run that
