
from common_functions import create_request_str, add_to_mongo, get_request_results, add_request_to_list


def overall_request(search_str, language_str, gitflags_list):

    all_repos_dict = {}

    for gitflag in gitflags_list:

        request_str = create_request_str(search_str, language_str, gitflag)

        status_code, repositories_list = get_repositories_list(request_str, gitflag)

        if (status_code == 200) and (len(repositories_list) > 0):

            add_to_mongo(repositories_list)

            all_repos_dict[gitflag] = repositories_list

        else:

            all_repos_dict[gitflag] = repositories_list

    return all_repos_dict


def get_repositories_list(request_str, gitflag):

    status_code = 404
    repositories_list = []

    if gitflag == 'github':

        status_code, repositories_list = get_from_github(request_str)

    if gitflag == 'gitlab':

        status_code, repositories_list = get_from_gitlab(request_str)

    if gitflag == 'gitzuzex':

        status_code, repositories_list = get_from_gitzuzex(request_str)

    return [status_code, repositories_list]


def get_from_github(request_str):

    repositories_list = list()

    status_code, links,  result = get_request_results(request_str, 'github')

    if status_code == 200:

        repositories_list = add_request_to_list(result, repositories_list, 'github')

        pages_url_list = list()

        if 'next' in links.keys():

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

        if len(pages_url_list) > 0:

            for url in pages_url_list:

                status_code, links, result = get_request_results(url, 'github')

                if status_code == 200:

                    repositories_list = add_request_to_list(result, repositories_list, 'github')

                # print('NPAGE = ', npage)

                npage += 1

    return [status_code, repositories_list]


def get_from_gitlab(request_str):

    repositories_list = list()

    status_code, links, result = get_request_results(request_str, 'gitlab')

    if status_code == 200:

        repositories_list = add_request_to_list(result, repositories_list, 'gitlab')

    if 'next' in links.keys():

        next_rel = 'next'

        while next_rel == 'next':

            next_url = links['next']['url']

            status_code, links, result = get_request_results(next_url, 'gitlab')

            if status_code == 200:

                repositories_list = add_request_to_list(result, repositories_list, 'gitlab')

            else:
                print("WRONG STATUS CODE", status_code)

            if not ('next' in links.keys()):
                break

    return [status_code, repositories_list]


def get_from_gitzuzex(request_str):

    repositories_list = list()

    status_code, links, result = get_request_results(request_str, 'gitzuzex')

    if status_code == 200:

        repositories_list = add_request_to_list(result, repositories_list, 'gitzuzex')

        pages_url_list = list()

        if 'next' in links.keys():

            next_url = links['next']['url']

            next_list = next_url.split('&page=')

            head_part = next_list[0]

            after_str = next_list[1]
            npos = after_str.find('&')

            next_str = after_str[0:npos]

            tail_part = after_str[npos:len(after_str)]

            next_num = int(next_str)

            last_url = links['last']['url']

            last_list = last_url.split('&page=')

            after_str = last_list[1]

            npos = after_str.find('&')

            last_str = after_str[0:npos]

            last_num = int(last_str)

            for i in range(next_num, last_num + 1):

                curr_url = head_part + '&page=' + str(i) + tail_part

                pages_url_list.append(curr_url)

        if len(pages_url_list) > 0:

            for url in pages_url_list:

                status_code, links, result = get_request_results(url, 'gitzuzex')

                if status_code == 200:

                    repositories_list = add_request_to_list(result, repositories_list, 'gitzuzex')

    return [status_code, repositories_list]


if __name__ == "__main__":

    search_str = 'machine+learning'

    language_str = 'python'

    gitflags_list = ['github', 'gitlab', 'gitzuzex']

    all_repos_dict = overall_request(search_str, language_str, gitflags_list)

    x = 0
