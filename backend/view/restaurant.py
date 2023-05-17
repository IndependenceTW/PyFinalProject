from flask import Blueprint, request, jsonify

restaurant = Blueprint('restaurant', __name__)

@restaurant.route('/', methods=['GET'])
def get_restaurant():
    return jsonify({'msg': 'Get Restaurant list'})

@restaurant.route('/id=<string:restaurant_id>', methods=['GET'])
def get_restaurant_by_id(restaurant_id):
    return jsonify({'msg': 'Get Restaurant by id'})

@restaurant.route('/menu', methods=['GET','POST'])
def get_menu():
    if request.method == 'GET':
        return jsonify({'msg': 'get the menu'})
    if request.method == 'POST':
        return jsonify({'msg': 'post the menu and update to database'})

@restaurant.route('/menu/ocr', methods=['GET'])
def ocr_menu():
    # get the picture of menu
    # throw into the ocr function
    return jsonify({'/msg': 'return ocr things'})

@restaurant.route('/random', methods=['GET'])
def get_random_restaurant():
    return jsonify({'msg': 'Get Random Restaurant'})

@restaurant.route('/specify', methods=['GET'])
def get_specify_restaurant():
    # get restaurant by specify conditions
    return jsonify({'msg': 'Get Specify Restaurant'})

