from flask import Blueprint, request, jsonify

restaurant = Blueprint('restaurant', __name__)

@restaurant.route('/', methods=['GET'])
def get_restaurant():
    return jsonify({'msg': 'Get Restaurant list'})

@restaurant.route('/<int:restaurant_id>', methods=['GET'])
def get_restaurant_by_id(restaurant_id):
    return jsonify({'msg': 'Get Restaurant by id'})

@restaurant.route('/random', methods=['GET'])
def get_random_restaurant():
    return jsonify({'msg': 'Get Random Restaurant'})

@restaurant.route('/specify', methods=['GET'])
def get_specify_restaurant():
    # get restaurant by specify conditions
    return jsonify({'msg': 'Get Specify Restaurant'})