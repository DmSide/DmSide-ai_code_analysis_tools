from pymongo import MongoClient
from mongo_config import MONGO
from bson import ObjectId
import os
from overall_request import overall_request


def set_template(db, collection, fields):
    doc = dict()
    for field in fields:
        doc[field[0]] = field[1]
    db[collection].insert_one(doc)


def pagination(db, collection, page_size, page_number=1, start=None):
    total = db[collection].count()
    pages_number = divmod(total, page_size)
    pages_number = pages_number[0] + (pages_number[1] != 0)

    if start is not None:
        start_page = divmod(start, page_size)
        start_page = start_page[0] + (start_page[1] != 0)

        page_number = start_page

        if page_number > pages_number:
            page_number = pages_number

    if page_number > pages_number:
        print('Over page limit')
        return []

    skips = page_size * (page_number - 1)
    cursor = db[collection].find().skip(skips).limit(page_size)
    return list(cursor)


def get_languages_list(params, config=MONGO['git_info'],):

    limit = 50
    start = None

    if 'start' in params:
        start = params['start']

    if 'limit' in params:
        limit = params['limit']

    mongodb = MongoClient(host=config['mongo_host'])
    db = mongodb[config['database']]
    collection = config['languages_collection']

    languages_list = pagination(db, collection, limit, start=start)

    return languages_list


def add_language(params, config=MONGO['git_info']):

    if 'name' not in params:
        raise EnvironmentError('request must contain language name')

    tags = []
    if 'tags' in params:
        tags = params['tags']

    extensions = []
    if 'extensions' in params:
        extensions = params['extensions']

    mongodb = MongoClient(host=config['mongo_host'])
    db = mongodb[config['database']]
    collection = db[config['languages_collection']]

    look = collection.find_one({'name': params['name']})

    if not look:
        doc = {'name': params['name'], 'extensions': extensions, 'tags': tags}

        return collection.insert_one(doc).inserted_id
    else:
        return None


def remove_language(params, config=MONGO['git_info']):

    if 'id' not in params:
        raise EnvironmentError('request must contain language id')

    mongodb = MongoClient(host=config['mongo_host'])
    db = mongodb[config['database']]
    collection = db[config['languages_collection']]

    return collection.delete_one({'_id': ObjectId(params['id'])}).deleted_count


def update_language(params, config=MONGO['git_info']):

    if 'id' not in params:
        raise EnvironmentError('request must contain language id')

    mongodb = MongoClient(host=config['mongo_host'])
    db = mongodb[config['database']]
    collection = db[config['languages_collection']]

    language = collection.find_one({'_id': ObjectId(params['id'])})

    renovate = {}

    if 'name' in params:
        if language['name'] != params['name']:
            renovate.update({'name': params['name']})
    if 'extensions' in params:
        if language['extensions'] != params['extensions']:
            renovate.update({'extensions': params['extensions']})
    if 'tags' in params:
        if language['tags'] != params['tags']:
            renovate.update({'tags': params['tags']})

    collection.update_one({'_id': language['_id']}, {"$set": renovate})


def prepare_db(db_params_name):
    if 'name' not in db_params_name:
        raise EnvironmentError('request must contain name')
    params = MONGO[db_params_name['name']]
    client = MongoClient(params['mongo_host'])

    db_name = params['database']
    if not check_db(db_name):
        db = client[db_name]
    else:
        db = client[db_name]

    coll_name = params['items_collection']
    if coll_name not in db.collection_names():
        coll = db[coll_name]
    if 'fields' in params:
        set_template(db, coll_name, params['fields'])

    coll_name = params['languages_collection']
    if coll_name not in db.collection_names():
        coll = db[coll_name]
    if 'columns' in params:
        set_template(db, coll_name, params['columns'])



    print('db granted')


def add_repositories(params, config=MONGO['git_info']):

    mongodb = MongoClient(host=config['mongo_host'])
    db = mongodb[config['database']]
    collection = db[config['items_collection']]

    # search_str = 'images'
    search_str = 'git'
    # language_str = 'python'
    language_str = ''
    git_flags_list = ['gitzuzex']

    all_repos_dict = overall_request(search_str, language_str, git_flags_list)

    inserted_ids = []

    for git_flag in git_flags_list:

        repos = all_repos_dict[git_flag]

        inserted_ids.extend(collection.insert_many(repos).inserted_ids)

    return inserted_ids


def check_db(name):
    myclient = MongoClient("mongodb://localhost:27017/")
    dblist = myclient.list_database_names()
    if name in dblist:
        return True
    else:
        return False


def get_accounts_list(config=MONGO['git_info'], account_type=None, query=None):

    if query is None:
        query = {}

    mongodb = MongoClient(host=config['mongo_host'])
    db = mongodb[config['database']]
    collection = db[config['items_collection']]

    if account_type:
        query.update({'account_type': account_type})
        account_list = list(collection.find(query))
    else:
        account_list = list(collection.find(query))
    return account_list


def get_account(p, config=MONGO['git_info']):
    if 'account_id' not in p:
        raise EnvironmentError('request must contain account_id')
    account_id = p['account_id']
    mongodb = MongoClient(host=config['mongo_host'])
    db = mongodb[config['database']]
    collection = db[config['items_collection']]
    account_id = ObjectId(account_id) if not isinstance(account_id, ObjectId) else account_id
    account = collection.find_one({'_id': account_id})
    return account

def delete_account(p, config=MONGO['git_info']):
    if 'account_id' not in p:
        raise EnvironmentError('request must contain account_id')
    account_id = p['account_id']
    mongodb = MongoClient(host=config['mongo_host'])
    db = mongodb[config['database']]
    collection = db[config['items_collection']]
    account_id = ObjectId(account_id) if not isinstance(account_id, ObjectId) else account_id
    url_path = collection.find_one({'_id': account_id})['ssh_key'] if collection.find_one({'_id': account_id})['ssh_key'] else None
    if os.path.exists(url_path):
        os.remove(url_path)
    collection.delete_one({'_id': account_id})


def update_account(account_id, params, config=MONGO['git_info']):
    mongodb = MongoClient(host=config['mongo_host'])
    db = mongodb[config['database']]
    collection = db[config['items_collection']]
    account_id = ObjectId(account_id) if not isinstance(account_id, ObjectId) else account_id
    collection.update_one({'_id': account_id}, {'$set': params})


def check_path(p):
    if 'path' not in p:
        raise EnvironmentError('path')
    directory = p['path']
    if not os.path.exists(directory):
        os.makedirs(directory)


if __name__ == '__main__':
    prepare_db('git_info')
    update_account("5d1dc453f0aec22c582496ac", {'account_id': 'new_id', 'name': 'Name'})
    print(get_account("5d1dc453f0aec22c582496ac"))
