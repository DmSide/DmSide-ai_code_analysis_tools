
import requests
import pymongo


def create_request_str(search_str, language_str, gitflag):

    if gitflag == 'github':

        request_str = 'https://api.github.com/search/repositories?q=' + search_str

        if len(language_str) > 0:
            request_str = request_str + '+language:' + language_str

        return request_str

    u_str = search_str

    if len(language_str) > 0:
        u_str = u_str + '+' + language_str

    if gitflag == 'gitlab':

        # request_str = 'https://gitlab.com/api/v4/search?scope=projects&search=machine+learning+python&private_token=tGwSHPTJciZVaPE4FYxn'

        request_str = 'https://gitlab.com/api/v4/search?scope=projects&search=' + u_str + '&private_token=tGwSHPTJciZVaPE4FYxn'

        return request_str

    if gitflag == 'gitzuzex':

        request_str = 'https://git.zuzex.com/api/v4/projects?&search=' + u_str + '&private_token=3CzspGr6gBa4f7hpZgoQ'

        return request_str

    return 'wrong gitflag value'


def get_request_results(request_str, gitflag):

    if gitflag == 'github':
        r = requests.get(request_str, auth=('agorbanev', 'M24AsQgW'))

    if (gitflag == 'gitzuzex') or (gitflag == 'gitlab'):
        r = requests.get(request_str)

    status_code = r.status_code

    links = r.links

    if status_code == 200:

        if gitflag == 'github':

            r_json = r.json()

            items = [x for x in r_json['items'] if 'created_at' in x]

            result = sorted(items, key=lambda x: x['created_at'], reverse=True)

        else:

            result = r.json()

    else:

        result = []

    return [status_code, links, result]


def add_request_to_list(req_list, repositories_list, gitflag):

    # if len(repositories_list) < 1:
    #     print("LIST_IS_EMPTY in ", gitflag)
    #     return repositories_list

    for curr_dict in req_list:

        repo = {}

        curr_tags = []

        if gitflag == 'github':

            curr_http_repo = curr_dict['clone_url']

            curr_ssh_repo = curr_dict['ssh_url']

            curr_user = ''
            curr_pass = ''
            curr_api_key = ''
        else:
            curr_http_repo = curr_dict['http_url_to_repo']

            curr_ssh_repo = curr_dict['ssh_url_to_repo']

            curr_user = 'agorbanev'
            curr_pass = 'M24AsQgW'

            if 'tag_list' in curr_dict:
                curr_tags = curr_dict['tag_list']

            if gitflag == 'gitzuzex':
                curr_api_key = '3CzspGr6gBa4f7hpZgoQ'
            else:
                curr_api_key = 'tGwSHPTJciZVaPE4FYxn'

        repo['base_url_http'] = curr_http_repo
        repo['base_url_ssh'] = curr_ssh_repo
        repo['account_type'] = gitflag
        repo['username'] = curr_user
        repo['password'] = curr_pass
        repo['ssh_key'] = ''
        repo['api_key'] = curr_api_key
        repo['languages'] = []
        repo['tags'] = curr_tags
        repo['progress'] = []
        repo['messages'] = []

        # repositories_list.append(curr_ssh_repo)
        # repositories_list.append(curr_http_repo)

        repositories_list.append(repo)

    if len(repositories_list) < 1:
        print("LIST_IS_EMPTY in ", gitflag)

    return repositories_list


def add_to_mongo(repositories_list):

    client = pymongo.MongoClient("localhost", 27017)

    # dbnames = client.list_database_names()
    # if 'repo_urls_db' in dbnames:
    #     index_flag = False

    db = client['repo_urls_db']

    repo_urls = db.repo_urls

    repo_urls.create_index([('url', pymongo.TEXT)])

    for url_str in repositories_list:

        item = {'url': url_str}

        try:
            repo_urls.insert_one(item)
        except Exception as e:
            print(e)
            continue


def read_mongo():

    client = pymongo.MongoClient("localhost", 27017)

    db = client['repo_urls_db']

    repo_urls = db.repo_urls

    find_list = list()

    for repo_url in repo_urls.find():
        find_list.append(repo_url['url'])

    return find_list
