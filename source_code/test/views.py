# -*- coding: utf-8 -*-
# from bson import ObjectId
from django.http import JsonResponse
from lib.json_encoder import JSONEncoderHttp
from rest_framework.decorators import api_view
from test import tasks
import db_master

from collect_git import get_new_name
from os.path import join, exists
from shutil import rmtree
from urllib.parse import urlparse

# from background_task.models import Task
# ***************************** TEST FUNCTIONS ******************************** #
# noinspection PyUnusedLocal


@api_view(['GET'])
def index(request):
    results = {'response': {}}
    return JsonResponse(results, encoder=JSONEncoderHttp)


@api_view(['POST'])
def task_repositories(request):

    # operation_list = ['downloading', 'listing', 'detection', 'tokenization', 'deleting']
    operation_list = ['downloading']

    if 'id' in request.data:
        incompleted = [db_master.get_account({'account_id': request.data['id']})]
    else:
        incompleted = db_master.get_accounts_list(query={'progress': {'$not': {'$all': operation_list}}})

    for repo in incompleted:

        repo_name = repo['base_url_http'].split('/')[-1][:-4]
        config = {'save_path': "D://"}
        # repo_name = get_new_name(repo_name, config=config)
        clone_path = join(config['save_path'], repo_name)

        # if exists(clone_path):
        #     rmtree(clone_path)

        parse_path = urlparse(repo['base_url_http'])
        clone_url = parse_path.scheme + '://' + repo['username'] + ':' + repo['password'] + '@' + \
                    parse_path.hostname + parse_path.path

        incompleted_list = operation_list.copy()

        for completed in repo['progress']:
            incompleted_list.remove(completed)

        id = str(repo['_id'])

        actions = []
        actions_import = []
        actions_args = []

        for operation in incompleted_list:

            if operation == 'downloading':
                actions.append('git.Repo.clone_from')
                actions_import.append('git')
                actions_args.append((clone_url, clone_path))
            elif operation == 'listing':
                pass
            elif operation == 'detection':
                pass
            elif operation == 'tokenization':
                pass
            elif operation == 'deleting':
                pass

        tasks.repo(id, incompleted_list, actions_import, actions, actions_args)

    results = {'status': True, 'response': 'tasks added', 'error': {}}
    return JsonResponse(results, encoder=JSONEncoderHttp)


@api_view(['POST'])
def add_repositories(request):
    params = request.data
    inserted_ids = db_master.add_repositories(params)
    results = {'status': True, 'response': {'inserted repos ids': inserted_ids}, 'error': {}}
    return JsonResponse(results, encoder=JSONEncoderHttp)


@api_view(['POST'])
def test_exception_work(request):
    tasks.test()
    results = {'status': True, 'response': 'http://127.0.0.1:8000/', 'error': {}}
    return JsonResponse(results, encoder=JSONEncoderHttp)


@api_view(['POST'])
def prepare_db(request):
    params = request.data
    db_master.prepare_db(params)
    results = {'status': True, 'response': {}, 'error': {}}
    return JsonResponse(results, encoder=JSONEncoderHttp)


@api_view(['POST'])
def get_accounts_list(request):
    params = request.data
    accounts_list = db_master.get_accounts_list()
    results = {'status': True, 'response': {'accounts list': accounts_list}, 'error': {}}
    return JsonResponse(results, encoder=JSONEncoderHttp)


@api_view(['POST'])
def get_languages_list(request):
    params = request.data
    languages_list = db_master.get_languages_list(params)
    results = {'status': True, 'response': {'languages list': languages_list}, 'error': {}}
    return JsonResponse(results, encoder=JSONEncoderHttp)


@api_view(['POST'])
def add_language(request):
    params = request.data
    inserted_language_id = db_master.add_language(params)
    results = {'status': True, 'response': {'inserted language id': inserted_language_id}, 'error': {}}
    return JsonResponse(results, encoder=JSONEncoderHttp)


@api_view(['POST'])
def remove_language(request):
    params = request.data
    removed = db_master.remove_language(params)
    results = {'status': True, 'response': {'removed languages count': removed}, 'error': {}}
    return JsonResponse(results, encoder=JSONEncoderHttp)


@api_view(['POST'])
def update_language(request):
    params = request.data
    db_master.update_language(params)
    results = {'status': True, 'response': {}, 'error': {}}
    return JsonResponse(results, encoder=JSONEncoderHttp)


@api_view(['POST'])
def get_account(request):
    params = request.data
    account = db_master.get_account(params)
    results = {'status': True, 'response': {'account': account}, 'error': {}}
    return JsonResponse(results, encoder=JSONEncoderHttp)


@api_view(['POST'])
def delete_account(request):
    params = request.data
    db_master.delete_account(params)
    results = {'status': True, 'response': {}, 'error': {}}
    return JsonResponse(results, encoder=JSONEncoderHttp)


@api_view(['POST'])
def check_path(request):
    params = request.data
    db_master.check_path(params)
    results = {'status': True, 'response': {}, 'error': {}}
    return JsonResponse(results, encoder=JSONEncoderHttp)
