
import os
import git


def get_repo_name_from_url(url: str) -> str:
    last_slash_index = url.rfind("/")
    last_suffix_index = url.rfind(".git")
    if last_suffix_index < 0:
        last_suffix_index = len(url)

    if last_slash_index < 0 or last_suffix_index <= last_slash_index:
        raise Exception("Badly formatted url {}".format(url))

    return url[last_slash_index + 1:last_suffix_index]


repos = [
         # 'https://github.com/exercism/delphi.git',
         # 'https://github.com/exercism/cpp.git',
         # 'https://github.com/exercism/python.git'
         # 'https://github.com/leachim6/hello-world.git'
         'https://github.com/liquidscorpio/helloworld.git',
         'https://github.com/michaljemala/hello-python.git'
         ]

for repo in repos:

    repo_path = 'D:\\repos\\%s' % get_repo_name_from_url(repo)

    if not os.path.isdir(repo_path):

        git.Repo.clone_from(repo, 'D:\\repos\\%s' % get_repo_name_from_url(repo))

        # wait until complete required

import mongo_manager

mongo_manager