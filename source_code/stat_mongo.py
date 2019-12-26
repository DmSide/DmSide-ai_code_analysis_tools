
import os

import subprocess

import shutil
import stat
import time
import pymongo
#os.environ["GIT_PYTHON_REFRESH"] = "quiet"

from git.repo.base import Repo

from my_token import TokenCode



from analyze_tokens_list import statist_research

from common_functions import read_mongo


def clone_url(url, gitclone_dir):

    Repo.clone_from(url, gitclone_dir)

    #print(url)


def get_files_list(dirName,ext_str):

    ext_len = len(ext_str)

    list_of_ext_files = list()

    for (dirpath, dirnames, filenames) in os.walk(dirName):

        for file_name in filenames:

            lef = len(file_name)

            if (lef > ext_len ):

                curr_ext = file_name[lef - ext_len : lef]

                if curr_ext == ext_str :

                    curr_full_name = os.path.join(dirpath, file_name)

                    list_of_ext_files.append(curr_full_name)

                else:

                    curr_full_name = os.path.join(dirpath, file_name)

                    os.chmod(curr_full_name, stat.S_IWRITE)

                    os.remove(curr_full_name)
            else:

                curr_full_name = os.path.join(dirpath, file_name)

                os.chmod(curr_full_name, stat.S_IWRITE)

                os.remove(curr_full_name)


    return    list_of_ext_files


def delete_code_files(files_names_list):

    for name in files_names_list :

        os.remove(name)



def get_size(dirName):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(dirName):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def add_result_to_stat_mongo(token_groups_list,groups_count_list,dbname):


    client = pymongo.MongoClient("localhost", 27017)

    dbnames = client.list_database_names()


    exists_flag = False

    if dbname in dbnames:

        exists_flag = True

    db = client[dbname]

    groups_stat = db.groups_stat


    for i in range(0,len(groups_count_list)):

        group = token_groups_list[i]
        ncount = groups_count_list[i]

        curr_doc = {"group":group, "count":ncount}

        if not exists_flag :

            groups_stat.insert_one(curr_doc)

        else:

            find_doc = groups_stat.find_one({"group": group})

            if find_doc is None :

                groups_stat.insert_one(curr_doc)

            else:

                new_count = ncount + find_doc["count"]

                newvalues = {"$set": {"count": new_count}}

                groups_stat.update_one(find_doc, newvalues)


def check_stat_mongo(check_str):

    client = pymongo.MongoClient("localhost", 27017)

    db = client['Python_statistics']

    groups_stat = db.groups_stat

    find_doc = groups_stat.find_one({"group": check_str})

    if find_doc is None :

        ncount = -1

    else:

        ncount = find_doc["count"]


    return ncount

def drop_mongo_stat():

    client = pymongo.MongoClient("localhost", 27017)


    client.drop_database('Python_statistics')


def mongo_stat_to_json(json_file_name):

    client = pymongo.MongoClient("localhost", 27017)

    db = client['Python_statistics']

    groups_stat = db.groups_stat

    find_doc = groups_stat.find()






def del_rw(action, name, exc):
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)



if __name__ == "__main__":



    #drop_mongo_stat()

    #x = 0



    # nimp = check_stat_mongo("list")
    # ndef =  check_stat_mongo("np")
    #
    # x = 0


    #for root, dirs, files in os.walk('D:/GitClone'):
    #     for f in files:
    #         os.unlink(os.path.join(root, f))
    #     for d in dirs:
    #         shutil.rmtree(os.path.join(root, d))


    all_list = read_mongo()

    all_l = len(all_list)



    # with open("C:/User/py_urls.txt", "w") as text_file:
    #
    #     for i in range(0, all_l):
    #
    #         text_file.write(all_list[i])
    #         text_file.write('\n')

    interval_list = [1, 2, 3, 4, 5, 6]

    nurl = 1

    all_clone_time = 0.0

    all_create_time = 0.0

    all_tok_lines_time = 0.0

    all_groups_count_time = 0.0

    all_add_to_mongo_time = 0.0

    #for url in all_list :

   #for index in range(0, len(all_list)) :

    for index in range(21, 22):

         url =  all_list[index]

         if not os.path.exists('../GitClone'):

              os.mkdir('../GitClone')

         head = url[0:4]

         if head != 'http':

             continue

         start = time.time()

         clone_url(url,'../GitClone/')

         time.sleep(5)

         start_size = get_size('../GitClone')

         size_count = 0

         while size_count < 3 :

             time.sleep(5)

             curr_size = get_size('../GitClone')

             if( curr_size == start_size) :

                 size_count += 1

             else:

                 start_size = curr_size

         py_files_list = get_files_list('../GitClone', '.py')

         end = time.time()

         dt = end - start

         #print('CLONE TIME', dt)
         all_clone_time += dt

         start = end

         print(nurl , "   URL  :  ", url)

         print(" NUMBER OT FILES :  ", len(py_files_list))

         nurl += 1

         if len(py_files_list) < 1:

             shutil.rmtree('../GitClone', ignore_errors=True)

             continue

         for code_file_name in  py_files_list :

            token_code = TokenCode(code_file_name)

            end = time.time()

            dt = end - start

            #print('TOKEN CREATION  TIME', dt)
            all_create_time += dt

            start = end

            token_code.read_and_token_lines()

            tokens_list = token_code.result_list

            end = time.time()

            dt = end - start

            #print('TOKEN LINESS TIME', dt)
            all_tok_lines_time += dt

            start = end

            token_groups_list, groups_count_list = statist_research(tokens_list, interval_list)

            end = time.time()

            dt = end - start

            #print('TOKEN GTOUPS COUNT TIME', dt)
            all_groups_count_time += dt

            start = end

            add_result_to_stat_mongo(token_groups_list, groups_count_list, "Python_statistics")

            end = time.time()

            dt = end - start

            #print('ADDING TO MONGO  TIME', dt)
            all_add_to_mongo_time += dt

            start = end

         # delete directory with read-only subdirs

         # if os.path.exists('D:/GitClone'):
         #
         #     subprocess.check_call(('attrib -R ' + 'D:/GitClone' + '\\* /S').split())
         #
         #     shutil.rmtree('D:/GitClone')

         # for root, dirs, files in os.walk('../GitClone', topdown=False):
         #     for name in files:
         #         os.remove(os.path.join(root, name))
         #     for name in dirs:
         #         os.rmdir(os.path.join(root, name))

         print("ALL_CLONE_TIME = ", all_clone_time)

         print("ALL_CREATE_TIME = ", all_create_time)

         print("ALL_TOK_LINES_TIME = ", all_tok_lines_time)

         print("ALL_ADD_TO_MONGO_TIME = ", all_add_to_mongo_time)

         delete_code_files(py_files_list)
         shutil.rmtree('../GitClone', ignore_errors=True)

    x = 0




