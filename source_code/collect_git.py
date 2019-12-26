import sys
from os import listdir
from os.path import join, abspath
from threading import Thread, active_count
import pandas as pd
from git import exc, Repo, RemoteProgress

# import asyncio


config = dict()
accounts = dict()
repo_ptr = {}


def init():
    """
    config initialisation from *.txt ,  easy way to change some config with text editor without using additional python source_code

    Text file for cases then the script uses as terminal tool, in some cases best practices is using python config files

    Warning!!! For stable parsing better way is using regular expression

    """

    with open(join(abspath('../data'), 'config')) as config_file:
        # TODO temporary, while config ctructure and requirement for it doesnt exist,
        #  then it is preferable to use regular expression

        for config_line in config_file:
            config_line = config_line.split(' = ')
            config.update({config_line[0]: config_line[1][:-1]})

    with open(join(abspath('../data'), 'accounts')) as __accounts:
        # TODO temporary, while config ctructure and requirement for it doesnt exist

        for account in __accounts:
            account = account.split(' ')
            accounts.update({account[0]: f'{account[1]}:{account[2]}@'})


def thread(function):
    """
      Decorator for move function in thread processing, work much faster than asynchronous implementation
    """

    def threaded_function(*args, **kwargs):
        _thread = Thread(target=function, args=args, kwargs=kwargs)
        _thread.start()

    return threaded_function


# async def load_repo(link=None, username=None, password=None, account=None):  # asinchron implementation

class ProgressPrinter(RemoteProgress):
    """
    Indication of standard git out

    """

    def update(self, op_code, cur_count, max_count=None, message=''):
        print(op_code, cur_count, max_count, cur_count / (max_count or 100.0), message or "NO MESSAGE")


def get_new_name(repo_name: str, config=config):
    """
    Folder for downloading git-repository, used when there is a folder with a similar name

    """
    if repo_name in listdir(config['save_path']):
        i = 1
        while f'{repo_name}({i})' in [folder for folder in listdir(config['save_path']) if
                                      folder.startswith(repo_name)]:
            i += 1
        return f'{repo_name}({i})'
    return repo_name


@thread
def load_repo(link=None, username=None, password=None, account=None):
    '''
    :param link:
    :param username:
    :param password:
    :param account: username:password
    :return: dictionary repository name and pointer to it
    '''

    if link:
        try:
            repo_name = link.split('/')[-1][:-4]
            repo_name = get_new_name(repo_name)
            path = join(config['save_path'], repo_name)
            if account is not None:
                # TODO check behavior in this case
                url = f'https://{accounts[account]}{link.split("://")[-1]}'
                # print('account :', url)
            if username is not None and password is not None:
                url = f'https://{username}:{password}@{link.split("://")[-1]}'
                # print('username:password :', url)
            else:
                url = link

            Repo.clone_from(url, path)  # , progress=ProgressPrinter)

        except exc.GitCommandError as error:
            print(f'Git command error: {error}\n')
            # print(f'repository link: {url}')


        except:
            import traceback
            trace = traceback.format_exc()
            print("Exception occured:\n{}\n\n".format(trace))
        else:
            repo_ptr.update({repo_name: Repo(path)})


if __name__ == "__main__":

    init()
    # parsing arguments from terminal
    for argument in sys.argv[1:]:
        # TODO add  some specific key arguments for adding accounts, paths , change options and etc.
        data = pd.read_csv(argument)

    # Load *.csv and read rows from table

    data = data.drop_duplicates()
    data = data.dropna(subset=['link'])

    threads = [[]]
    separate_threads = [[]]
    for source in data.to_dict('records'):
        for num, thread_queue in enumerate(separate_threads, 0):
            repository_name = source['link'].split('/')[-1]
            if repository_name not in thread_queue:
                separate_threads[num].append(repository_name)
                threads[num].append(source)
                break
            else:
                if len(separate_threads) - 1 == num:
                    separate_threads.append([repository_name])
                    threads.append([source])
                    break

    for queue in threads:
        for load_thread in queue:
            load_repo(**{key: load_thread[key] for key in load_thread if not pd.isnull(load_thread[key])})
        else:
            # Wait until all threads completed

            while active_count() != 1:
                # TODO progress indication
                pass
            else:
                pass
    # pass
    for i in repo_ptr:
        print(i, repo_ptr[i])  # pointers to repositories !!!!!!!!!!!!

    # repo = git.Repo.clone_from(self._small_repo_url(), os.path.join(rw_dir, 'repo'), branch='master')
    # cloned_repo = repo.clone(os.path.join(rw_dir, 'to/this/path'))
    # origin = bare_repo.create_remote('origin', url=cloned_repo.working_tree_dir)
    # assert origin.exists()

    ####################################################################################################################
    # asinchron implementation  !!!
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(asyncio.wait([load_repo(**{key: source[key] for key in source if not pd.isnull(source[key])}) for source in data.to_dict('records')]))
    ####################################################################################################################

else:

    # this case for load function to another module, may include some initialisations and ect
    pass
