
import os

os.environ.setdefault('MONGO_HOST', '127.0.0.1')
os.environ.setdefault('MONGO_USER', 'guest')
os.environ.setdefault('MONGO_PASS', '')

os.environ.setdefault('MONGO_ENVIRONMENT', 'test')

MONGO = {
    'tokenization': {
        'mongo_host': 'localhost',
        'database': 'tokenization',  # ZuzexAICodeAnalysis
        'items_collection': 'repos',
        'user': '',
        'password': '',
    },
    'test': {
        'mongo_host': 'localhost',
        'database': 'test_items',
        'items_collection': 'items',
        'user': '',
        'password': '',
        'fields': [('id', 1), ('value', 1)]
    },
    'restricted': {
        'mongo_host': 'localhost',
        'database': 'restricted_items',
        'items_collection': 'items',
        'user': 'admin',
        'password': 'password',
        'fields': [('id', 1), ('value', 1)]
    },
    'system': {
        'mongo_host': os.environ.get('MONGO_HOST', 'localhost'),
        'database': 'system_items',
        'items_collection': 'items',
        'user': os.environ.get('MONGO_USER', ''),
        'password': os.environ.get('MONGO_PASS', ''),
        'fields': [('id', 1), ('value', 1)]
    },
    'git_info': {
        'mongo_host': 'localhost',
        'database': 'git_info',
        'items_collection': 'git_accounts',
        'languages_collection': 'languages',
        'files_collection': 'files',
        'user': 'admin',
        'password': 'password',
        'fields': [('account_id', 'id'), ('account_type', 'gitlab'), ('base_url_http', 'https://'),
                   ('base_url_ssh', 'ssh:'), ('username', ''), ('password', ''), ('ssh_key', 'path/to/ssh_key_file'),
                   ('api_key', 'API_KEY'), ('languages', []), ('tags', []), ('progress', []), ('messages', [])],
        'columns': [('name', 'name'), ('extensions', []), ('tags', [])]
    }
}

USE_DB = os.environ.get('MONGO_ENVIRONMENT', 'restricted')
