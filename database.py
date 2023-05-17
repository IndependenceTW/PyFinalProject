from typing import Any, Dict, List, Union
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.client import Client
from google.cloud.firestore_v1.document import DocumentReference
from google.cloud.firestore_v1.base_document import DocumentSnapshot


cred = credentials.Certificate('serviceAccount.json')
firebase_admin.initialize_app(cred)
db: Client = firestore.client()
restaurant_collection = db.collection('restaurant')
food_collection = db.collection('food')
user_collection = db.collection('user')
record_collection = db.collection('record')


def test():
    test_doc_ref = restaurant_collection.document('test')
    test_doc_ref.set({'test': 'test'})
    test_data = test_doc_ref.get().to_dict()
    if test_data['test'] == 'test':
        print('test success')
    else:
        print('test fail')


def create_restaurant(name: str, address: str, type: str, mean_price: float) -> str:
    new_restaurant_dict = {'name': name, 'addr': address,
                           'type': type, 'mean_price': mean_price}
    result = restaurant_collection.add(new_restaurant_dict)
    new_restaurant_ref: DocumentReference = result[1]
    return new_restaurant_ref.id


def update_restaurant(id: str, name: Union[str, None] = None, address: Union[str, None] = None,
                      type: Union[str, None] = None, mean_price: Union[float, None] = None):
    restaurant_ref = restaurant_collection.document(id)
    restaurant_dict = {}
    if name != None:
        restaurant_dict['name'] = name
    if address != None:
        restaurant_dict['addr'] = address
    if type != None:
        restaurant_dict['type'] = type
    if mean_price != None:
        restaurant_dict['mean_price'] = mean_price
    restaurant_ref.update(restaurant_dict)


def get_restaurant(id: str) -> Union[Dict[str, Any], None]:
    restaurant_ref = restaurant_collection.document(id)
    restaurant_data = restaurant_ref.get().to_dict()
    return restaurant_data


def get_all_restaurant() -> List[Dict[str, Any]]:
    restaurant_ref_list: List[DocumentSnapshot] = restaurant_collection.get()
    restaurant_list = []
    for restaurant_ref in restaurant_ref_list:
        restaurant_list.append(restaurant_ref.to_dict())
    return restaurant_list


def delete_restaurant(id: str):
    restaurant_ref = restaurant_collection.document(id)
    restaurant_ref.delete()


def create_food(belong_restaurant_id: str, name: str, type: str) -> str:
    new_food_dict = {'name': name, 'type': type,
                     'belong_restaurant_id': belong_restaurant_id}
    result = food_collection.add(new_food_dict)
    new_food_ref: DocumentReference = result[1]
    return new_food_ref.id


def update_food(id: str, belong_restaurant_id: Union[str, None], name: Union[str, None], type: Union[str, None]):
    food_ref = food_collection.document(id)
    food_dict = {}
    if belong_restaurant_id != None:
        food_dict['belong_restaurant_id'] = belong_restaurant_id
    if name != None:
        food_dict['name'] = name
    if type != None:
        food_dict['type'] = type
    food_ref.update(food_dict)


def get_food(id: str) -> Union[Dict[str, Any], None]:
    food_ref = food_collection.document(id)
    food_data = food_ref.get().to_dict()
    return food_data


def get_all_food() -> List[Dict[str, Any]]:
    food_ref_list: List[DocumentSnapshot] = food_collection.get()
    food_list = []
    for food_ref in food_ref_list:
        food_list.append(food_ref.to_dict())
    return food_list


def delete_food(id: str):
    food_ref = food_collection.document(id)
    food_ref.delete()


def create_user(account: str, password: str):
    new_user_dict = {'account': account, 'password': password}
    result = user_collection.add(new_user_dict)
    new_user_ref: DocumentReference = result[1]
    return new_user_ref.id


def update_user(id: str, account: Union[str, None] = None, password: Union[str, None] = None):
    user_ref = user_collection.document(id)
    user_dict = {}
    if account != None:
        user_dict['account'] = account
    if password != None:
        user_dict['password'] = password
    user_ref.update(user_dict)


def get_user(id: str) -> Union[Dict[str, Any], None]:
    user_ref = user_collection.document(id)
    user_data = user_ref.get().to_dict()
    return user_data

# def get_all_user() -> List[Dict[str, Any]]:
#     user_ref_list: List[DocumentSnapshot] = user_collection.get()
#     user_list = []
#     for user_ref in user_ref_list:
#         user_list.append(user_ref.to_dict())
#     return user_list


def delete_user(id: str):
    user_ref = user_collection.document(id)
    user_ref.delete()


def create_record(user_id: str, food_id: str):
    new_record_dict = {'user_id': user_id, 'food_id': food_id}
    result = record_collection.add(new_record_dict)
    new_record_ref: DocumentReference = result[1]
    return new_record_ref.id


def update_record(id: str, user_id: Union[str, None], food_id: Union[str, None]):
    record_ref = record_collection.document(id)
    record_dict = {}
    if user_id != None:
        record_dict['user_id'] = user_id
    if food_id != None:
        record_dict['food_id'] = food_id
    record_ref.update(record_dict)


def get_record(id: str) -> Union[Dict[str, Any], None]:
    record_ref = record_collection.document(id)
    record_data = record_ref.get().to_dict()
    return record_data


def get_all_record() -> List[Dict[str, Any]]:
    record_ref_list: List[DocumentSnapshot] = record_collection.get()
    record_list = []
    for record_ref in record_ref_list:
        record_list.append(record_ref.to_dict())
    return record_list


def delete_record(id: str):
    record_ref = record_collection.document(id)
    record_ref.delete()
