import requests


def zuzex_projects_search():

    repositories_list = list()

    request_str = 'https://git.zuzex.com/api/v4/projects?private_token=3CzspGr6gBa4f7hpZgoQ'

    r = requests.get(request_str)

    status_code = r.status_code

    if status_code == 200:
        links = r.links

        json_result = r.json()

        for curr_dict in json_result:

            curr_ssh_repo = curr_dict['ssh_url_to_repo']
            curr_http_repo = curr_dict['http_url_to_repo']

            repositories_list.append(curr_ssh_repo)
            repositories_list.append(curr_http_repo)

        pages_url_list = list()

        if 'next' in links.keys() :

            next_url = links['next']['url']

            next_list = next_url.split('&page=')

            head_part = next_list[0]

            after_str = next_list[1]
            npos = after_str.find('&')

            next_str = after_str[0:npos]

            tail_part = after_str[npos : len(after_str)]

            next_num = int(next_str)

            last_url = links['last']['url']

            last_list = last_url.split('&page=')

            after_str = last_list[1]

            npos = after_str.find('&')

            last_str = after_str[0:npos]

            last_num = int(last_str)

            for i in range (next_num, last_num + 1) :

                curr_url = head_part + '&page=' + str(i) + tail_part
                pages_url_list.append(curr_url)

        if len(pages_url_list) > 0 :

           for url in pages_url_list :

               r = requests.get(url)

               status_code = r.status_code

               if status_code == 200 :
                   json_result = r.json()

                   for curr_dict in json_result:
                       curr_ssh_repo = curr_dict['ssh_url_to_repo']
                       curr_http_repo = curr_dict['http_url_to_repo']

                       repositories_list.append(curr_ssh_repo)
                       repositories_list.append(curr_http_repo)

    return [status_code, repositories_list ]


if __name__ == "__main__":

    status_code, repositories_list = zuzex_projects_search()

    lr = len(repositories_list)

    print("NUMBER OF PROJECTS", lr)

    for url in repositories_list :

        print(url)


