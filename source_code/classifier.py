from os import listdir
from os.path import isdir, join, abspath
from pathlib import Path
import pickle
import traceback
from guesslang import Guess


class Classifier:


    def __init__(self):
        self.extension_dict = self.load_extensions()
        self.code_analysis_methods = [self.sort_by_extension]

    def load_extensions(self):
        with open(join(abspath('../data'), 'data_types.pickle'), 'rb') as __file:
            return pickle.load(__file)

    def __call__(self, repository):
        method = iter(self.code_analysis_methods)

        condition = True
        ################# tmp #################
        quality, statistic = None, None
        #######################################
        while condition:
            try:
                condition, statistic = next(method)(repository)
            except StopIteration:
                print(f'Last method was end working without result')
                break
            #except:
            #    trace = traceback.format_exc()
            #    print(f"Exception occured:\n{format(trace)}\n\n")

        return (repository,  # both paths to repo, local and remote(may already been in mongodb)
                condition,   # subjective quality of language detecting
                statistic)   # information about repository structure, maybe pair key value for every file



    def sort_by_extension(self, file_name):
        # TODO check behavior with uppercase suffixies
        for file_type in self.extension_dict:
            if Path(file_name).suffix in self.extension_dict[file_type].keys():  ## for complex types like .tar.gz maybe need suffixes witch return list ['.tar' , '.gz']
                return file_type # class of file , data file, program file, ect
        else:
             file_type = 'undeclared'

        if file_type == 'sourse_code':
            file_content = self.sourse_analysis(file_name)

        elif file_type == 'undeclared':
            file_content = self.file_analysis(file_name)
        else:
            file_content = {'data': self.extension_dict[file_type][Path(file_name).suffix]}

        return file_content

    def sourse_analysis(self, file_name):
        # TODO gueslang support  only 20 program languages support, need something else
        file_type = Guess().language_name(file_name)
        print(file_type)



if __name__ == '__main__':

    path = '/home/redhat/test/check_file'
    a = Classifier()
    a(path)


# data = test()
# with open('data_types.pickle', 'wb') as f:
#    # Pickle the 'data' dictionary using the highest protocol available.
#    pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)



def code_analyzer(method):
    def wrapper(*arg,**kwarg):
        # some_code
        result = method()
        # some_code
        condition, statistic = 0, 0
        return condition, statistic
    return wrapper



