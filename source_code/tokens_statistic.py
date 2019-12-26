import itertools


def get_tokens_statistics(file_name,tokens_list,comb_list,search_flag):

    result_dict = {}

    if search_flag > 0 :

        with open(file_name, 'r') as myfile:
            data = myfile.read()


        result_dict = search_and_count(data,tokens_list,comb_list,search_flag)


    else:

        with open(file_name, 'r') as myfile:

            line = myfile.readline()

            line_dict = search_and_count(line, tokens_list, comb_list, abs(search_flag))

            for key in line_dict.keys():

                if key in result_dict.keys():

                    result_dict[key] += line_dict[key]

                else:

                    result_dict[key] = line_dict[key]


    return result_dict


def  search_and_count(text,tokens_list,comb_list,search_flag):

     res_dict = {}

     for i in range(0,len(comb_list)):

         tokens_in_group = comb_list[i]

         search_dict = search_groups(text, tokens_in_group, tokens_list, search_flag )

         res_dict = {**res_dict, **search_dict}

     return res_dict

def   search_groups(text, tokens_in_group,tokens_list, search_flag ) :

      search_dict = {}

      index_list = list(range(0,len(tokens_list)))

      if tokens_in_group == 1 :

         for j in range(0,len(tokens_list)):

             curr_str = tokens_list[j]

             ncount = count_string_occurrence(text, curr_str, search_flag)

             search_dict[curr_str] = ncount

      if (tokens_in_group > 1) and ( tokens_in_group <= len(tokens_list)) :

           combinations = list(itertools.combinations(index_list,tokens_in_group))

           for combination  in combinations:

               permutations = list(itertools.permutations(combination))


               for permutation in permutations :

                   curr_str = ''
                   for k in permutation:

                       curr_str = curr_str.join(tokens_list[k])

                   ncount = count_string_occurrence(text, curr_str, search_flag)

                   search_dict[curr_str] = ncount


      return search_dict


def  count_string_occurrence(text, sub_str, search_flag):

     ncount = 0

     if search_flag == 1 :

         ncount = text.count(sub_str)


     return ncount


if __name__ == "__main__":


    code_file_name = 'C:\\User\\t_delphi_examp.txt'

    tokens_list = ['T', 'Form4', 'Color']
    comb_list = [1]
    search_flag = 1

    stat_dict = get_tokens_statistics(code_file_name,tokens_list,comb_list,search_flag)

    x = 0
