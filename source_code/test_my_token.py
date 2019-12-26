#!/usr/bin/env python
# -*- coding: utf-8 -*-

from my_token import  TokenCode
from analyze_tokens_list import statist_research

#import mock
import unittest
from unittest.mock import Mock
from unittest.mock import patch

#import unittest.mock

class TokenCodeTestCase(unittest.TestCase):

    tk = TokenCode('C:\\User\\one_two_three.txt')

    def test_tokenize_line(self):

        test_line = '1. FirstTest ;' + '\n'
        true_result = ['1', '.', ' ', 'First', 'Test', ' ', ';', '\n']

        tk = TokenCode('C:\\User\\one_two_three.txt')
        tokens_dict = {}
        result, tokens_dict = tk.tokenize_line(test_line,tokens_dict)

        self.assertEqual(result, true_result)

    def test_capitals_separate(self):

        testlist = list('OneTwoThree')
        capital_positions_list = [-1,1,-1,-1,1,-1,-1,1,-1,-1,-1]

        tk = TokenCode('C:\\User\\one_two_three.txt')
        result = tk.capitals_separate(testlist,capital_positions_list)

        true_result = list()

        true_result.append(list('One'))
        true_result.append(list('Two'))
        true_result.append(list('Three'))

        self.assertEqual(result, true_result)



class AnalyzeTokensTestCase(unittest.TestCase):

    def test_statist_research(self):

        tokens_list = ['a', 'b', 'a', 'b']
        interval_list = [1, 2]

        result_group = [['a'],['b'],['a','b'], ['b', 'a']]
        result_count = [2, 2, 2, 1]

        test_group, test_count = statist_research(tokens_list, interval_list)

        self.assertEqual(test_group, result_group)
        self.assertEqual(test_count, result_count)



if __name__ == '__main__':

    tokenTestSuite = unittest.TestSuite()
    tokenTestSuite.addTest(unittest.makeSuite(TokenCodeTestCase))
    tokenTestSuite.addTest(unittest.makeSuite(AnalyzeTokensTestCase))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(tokenTestSuite)


    #unittest.main()