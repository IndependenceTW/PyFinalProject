from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity


auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET'])
@jwt_required()
def get_auth():
    identity = get_jwt_identity()
    if identity is not None:
        return jsonify({'msg': 'hello, ' + identity}), 200
    else:
        return jsonify({'msg': 'non-auth'}), 401

@auth.route('/login', methods=['POST'])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    # check the user is valid
    if username != 'test' or password != 'test':
        return jsonify({'msg': 'non-auth'}), 401

    token = create_access_token(identity=username)
    return jsonify({'token': token, 'user': username}), 200

@auth.route('/register', methods=['POST'])
def register():
    # check if user exists
    # if user is not exists, create user, return created code 201
    # if user is exists, return error code 409
    return jsonify({'msg': 'Register'})

@auth.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    # check if user exists
    # front-end should delete the token
    return jsonify({'msg': 'Logout'})

@auth.route('/new-token', methods=['GET'])
@jwt_required()
def new_token():
    identity = get_jwt_identity()
    if identity is not None:
        token = create_access_token(identity=identity)
        return jsonify({'msg': 'new token created, ' + identity, 'token': token}), 200
    else:
        return jsonify({'msg': 'non-auth'}), 401
