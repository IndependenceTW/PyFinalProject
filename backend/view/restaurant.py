from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import functions.database as db
import functions.ocr_menu as ocr
import PIL.Image as Image
from model.recommendation import RecommendationSystem

restaurant = Blueprint('restaurant', __name__)
recommendation = RecommendationSystem();

@restaurant.route('/', methods=['GET'])
def get_all_restaurant():
    list = db.get_all_restaurant()
    json = jsonify(list)
    return json, 200

@restaurant.route('/id=<string:restaurant_id>', methods=['GET'])
def get_restaurant_by_id(restaurant_id):
    info = db.get_restaurant(id=restaurant_id)
    return jsonify(info), 200

@restaurant.route('/id=<string:restaurant_id>/menu', methods=['GET','POST'])
def get_menu(restaurant_id):
    if request.method == 'GET':
        all_foods = db.get_all_food()
        foods = []
        for food in all_foods:
            if food['restaurant_id'] == restaurant_id:
                foods.append(food)
        return jsonify(foods), 200

    if request.method == 'POST':
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
    # get the user's prefer
    # throw user's prefer into the model
    recommendation.recommend(user_id=user)
    # return he may want to eat
    return jsonify({'msg': 'Get Random Restaurant'})

@restaurant.route('/specify', methods=['GET'])
@jwt_required()
def get_specify_restaurant():
    # get restaurant by specify conditions
    user = get_jwt_identity()
    restaurant_list = recommendation.recommend(user_id=user, restaurant_options={'restaurant_type': '麵食', 'mean_price': 1}) #TODO get the specify conditions from the request
    return jsonify({'msg': 'Get Specify Restaurant'})

@restaurant.route('/restaurant=<string:restaurant_id>/record', methods=['POST'])
@jwt_required()
def record_food(restaurant_id):
    user = get_jwt_identity()
    # record the food the user eat
    db.create_record(user, restaurant_id)
    recommendation.update_results(user_id=user, choice=1) # TODO choice should be the food's number
    # return the food's information
    return {}, 200


