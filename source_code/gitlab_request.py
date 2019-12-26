#https://docs.gitlab.com/ce/api/projects.html

import requests
import gitlab






def gitlab_projects_request():


    repositories_list = list()

    #request_str = 'https://gitlab.com/api/v4/projects?private_token=tGwSHPTJciZVaPE4FYxn'
    #request_str = 'https://gitlab.com/api/v4/search?scope=projects&search=python?private_token=tGwSHPTJciZVaPE4FYxn'
    request_str = 'https://gitlab.com/api/v4/search?scope=projects&search=machine+learning+python&private_token=tGwSHPTJciZVaPE4FYxn'



    #per_page = {'q':'machine+leaning+language:python', 'per_page' : '100' }

    #r = requests.get(request_str,params = per_page)
    r = requests.get(request_str)

    status_code = r.status_code


    if status_code == 200:

         links = r.links

         json_result = r.json()



         for curr_dict in json_result :

             keys_list = curr_dict.keys()

             curr_ssh_repo = curr_dict['ssh_url_to_repo']

             curr_http_repo = curr_dict['http_url_to_repo']

             repositories_list.append(curr_ssh_repo)

             repositories_list.append(curr_http_repo)

    pages_url_list = list()

    if 'next' in links.keys():



        next_rel = 'next'

        nnext = 2
        while next_rel == 'next' :
        #while nnext < 4 :

            next = links['next']


            next_url = links['next']['url']

            r = requests.get(next_url)

            links = r.links

            status_code = r.status_code

            if status_code == 200:

                json_result = r.json()

                for curr_dict in json_result:
                    curr_ssh_repo = curr_dict['ssh_url_to_repo']
                    curr_http_repo = curr_dict['http_url_to_repo']
                    print(curr_http_repo)

                    repositories_list.append(curr_ssh_repo)
                    repositories_list.append(curr_http_repo)

            else:
                print("WRONG STATUS CODE", status_code)

            if not ('next' in links.keys()):
                break

    return [status_code, repositories_list]

if __name__ == "__main__":

    # find_list = read_mongo()
    #
    # lf = len(find_list)
    #
    # for url in find_list :
    #
    #     print(url)

    status_code, repositories_list = gitlab_projects_request()

    print("FINISH")



    x = 0