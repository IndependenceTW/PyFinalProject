from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import functions.database as db
import functions.ocr_menu as ocr
import PIL.Image as Image
from model.recommendation import RecommendationSystem

restaurant = Blueprint('restaurant', __name__)
recommendation = RecommendationSystem();

@restaurant.route('/', methods=['GET'])
def restaurants():
    list = db.get_all_restaurant()
    json = jsonify(list)
    return json, 200

@restaurant.route('/', methods=['POST'])
@jwt_required()
def create_restaurant():
    data = request.get_json()
    db.create_restaurant(data['name'], data['address'], data['type'], data['price'])
    return jsonify({'msg': 'post the restaurant and update to database'}), 201;

        
@restaurant.route('/id=<string:restaurant_id>', methods=['GET'])
def get_restaurant_by_id(restaurant_id):
    info = db.get_restaurant(id=restaurant_id)
    return jsonify(info), 200

@restaurant.route('/id=<string:restaurant_id>/menu', methods=['GET'])
def get_menu(restaurant_id):
    all_foods = db.get_all_food()
    foods = []
    for food in all_foods:
        if food['belong_restaurant_id'] == restaurant_id:
            foods.append(food)
    return jsonify(foods), 200


@restaurant.route('/id=<string:restaurant_id>/menu', methods=['POST'])
def add_food(restaurant_id):
    # TODO
    return jsonify({'msg': 'post the menu and update to database'})

@restaurant.route('/menu/ocr', methods=['POST'])
def ocr_menu():
    # get the picture of menu
    # throw into the ocr function
    img = request.files['img']
    img = Image.open(img)
    dishs = ocr.menu_img(img)
    return jsonify(dishs), 200

@restaurant.route('/random', methods=['GET'])
@jwt_required()
def get_random_restaurant():
    user = get_jwt_identity()
    list = recommendation.recommend(user_id=user)
    return jsonify(list), 200

@restaurant.route('/specify', methods=['GET'])
@jwt_required()
def get_specify_restaurant():
    # get restaurant by specify conditions
    user = get_jwt_identity()
    data = request.get_json()
    list = recommendation.recommend(user_id=user, restaurant_options={'restaurant_type': data.type, 'mean_price': data.mean_price}) #TODO get the specify conditions from the request
    return jsonify({'msg': 'Get Specify Restaurant'})

@restaurant.route('/record', methods=['POST'])
@jwt_required()
def record_food():
    user = get_jwt_identity()
    data = request.get_json()
    restaurant_id = data.restaurant_id
    choice = data.choice
    db.create_record(user, restaurant_id)
    recommendation.update_results(user_id=user, choice=choice) 
    return jsonify({'msg': 'recorded'}), 200


