from flask import Blueprint, request, jsonify

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET'])
def get_auth():
    # check if the token is in the database
    return jsonify({'msg': 'Get Auth'})

@auth.route('/login', methods=['POST'])
def login():
    # create a token and store it in the database
    # return the token and user id
    return jsonify({'msg': 'Login'})

@auth.route('/register', methods=['POST'])
def register():
    # check if user exists
    return jsonify({'msg': 'Register'})

@auth.route('/logout', methods=['GET'])
def logout():
    # need to check if the token is in the database
    # delete the token from the database
    return jsonify({'msg': 'Logout'})

@auth.route('/new-token', methods=['GET'])
def new_token():
    # check if the token is in the database
    # return a new token
    return jsonify({'msg': 'New Token'})
