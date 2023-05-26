from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from functions.database import get_user, create_user, get_user_id_by_account

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
    user = get_user_id_by_account(username)
    # # if user is not exist, return error code 401
    print(user)
    if user == None:
        return jsonify({'msg': 'no such account'}), 401
    # if user is exist, check the password
    if user['password'] != password:
        return jsonify({'msg': 'Invalid username or password'}), 401

    token = create_access_token(identity=user['id'])
    return jsonify({'token': token, 'user': username, 'id': user['id']}), 200

@auth.route('/register', methods=['POST'])
def register():
    # check if user exists
    user = get_user_id_by_account(request.json.get("username"))
    # if user is not exists, create user, return created code 201
    if user == None:
        id = create_user(request.json.get("username"), request.json.get("password"))
        return jsonify({'msg': 'created', 'id': id}), 201
    # if user is exists, return error code 409
    else: 
        return jsonify({'msg': 'User already exists'}), 409

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
