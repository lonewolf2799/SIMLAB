import os
from flask import Flask
import secrets



app= Flask(__name__, static_url_path='/static')

app.config['SECRET_KEY']=secrets.token_hex(16)





from simlab import routes