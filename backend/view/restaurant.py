from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

restaurant = Blueprint('restaurant', __name__)

@restaurant.route('/', methods=['GET'])
def get_restaurant():
    return jsonify({'msg': 'Get Restaurant list'})

@restaurant.route('/id=<string:restaurant_id>', methods=['GET'])
def get_restaurant_by_id(restaurant_id):
    return jsonify({'msg': 'Get Restaurant by id'})

@restaurant.route('/id=<string:restaurant_id>/menu', methods=['GET','POST'])
def get_menu():
    if request.method == 'GET':
        return jsonify({'msg': 'get the menu for the restaurant'})
    if request.method == 'POST':
        return jsonify({'msg': 'post the menu and update to database'})

@restaurant.route('/menu/ocr', methods=['POST'])
def ocr_menu():
    # get the picture of menu
    # throw into the ocr function
    return jsonify({'/msg': 'return ocr things'})

@restaurant.route('/random', methods=['GET'])
@jwt_required()
def get_random_restaurant():
    user = get_jwt_identity()
    # get the user's prefer
    # throw user's prefer into the model
    # return he may want to eat
    return jsonify({'msg': 'Get Random Restaurant'})

@restaurant.route('/specify', methods=['GET'])
@jwt_required()
def get_specify_restaurant():
    # get restaurant by specify conditions
    user = get_jwt_identity()
    # get the user's prefer
    # throw conditions and prefer into the model
    # return he may want to eat
    return jsonify({'msg': 'Get Specify Restaurant'})

