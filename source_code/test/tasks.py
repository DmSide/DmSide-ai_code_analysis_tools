"""module containing background tasks"""

from background_task import background
from db_master import get_account, update_account
import requests


@background(schedule=1, name='test')
def test():
    print("test: ok!")


@background(schedule=5, name='retry')
def retry(id):
    try:
        requests.post('http://127.0.0.1:8000/task_repositories', {'id': id})
    except Exception as e:
        print('retry failed')
        print(e)


@background(schedule=1, name='repo')
def repo(id, actions_name=None, actions_import=None, actions=None, actions_args=None):

    element = get_account({'account_id': id})

    current_progress = element['progress']

    print('scheduled id %s' % id)

    if actions_name is None:
        actions_name = []

    if actions_import is None:
        actions_import = []

    if actions is None:
        actions = []

    if actions_args is None:
        actions_args = []

    try:
        for action_import in actions_import:
            exec("import %s" % action_import)

        current_actions = actions_name

        for n, action_name in enumerate(current_actions):

            action = actions[n]

            if action is None:
                message = "null action"

                if action_name:
                    message = message + ' for ' + action_name

                print(message)
            else:
                action = eval(action)

                if actions_args[n] is None:
                    result = action()
                else:
                    result = action(*actions_args[n])

                if action_name:
                    # current_progress.extend([action_name])
                    current_progress.append(action_name)

                    update_account(id, {'progress': current_progress})

                print(result)

                print('action completed')

                actions_name.remove(action_name)

    except Exception as e:
        print(e)

        retry(id)

