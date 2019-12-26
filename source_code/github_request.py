import requests

def github_repositories_search(search_str,language_str):

    repositories_list = list()

    request_str = 'https://api.github.com/search/repositories?q=' + search_str

    if len(language_str) > 0 :
        request_str = request_str + '+language:' + language_str

    # from getpass import getpass
    import getpass
    from common_functions import add_to_mongo

    search_flag = True

    last_flag = False

    status_code, json_result, links = github_http_request(request_str)

    results = [x for x in json_result['items'] if 'created_at' in x]

    items =  sorted(results, key=lambda x: x['created_at'],reverse = True)

    if status_code == 200 :

        for item in items:

            #curr_adres = 'https://github.com/' + item['full_name'] + '.git'
            clone_url  = item['clone_url']
            repositories_list.append(clone_url)
            ssh_url = item['ssh_url']
            repositories_list.append(clone_url)

        pages_url_list = list()

        if 'next'  in links.keys() :

            next_page = links['next']

            req_str = next_page['url']

            last_page = links['last']

            last_str = last_page['url']

            rlist = req_str.split('&page=')

            llist = last_str.split('&page=')

            main_part = rlist[0] + '&page='

            min_page = int(rlist[1])
            max_page = int(llist[1])

            for i in range(min_page, max_page + 1):
                curr_str = main_part + str(i)
                pages_url_list.append(curr_str)

        npage = 2
        if len(pages_url_list) > 0 :

            for url in  pages_url_list :

                status_code, json_result, links = github_http_request(url)

                print('NPAGE = ',npage)

                npage += 1

                if 'items' in json_result.keys() :

                    results = [x for x in json_result['items'] if 'created_at' in x]

                    items = sorted(results, key=lambda x: x['created_at'],reverse = True)

                    if status_code == 200:

                        #items = json_result['items']

                        for item in items:
                            #curr_adres = 'https://github.com/' + item['full_name'] + '.git'
                            curr_adres = item['git_url']

                            repositories_list.append(curr_adres)


    return   [ status_code , repositories_list ]


def github_http_request(request_str):

    #requests.get('https://api.github.com')

    r = requests.get(request_str,auth=('agorbanev', 'M24AsQgW'))

    status_code = r.status_code

    links = r.links

    json_result = r.json()

    return  [ status_code, json_result, links ]







def my_session(urlstr):
    # By using a context manager, you can ensure the resources used by
    # the session will be released after use
    #with requests.Session() as session:

        # session.auth = ('username', getpass.getpass())
        #
        # auth = session.auth
        #
        # # Instead of requests.get(), you'll use session.get()
        # #response = session.get('https://api.github.com/user')
        # response = session.get(urlstr)
        #
        # json_result = response.json()

    requests.Session().auth = ('username', getpass.getpass())



    # Instead of requests.get(), you'll use session.get()
    # response = session.get('https://api.github.com/user')
    response = requests.Session().get(urlstr)

    json_result = response.json()

    return  json_result


if __name__ == "__main__":

    search_str = "machine+learning"
    language_str = 'python'

    status_code, repositories_list =  github_repositories_search(search_str,language_str)

    lr = len(repositories_list )

    print(" NUMBER OF URLs = ",lr)

    for url in repositories_list:
         print(url)

    #add_to_mongo(repositories_list)



    # request_str = 'https://api.github.com/search/repositories?q=machine+learning+language:python'
    # #request_str = 'https://api.github.com/search/repositories?q=tetris+language:assembly&sort=stars&order=desc'
    # status_code, rjson = github_http_request(request_str)
    #
    # items = rjson['items']
    #
    # li = len(items)
    #
    # adres_list = list()
    # for item in items :
    #     curr_adres = 'https://github.com/' + item['full_name'] +'.git'
    #     print(curr_adres)
    #     adres_list.append(curr_adres)
    #
    #
    #
    #
    #
    # x = 0

