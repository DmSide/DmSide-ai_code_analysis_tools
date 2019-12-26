import warnings
import git
import os
from guesslang import Guess
from pathlib import Path

import pymongo
from pymongo.collation import Collation
from bson.code import Code

from mongo_config import MONGO

from my_token import TokenCode
from analyze_tokens_list import statist_research

break_line = '_________________________________________________________________________________________________________'


class MongoManager:

    def __init__(self, config):

        self.config = config
        self.client = None
        self.db = None
        self.collection = None
        self.index_name = None
        self.fields = MONGO['test']['fields']

        if self.config['mongo_host'] == 'localhost':

            self.client = pymongo.MongoClient(self.config['mongo_host'], connect=True)

            self.create_db()

            self.add_user()

    def add_user(self):

        user_in = self.db.command({'usersInfo': {'user': self.config['user'], 'db': self.db.name}})['users']

        if user_in:
            self.db.command('dropUser', self.config['user'])

        if self.config['user']:
            self.db.command("createUser", self.config['user'],
                            pwd=self.config['password'],
                            roles=[{'role': "dbOwner", 'db': self.db.name}]
                            # roles=["dbOwner"],
                            # roles=["root"],  # Not working without additional initializations
                            )

    def create_db(self):

        if self.client is None:
            return

        self.db = self.client[self.config['database']]
        # self.collection = self.db[self.config['items_collection']]

        if self.config['items_collection'] in self.db.list_collection_names():
            collection = self.db[self.config['items_collection']]
            collection.drop()

        self.collection = self.db.create_collection(self.config['items_collection'],
                                                    collation=Collation(locale='en_US'))

        indexes_keys = self.get_indexes()

        index = [self.fields[0]]

        if index not in indexes_keys:
            self.index_name = self.collection.create_index(index)

            print(self.index_name)

    def restart_db(self):

        if self.client is None:
            return

        self.client.drop_database(self.config['database'])
        self.create_db()

    def add_records(self, documents):

        return self.add_records_to_collection(documents, self.collection.name)

    def remove_records(self, selector, once=False):

        if self.client is None:
            return

        args = tuple(selector)

        if once:
            self.collection.delete_one(*args)
        else:
            self.collection.delete_many(*args)

    def remove_collection(self):

        if self.client is None:
            return

        self.collection.drop()

    def remove_index(self):

        indexes_names = self.get_indexes(keys=False)
        if self.index_name in indexes_names:
            self.collection.drop_index(self.index_name)

    def get_indexes(self, keys=True):
        indexes = self.collection.index_information()
        indexes_names = list(indexes.keys())
        indexes_keys = [x['key'] for x in list(indexes.values())]

        if keys:
            return indexes_keys
        else:
            return indexes_names

    def select(self, selector, once=False):

        args = tuple(selector)
        if once:
            cursor = self.collection.find_one(*args)

            return cursor
        else:
            cursor = self.collection.find(*args)

            return list(cursor)

    def execute(self, arguments):
        cursor = self.db.command(*arguments['args'], **arguments['kwargs'])['cursor']

        return cursor['firstBatch']

    def count(self, selector):

        return self.count_collection_records(selector, self.collection.name)

    def update_records(self, renovate, once=False):
        args = tuple(renovate)

        if once:
            self.collection.update_one(*args)
        else:
            self.collection.update_many(*args)

    # def map_reduce(self, selector):
    #
    #     mapper = Code("""
    #                    function () {
    #                      this.scores.forEach(function(z) {
    #                        emit(z, 1);
    #                      });
    #                    }
    #                    """)
    #
    #     reducer = Code("""
    #                     function (key, values) {
    #                       var total = 0;
    #                       for (var i = 0; i < values.length; i++) {
    #                         total += values[i];
    #                       }
    #                       return total;
    #                     }
    #                     """)
    #
    #     collection = self.collection.map_reduce(mapper, reducer, "experiments",  # create new collection experiments
    #                                             full_response=False,
    #                                             query=selector)
    #
    #     return list(collection.find())

    def user_connect(self):

        self.client = pymongo.MongoClient('mongodb://%s:%s@127.0.0.1/%s' % (self.config['user'],
                                                                            self.config['password'],
                                                                            self.collection.name))

    def copy_database(self):

        if '%s_copy' % self.db.name in self.client.list_database_names():
            self.client.drop_database('%s_copy' % self.db.name)

        self.client.admin.command('copydb',
                                  fromdb=self.db.name,
                                  todb='%s_copy' % self.db.name,
                                  fromhost=self.config['mongo_host'])

    def create_collection(self, collection_name):

        if collection_name in self.db.list_collection_names():
            collection = self.db[collection_name]
            collection.drop()

        collection = self.db.create_collection(collection_name,
                                               collation=Collation(locale='en_US'))

        print(collection)

    def add_records_to_collection(self, documents, target_collection):

        if self.client is None:
            return None

        if target_collection in self.db.list_collection_names():

            collection = self.db[target_collection]

            if isinstance(documents, list):

                # self.collection.insert(documents)  # DEPRECATED

                return collection.insert_many(documents).inserted_ids
            else:

                return collection.insert_one(documents).inserted_id
        else:

            return None

    def update_collection_records(self, renovation, target_collection):

        args = tuple(renovation)

        if target_collection in self.db.list_collection_names():

            collection = self.db[target_collection]

            collection.update_one(*args)  # consider unique token group

    def count_collection_records(self, selector, target_collection):

        if target_collection in self.db.list_collection_names():

            collection = self.db[target_collection]

            args = tuple(selector)
            return collection.count_documents(*args)
        else:
            return 0

    def select_collection_records(self, selector, target_collection, once=False):

        if target_collection in self.db.list_collection_names():

            collection = self.db[target_collection]

            args = tuple(selector)
            if once:
                cursor = collection.find_one(*args)

                return cursor
            else:
                cursor = collection.find(*args)

                return list(cursor)
        else:

            return []

    def tokenization_statistics(self):

        detector = Guess()

        languages = list(detector.languages.keys())

        # create languages collection

        self.create_collection('languages')

        self.create_collection('files')

        self.create_collection('tokens')

        for lang in languages:
            lang = lang.replace('+', 'P')
            lang = lang.replace('#', '_Sharp')

            document = {'_id': lang, 'stat': lang + '_statistics'}

            self.add_records_to_collection(document, 'languages')

            self.create_collection(lang + '_statistics')

        # get repositories

        repos_path = 'D:\\repos'

        repos = os.listdir(repos_path)

        for repo in repos:

            repository = git.Repo(os.path.join(repos_path, repo))

            url = repository.config_reader().get_value('remote "origin"', 'url')

            document = {'url': url}

            repo_id = self.add_records(document)

            files = [x[0] for x in list(repository.index.entries.keys())]

            documents = []

            for file in files:

                # print(file)

                try:
                    filepath = os.path.join(repos_path, repo, file)

                    token_code = TokenCode(filepath)
                    tokens_list = token_code.result_list
                    n = 1
                    interval_list = list(range(1, n + 1))

                    token_groups_list, groups_count_list = statist_research(tokens_list, interval_list)

                    text = Path(filepath).read_text()
                    text_language = detector.language_name(text)

                    text_language = text_language.replace('+', 'P')
                    text_language = text_language.replace('#', '_Sharp')

                    documents.append({'file': file, 'lang': text_language, 'repo': repo_id})

                    statistics_collection = text_language + '_statistics'

                    for i in range(len(token_groups_list)):
                        group_list = token_groups_list[i]
                        n_occ = groups_count_list[i]

                        selector = [{'token_group': group_list}]
                        count = self.count_collection_records(selector, 'tokens')

                        if not count:
                            document = selector[0]
                            token_id = self.add_records_to_collection(document, 'tokens')
                        else:
                            document = self.select_collection_records(selector, 'tokens', once=True)
                            token_id = document.get('_id')

                        selector = [{'_id': token_id}]
                        count = self.count_collection_records(selector, statistics_collection)

                        if count:
                            selector.extend([{'$inc': {'count': n_occ}}])
                            renovate = selector
                            self.update_collection_records(renovate, statistics_collection)
                        else:
                            document = {'_id': token_id, 'count': n_occ}
                            self.add_records_to_collection(document, statistics_collection)

                except Exception as e:
                    print(e)
                    documents.append({'file': file, 'lang': 'UNKNOWN', 'repo': repo_id})

            self.add_records_to_collection(documents, 'files')


