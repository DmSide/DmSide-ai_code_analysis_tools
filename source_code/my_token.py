#!/usr/bin/env python
#-*- coding: utf-8 -*-

import itertools

class TokenCode :

    def __init__(self, code_file_name):


        self.not_separatores_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                                     'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                                     '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        self.capital_letters_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                                     'N', 'M', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


        self.separatores_list = [ ' ', '_', '(', ')', '[', ']', '{', '}', '=', '!', '<', '>', '?', '\t', '\r', '\b', '\n',
                                  '\f', ',', '.',  ':', ';', '+', '-', '+', '*', '/', '&', '%', '@', '$', '#', '"',"'",
                                  '^', '~' ]



        self.code_file_name = code_file_name

        result_list,  self.tokens_dict = self.read_and_token_lines()

        self.result_list = list(itertools.chain.from_iterable(result_list))

    def read_and_token_lines(self):
        result_list = list()
        tokens_dict = {}
        tokens_keys_list = tokens_dict.keys()
        tl = len(tokens_keys_list)

        with open(self.code_file_name,'r') as f:
             for line in f:
                 curr_tokens_list, tokens_dict = self.tokenize_line(line, tokens_dict)
                 result_list.append(curr_tokens_list)

        return [result_list, tokens_dict]

    def tokenize_line(self,line,tokens_dict) :

        line_list = list()
        comment_list = list()
        curr_list = list()

        npos = 0
        ncapitals = 0
        capital_positions_list = list()
        capital_positions_list.append(-1)

        for i in range(0,len(line)):

            curr_symb = line[i]

            # if curr_symb == '4':
            #      symb1 = line[i + 1]
            #
            #      ord0 = ord('.')
            #      ord1 = ord(symb1)
            #      print(symb1)
            #     x = 0




            if not ((curr_symb in self.not_separatores_list) or (curr_symb in self.capital_letters_list) or (curr_symb in  self.separatores_list)):
                curr_list.append(curr_symb)
                capital_positions_list.append(-1)
                npos = npos + 1

            if curr_symb in self.not_separatores_list :
               curr_list.append(curr_symb)
               capital_positions_list.append(-1)
               npos = npos + 1

            if curr_symb in self.capital_letters_list:
                curr_list.append(curr_symb)
                capital_positions_list.append(1)
                ncapitals = ncapitals + 1
                npos = npos + 1

            if curr_symb in  self.separatores_list:

                if (len(curr_list) > 0) and (ncapitals == 0):
                    curr_str = ''.join(curr_list)
                    line_list.append(curr_str)
                    if curr_str in tokens_dict.keys():
                        tokens_dict[curr_str] = tokens_dict[curr_str] + 1
                    else:
                        tokens_dict[curr_str] = 1



                if (len(curr_list) > 0) and (ncapitals > 0 ) :

                    capitals_separate_list = self.capitals_separate(curr_list,capital_positions_list)

                    for symb_list in capitals_separate_list:
                        curr_str = ''.join(symb_list)
                        line_list.append(curr_str)
                        if curr_str in tokens_dict.keys():
                            tokens_dict[curr_str] = tokens_dict[curr_str] + 1
                        else:
                            tokens_dict[curr_str] = 1



                curr_str = ''.join([curr_symb])
                if curr_str in tokens_dict.keys():
                    tokens_dict[curr_str] = tokens_dict[curr_str] + 1
                else:
                    tokens_dict[curr_str] = 1

                line_list.append(curr_str)
                curr_list = list()
                npos = 0
                ncapitals = 0
                capital_positions_list = list()
                capital_positions_list.append(-1)

        return  [ line_list, tokens_dict ]

    def capitals_separate(self,curr_list,capital_positions_list):
        list_of_sublists = list()
        cap_pos_list = list()
        cap_pos_list.append(0)
        npos = 0
        for i in range(2,len(capital_positions_list) - 2):

            #if (i > 1) and (capital_positions_list[i-1] < 0) and(capital_positions_list[i] > 0) and (capital_positions_list[i+1] < 0):
            if (i > 1) and (capital_positions_list[i] > 0) and( (capital_positions_list[i - 1] < 0) or (capital_positions_list[i + 1] < 0)):
                cap_pos_list.append(i-1)
                npos = npos + 1

        cap_pos_list.append(len(curr_list))

        if npos < 1 :
            return [curr_list]

        else:
            for j in range(0,len(cap_pos_list) - 1):

                sublist = curr_list[cap_pos_list[j] : cap_pos_list[j + 1]]
                list_of_sublists.append(sublist)


            return list_of_sublists

if __name__ == "__main__":


    #code_file_name = 'C:\\User\\test_token.txt'

    #code_file_name = 'C:\\User\\one_two_three.txt'

    #code_file_name = 'C:\\User\\my_token.txt'

    #code_file_name = 'C:\\User\\cpp_examp.cpp'

    #code_file_name = 'C:\\User\\basic_examp.bsc'

    code_file_name = 'C:\\User\\t_delphi_examp.txt'

    token_code =  TokenCode( code_file_name)

    token_code.read_and_token_lines()

    r_t = token_code.result_list

   # all_tokens_list = list(itertools.chain.from_iterable(r_t))

    t_d = token_code.tokens_dict

    for i in range(0,len(r_t)):
        print('LINE N ', i + 1)
        print(r_t[i])



    x = 0