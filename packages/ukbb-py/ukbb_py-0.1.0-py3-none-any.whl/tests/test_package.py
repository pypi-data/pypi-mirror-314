import unittest
from ukbb_py.UKBB_Health_Records_New_Project import read_GP

class TestPackage(unittest.TestCase):
    def test_read_GP(self):
        gp_codes = ['XE2eD', '22K..']
        project_folder = 'test_project'
        result = read_GP(gp_codes, project_folder)
        self.assertIsNotNone(result)
        # Add more assertions to verify the correctness of 'result'

if __name__ == '__main__':
    unittest.main()