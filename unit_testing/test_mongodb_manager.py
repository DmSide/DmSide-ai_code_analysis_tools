import unittest
import sys
import traceback

if sys.version_info >= (2, 7) and sys.version_info[0] != 3:
    """ Starting with major version 3 python unittest module include mock module
     for python >= 2.7 with micro versions mock module installing
      via: pip install mock   
    """
    try:
        from mock import Mock, patch
    except ImportError as Error:
        print("Couldn't import mock module, check it was be installed")
        raise ImportError
else:
    from unittest.mock import Mock, patch

#import source_code.testviews as views



class set_expected_output:
    """
    This is the decorator class,
    but it is named according to the style of naming functions or methods.

    named arguments:
        expected_return
        output_type
    """

    def __init__(self, **kwargs):
        # supports only named variables,
        # this class work like a decorator with arguments ,
        # it's enough flexible for wide range of methods

        self.expected_return = kwargs[
            'expected_return'] if 'expected_return' in kwargs else None
        self.expected_return_type = kwargs[
            'output_type'] if 'output_type' in kwargs else {'status': bool,
                                                            'response': dict,
                                                            'error': dict}

    def __call__(self, t_method):
        def tested_method(*args, **kwargs):
            ut = unittest.TestCase
            method_return = t_method(*args, **kwargs)
            ut.assertIsInstance(args[0], method_return,
                                type(self.expected_return),
                                'Unexpected output type')
            if self.expected_return_type is not None:
                if isinstance(self.expected_return_type, dict):
                    # check keys
                    ut.assertEqual(args[0], method_return.keys(),
                                   self.expected_return_type.keys(),
                                   'Different output structure')
                    # check types and

                    #TODO then return_type is none fix conditions

                    for __type in self.expected_return_type:
                        with ut.subTest(args[0], Check_dtype=__type):
                            ut.assertIsInstance(args[0],
                                                method_return[__type],
                                                self.expected_return_type[
                                                    __type],
                                                'Unexpected output type')

                        with ut.subTest(args[0], Check_data=__type):
                            ut.assertEqual(args[0], method_return[__type],
                                           self.expected_return[__type],
                                           'Unexpected output')

                else:

                    pass
                    # it is not similar to already exist project,
                    # but in future...

        return tested_method


def test_method_stability(self, t_method, input_arguments):
    ##########################################
    # input_arguments  [[1,2,3,4,5],{1:1,2:2}] or [[],dict()] {} is empty set
    # equivalent       [*args , **kwargs]
    ut = unittest.TestCase
    ut.assertIsInstance(input_arguments, (list, tuple),
                        'Wrog format of input arguments')
    for iter_arguments in input_arguments:
        with ut.subTest(self, arguments= iter_arguments):
            args, kwargs = iter_arguments
            try:
                _ = t_method(*args, **kwargs)
            except:
                msg = 'Error'
                raise AssertionError(msg)



def test_api_method():
    pass


##########################for testing functionality ############################
class Test:

    def method_1(self):
        output = dict.fromkeys(["status", "response", "error"], True)
        output['response'] = {1: 2, 1: 2}
        output['response'].update({'new': self.method_2()})
        output['error'] = {}
        return output

    def method_2(self):
        return 13


aaa = Test()
bb = aaa.method_1()


######################

class TestMongoDBManager(unittest.TestCase):

    @set_expected_output(expected_return=bb,
                      output_type={'status': bool,
                                   'response': dict,
                                   'error': dict})
    def test_case(self):
        # print('This is test case:',self) # testing

        # just as an example
        # do some preparations such creating instance, mock some methods or
        # properties and return method which need test. In decorator argument
        # we could set expected return of method , type of return
        # and check behavior with input incorrect args

        a = Test()
        mock_method = Mock()
        mock_method.retutn_value = 'Mock_return'
        # a.method_2 = mock_method
        return a.method_1()


if __name__ == '__main__':
    unittest.main(verbosity=2)
