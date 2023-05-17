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
    """ to test if database work
        ---
        Returns:
            * print `'test success'` and return true if it work
            * print `'test fail'` and return false if not
    """
    test_doc_ref = restaurant_collection.document('test')
    test_doc_ref.set({'test': 'test'})
    test_data = test_doc_ref.get().to_dict()
    if test_data['test'] == 'test':
        print('test success')
        return True
    else:
        print('test fail')
        return False


def create_restaurant(name: str, address: str, type: str, mean_price: float) -> str:
    """ create a restaurant data in database
        ---
        Args:
            name (str): restaurant name
            address (str): restaurant location
            type (str): restaurant type
            mean_price (float): the average price of this restaurant

        Returns:
            :class:`str`: the restaurant id
    """
    new_restaurant_dict = {'name': name, 'address': address,
                           'type': type, 'mean_price': mean_price}
    result = restaurant_collection.add(new_restaurant_dict)
    new_restaurant_ref: DocumentReference = result[1]
    return new_restaurant_ref.id


def update_restaurant(id: str, name: Union[str, None] = None, address: Union[str, None] = None,
                      type: Union[str, None] = None, mean_price: Union[float, None] = None):
    """update a existed restaurant data

    Args:
        id (str): the restaurant id
        name (Union[str, None], optional): restaurant name. would not update if not given.
        address (Union[str, None], optional): restaurant location. would not update if not given.
        type (Union[str, None], optional): restaurant type. would not update if not given.
        mean_price (Union[float, None], optional): the average price of this restaurant. would not update if not given.

    * Notice that if there is no data reference to the id, might have Error occur.
    """
    restaurant_ref = restaurant_collection.document(id)
    restaurant_dict = {}
    if name != None:
        restaurant_dict['name'] = name
    if address != None:
        restaurant_dict['address'] = address
    if type != None:
        restaurant_dict['type'] = type
    if mean_price != None:
        restaurant_dict['mean_price'] = mean_price
    restaurant_ref.update(restaurant_dict)


def get_restaurant(id: str) -> Union[Dict[str, Any], None]:
    """get a restaurant data

    Args:
        id (str): the restaurant id

    Returns:
        Union[Dict[str, Any], None]: a Dict if data found, None if not.
        keys are `'id'` `'name'` `'address'` `'type'` `'mean_price'`,
        values are the data correspounded.
    """
    restaurant_ref = restaurant_collection.document(id)
    restaurant_data = restaurant_ref.get().to_dict()
    restaurant_data['id'] = id
    return restaurant_data


def get_all_restaurant() -> List[Dict[str, Any]]:
    """get all restaurant data

    Returns:
        List[Dict[str, Any]]: a List contains several Dict.
        each Dict keys are `'id'` `'name'` `'address'` `'type'` `'mean_price'`,
        values are the data correspounded.
    """
    restaurant_ref_list: List[DocumentSnapshot] = restaurant_collection.get()
    restaurant_list = []
    for restaurant_ref in restaurant_ref_list:
        restaurant_list.append(get_restaurant(restaurant_ref.id))
    return restaurant_list


def delete_restaurant(id: str):
    """delete a restaurant data

    Args:
        id (str): the restaurant id
    """
    restaurant_ref = restaurant_collection.document(id)
    restaurant_ref.delete()


def create_food(belong_restaurant_id: str, name: str, type: str) -> str:
    """ create a food data in database
        ---
        Args:
            belong_restaurant_id (str): the id of the restaurant that this food belong to
            name (str): food name
            type (str): food type

        Returns:
            :class:`str`: the food id
    """
    new_food_dict = {'name': name, 'type': type,
                     'belong_restaurant_id': belong_restaurant_id}
    result = food_collection.add(new_food_dict)
    new_food_ref: DocumentReference = result[1]
    return new_food_ref.id


def update_food(id: str, belong_restaurant_id: Union[str, None], name: Union[str, None], type: Union[str, None]):
    """update a existed food data

    Args:
        id (str): the food id
        belong_restaurant_id (Union[str, None]): the id of the restaurant that this food belong to. would not update if not given.
        name (Union[str, None]): food name. would not update if not given.
        type (Union[str, None]): food type. would not update if not given.

    * Notice that if there is no data reference to the id, might have Error occur.
    """
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
    """get a food data

    Args:
        id (str): the food id

    Returns:
        Union[Dict[str, Any], None]: a Dict if data found, None if not.
        keys are `'id'` `'belong_restaurant_id'` `'name'` `'type'`,
        values are the data correspounded.
    """
    food_ref = food_collection.document(id)
    food_data = food_ref.get().to_dict()
    food_data['id'] = id
    return food_data


def get_all_food() -> List[Dict[str, Any]]:
    """get all food data

    Returns:
        List[Dict[str, Any]]: a List contains several Dict.
        each Dict keys are `'id'` `'belong_restaurant_id'` `'name'` `'type'`,
        values are the data correspounded.
    """
    food_ref_list: List[DocumentSnapshot] = food_collection.get()
    food_list = []
    for food_ref in food_ref_list:
        food_list.append(get_food(food_ref.id))
    return food_list


