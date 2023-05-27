from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS

jwt = JWTManager()
app = Flask(__name__)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_SECRET_KEY'] = "not-secret"
jwt.init_app(app)
CORS(app)

@app.route('/')
def hello():
    return 'hello'

from view.auth import auth
app.register_blueprint(auth, url_prefix='/auth')
from view.restaurant import restaurant
app.register_blueprint(restaurant, url_prefix='/restaurant')
