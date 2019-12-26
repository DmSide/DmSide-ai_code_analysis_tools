"""Configuring the server at startup"""

import os
import sys
import traceback
from background_task.models import Task


def unlock_all_tasks():
    for task in Task.objects.all():
        if task.locked_by:
            task.locked_by = None
            task.locked_at = None
            task.save()


def execution_at_startup():
    """Function that executes the necessary code at startup"""

    # create_folder()
    # add_final_processing()
    unlock_all_tasks()
    # add_admin_user()


if __name__ == '__main__':
    # os.path.sep = '/'
    # polyglot_path = POLIGLOT['path_polyglot_data']
    # polyglot_path = tools.get_abs_path(polyglot_path)
    # load.polyglot_path = polyglot_path
    # test = Text('Testing and cashing', hint_language_code='en')
    # sentences = test.sentences
    # pola = sentences[0].polarity
    # print pola
    #polyglot_default_install()
    execution_at_startup()


