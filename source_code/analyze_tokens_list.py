from my_token import TokenCode

def statist_research(tokens_list, interval_list):

    token_groups_list = list()
    groups_count_list = list()

    for n_inter in interval_list :

         met_group_list = list()

         for i in range(0,len(tokens_list) - n_inter + 1):
             curr_tokens_group = tokens_list[i : i + n_inter]
             if not (curr_tokens_group in met_group_list):
                 ncount = count_group_in_tokens(tokens_list,curr_tokens_group,i+1,n_inter)
                 met_group_list.append(curr_tokens_group)
                 token_groups_list.append(curr_tokens_group)
                 groups_count_list.append(ncount + 1)


    return[ token_groups_list, groups_count_list]

def count_group_in_tokens(tokens_list,search_tokens_group,ini_index,n_inter):

    ncount = 0
    for i in range(ini_index,len(tokens_list) - n_inter + 1):
        curr_tokens_group = tokens_list[i: i + n_inter]
        compare = compare_tokens_groups(curr_tokens_group,search_tokens_group)
        if compare:
            ncount += 1

    return ncount

def  compare_tokens_groups(curr_tokens_group,search_tokens_group) :

     for i in range (0,len(search_tokens_group)):

         if  curr_tokens_group[i] != search_tokens_group[i]:
              return False

     return True

if __name__ == "__main__":

   #tokens_list =  ['a','b','a', 'b']
   #interval_list = [1, 2]

   code_file_name = 'C:\\User\\python_gas_diagram_processing\\source_code\\get_graphic.py'

   # #code_file_name = 'C:\\User\\t_delphi_examp.txt'
   #
   # code_file_name = 'C:\\User\\cpp_examp.cpp'
   #
   token_code = TokenCode(code_file_name)

   token_code.read_and_token_lines()

   tokens_list = token_code.result_list
   #
   # t_d = token_code.tokens_dict
   #
   #interval_list = [1, 2, 3]
   interval_list = [1, 2]
   #
   # #interval_list = [1]

   token_groups_list, groups_count_list = statist_research(tokens_list, interval_list)

   for i  in range(0, len(token_groups_list)) :

       group_list = token_groups_list[i]
       n_occ = groups_count_list[i]

       print('GROUP =  ', group_list, '   ', n_occ )