if __name__ == '__main__':

    warnings.simplefilter("always")

    # configuration = MONGO['test']
    configuration = MONGO['restricted']

    mongoVisor = MongoManager(configuration)

    mongoVisor.restart_db()

    mongoVisor.copy_database()

    mongoVisor.user_connect()

    record = {'id': 'particle', 'value': 'electron', 'scores': [1, 2, 4], 'cash': 4, 'bool': True}
    records = [{'id': 'element', 'value': 'experiment', 'scores': [10, 3, 3], 'cash': 5, 'bool': False},
               {'id': 'beam', 'value': 'wave', 'scores': [2, 0, 5], 'cash': 1, 'bool': True}]

    mongoVisor.add_records(records)
    # mongoVisor.remove_collection()
    mongoVisor.add_records(record)
    mongoVisor.remove_index()

    records = [{'id': 'test', 'value': 'result', 'scores': [3, 1, 1], 'cash': 10, 'bool': True},
               {'id': 'ray', 'value': 'laser', 'scores': [0, 0, 0], 'cash': 0, 'bool': False}]

    mongoVisor.add_records(records)

    query = {'id': {'$in': ['element', 'beam']}}
    # print(query)
    result = mongoVisor.map_reduce(query)
    print(*tuple(result), sep='\n')

    print(break_line)

    query = [{'value': 'laser'}]
    mongoVisor.remove_records(query)

    update = [{}, {'$inc': {'cash': 2}}]
    mongoVisor.update_records(update)

    query = [{}]
    # print(query)
    result = mongoVisor.count(query)
    print(result)

    query = [{'value': {'$regex': '^l'}}]
    # print(query)
    result = mongoVisor.count(query)
    print(result)

    query = [{'$and': [{'bool': True}, {'cash': {'$lt': 10}}]}]
    # print(query)
    result = mongoVisor.count(query)
    print(result)

    command = {'args': ('aggregate', 'items'),
               'kwargs': {'pipeline': [
                                       {'$unwind': '$scores'},
                                       ],
                          'cursor': {'batchSize': 3},
                          'hint': {},
                          }
               }
    # print(command)
    result = mongoVisor.execute(command)
    print(*tuple(result), sep='\n')

    print(break_line)

    command = {'args': ('aggregate', 'items'),
               'kwargs': {'pipeline': [
                                       {'$sort': {'id': 1}},
                                       {'$skip': 0},
                                       {'$limit': 3},
                                       {'$match': {'value': 'wave'}},
                                       # {'$group': {'_id': None, 'count': {'$sum': 1}}},
                                       {'$addFields': {'score': {'$sum': '$scores'}}},
                                       ],
                          'cursor': {'batchSize': 3},
                          'hint': {},
                          }
               }
    # print(command)
    result = mongoVisor.execute(command)
    print(*tuple(result), sep='\n')

    print(break_line)

    command = {'args': ('find', 'items'),
               'kwargs': {
                          'limit': 2,
                          'skip': 0,
                          'hint': {}
                          }
               }
    # print(command)
    result = mongoVisor.execute(command)
    print(*tuple(result), sep='\n')

    print(break_line)

    query = [{}]
    # print(query)
    result = mongoVisor.select(query)
    print(*tuple(result), sep='\n')

    print(break_line)

    query = [{}, {'value': 0}]
    # print(query)
    result = mongoVisor.select(query)
    print(*tuple(result), sep='\n')

    print(break_line)

    query = [{'id': 'element'}]
    # print(query)
    result = mongoVisor.select(query)
    print(*tuple(result), sep='\n')

    print(break_line)

    query = [{'id': {'$in': ['element', 'beam']}}]
    # print(query)
    result = mongoVisor.select(query)
    print(*tuple(result), sep='\n')

    print(break_line)

    query = [{'$or': [{'id': 'element'}, {'id': 'beam'}]}]
    # print(query)
    result = mongoVisor.select(query)
    print(*tuple(result), sep='\n')

    mongoVisor.client.close()

    print('test')

else:

    configuration = MONGO['tokenization']

    mongoVisor = MongoManager(configuration)

    mongoVisor.restart_db()

    mongoVisor.tokenization_statistics()

    print('done')