def delete_food(id: str):
    """delete a food data

    Args:
        id (str): the food id
    """
    food_ref = food_collection.document(id)
    food_ref.delete()


def create_user(account: str, password: str):
    """ create a user data in database
        ---
        Args:
            account (str): user account
            password (str): user password

        Returns:
            :class:`str`: the user id
    """
    new_user_dict = {'account': account, 'password': password}
    result = user_collection.add(new_user_dict)
    new_user_ref: DocumentReference = result[1]
    return new_user_ref.id


def update_user(id: str, account: Union[str, None] = None, password: Union[str, None] = None):
    """update a existed user data

    Args:
        id (str): the user id
        account (Union[str, None]): user account. would not update if not given.
        password (Union[str, None]): user password. would not update if not given.

    * Notice that if there is no data reference to the id, might have Error occur.
    """
    user_ref = user_collection.document(id)
    user_dict = {}
    if account != None:
        user_dict['account'] = account
    if password != None:
        user_dict['password'] = password
    user_ref.update(user_dict)


def get_user(id: str) -> Union[Dict[str, Any], None]:
    """get a user data

    Args:
        id (str): the user id

    Returns:
        Union[Dict[str, Any], None]: a Dict if data found, None if not.
        keys are `'id'` `'account'` `'password'`, values are the data correspounded.
    """
    user_ref = user_collection.document(id)
    user_data = user_ref.get().to_dict()
    user_data['id'] = id
    return user_data


def delete_user(id: str):
    """delete a user data

    Args:
        id (str): the user id
    """
    user_ref = user_collection.document(id)
    user_ref.delete()


def create_record(user_id: str, food_id: str):
    """ create a record data in database
        ---
        Args:
            user_id (str): the id of the user that create this this record
            food_id (str): the id of the food that the user search

        Returns:
            :class:`str`: the record id
    """
    new_record_dict = {'user_id': user_id, 'food_id': food_id}
    result = record_collection.add(new_record_dict)
    new_record_ref: DocumentReference = result[1]
    return new_record_ref.id


def update_record(id: str, user_id: Union[str, None], food_id: Union[str, None]):
    """update a existed usrecorder data

    Args:
        id (str): the record id
        user_id (str): the id of the user that create this this record. would not update if not given.
        food_id (str): the id of the food that the user search. would not update if not given.

    * Notice that if there is no data reference to the id, might have Error occur.
    """
    record_ref = record_collection.document(id)
    record_dict = {}
    if user_id != None:
        record_dict['user_id'] = user_id
    if food_id != None:
        record_dict['food_id'] = food_id
    record_ref.update(record_dict)


def get_record(id: str) -> Union[Dict[str, Any], None]:
    """get a record data

    Args:
        id (str): the record id

    Returns:
        Union[Dict[str, Any], None]: a Dict if data found, None if not.
        keys are `'id'` `'user_id'` `'food_id'`,
        values are the data correspounded.
    """
    record_ref = record_collection.document(id)
    record_data = record_ref.get().to_dict()
    record_data['id'] = id
    return record_data


def get_all_record() -> List[Dict[str, Any]]:
    """get all record data

    Returns:
        List[Dict[str, Any]]: a List contains several Dict.
        each Dict keys are `'user_id'` `'food_id'`,
        values are the data correspounded.
    """
    record_ref_list: List[DocumentSnapshot] = record_collection.get()
    record_list = []
    for record_ref in record_ref_list:
        record_list.append(get_record(record_ref.id))
    return record_list


def delete_record(id: str):
    """delete a record data

    Args:
        id (str): the record id
    """
    record_ref = record_collection.document(id)
    record_ref.delete()


def clear_record_where_user_is(user_id: str):
    """clear all record that involve a specific user

    Args:
        user_id (str): the user id
    """
    all_record = get_all_record()
    for record in all_record:
        if record['user_id'] == user_id:
            delete_food(record['id'])


def get_user_search_food_type_counts(user_id: str) -> Dict[str, int]:
    """ get the times of each food that have been searched by a specific user

    Args:
        user_id (str): the user id

    Returns:
        Dict[str, int]: keys is each type, values is the times been searched of the type
    """
    all_record = get_all_record()
    type_counts: Dict[str, int] = {}
    for record in all_record:
        food = get_food(record['food_id'])
        if food != None:
            if food['type'] not in type_counts.keys():
                type_counts[food['type']] = 0
            if record['user_id'] == user_id:
                type_counts[food['type']] += 1
    return type_counts


def get_user_search_restaurant_type_counts(user_id: str) -> Dict[str, int]:
    """ get the times of each restaurant that have been searched by a specific user

    Args:
        user_id (str): the user id

    Returns:
        Dict[str, int]: keys is each type, values is the times been searched of the type
    """
    all_record = get_all_record()
    type_counts: Dict[str, int] = {}
    for record in all_record:
        food = get_food(record['food_id'])
        restaurant = get_restaurant(food['belong_restaurant_id'])
        if restaurant != None:
            if restaurant['type'] not in type_counts.keys():
                type_counts[restaurant['type']] = 0
            if record['user_id'] == user_id:
                type_counts[restaurant['type']] += 1
    return type_counts
