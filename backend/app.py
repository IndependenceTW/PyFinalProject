from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'hello'

from view.auth import auth
app.register_blueprint(auth, url_prefix='/auth')
from view.restaurant import restaurant
app.register_blueprint(restaurant, url_prefix='/restaurant')
