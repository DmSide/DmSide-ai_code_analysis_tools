import unittest
from os.path  import join
from source_code.classifier import Classifier as verified_class

classifier = verified_class()

class ClassifierTesting(unittest.TestCase):

    def test_ispython(self):
        path = join('unit_testing', 'python')
        classifier(path)
        self.assertEqual(classifier(path),(path,1,0))


if __name__ == '__main__':
    unittest.main()
