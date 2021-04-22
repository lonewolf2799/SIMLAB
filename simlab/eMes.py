

import pandas as pd
from flask import render_template, redirect, url_for, flash, abort, request
import numpy as np

import random





@app.route('/test', methods=['GET','POST'])
def test():
    global abc
    global val
    global dd
    if request.method=='POST':
        if request.form.get('number7'):
            if dd=="":
                dd="disabled"
            else:
                dd=""
            return redirect('/test')
        else:
            abc+=1
            val=request.form['number67']
            return redirect('/test')
    return render_template('test.html', title='TEST', abc=abc, val=val, dd=dd)
