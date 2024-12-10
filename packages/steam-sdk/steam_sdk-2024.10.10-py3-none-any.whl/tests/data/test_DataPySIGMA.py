import unittest
import os
from deepdiff import DeepDiff

from steam_sdk.data import DataPySIGMA as dS
from steam_sdk.parsers.ParserYAML import yaml_to_data
from steam_sdk.parsers.ParserYAML import dict_to_yaml


class TestModelData(unittest.TestCase):

    def setUp(self) -> None:
        """
            This function is executed before each test in this class
        """
        self.current_path = os.getcwd()
        os.chdir(os.path.dirname(__file__))  # move to the directory where this file is located
        print('\nCurrent folder:          {}'.format(self.current_path))
        print('\nTest is run from folder: {}'.format(os.getcwd()))

    def tearDown(self) -> None:
        """
            This function is executed after each test in this class
        """
        os.chdir(self.current_path)  # go back to initial folder

    def test_writeToFile_SIGMAData(self):
        """
            Check that DataFiQuS generates a structure with the same keys as a reference file
        """


        # arrange
        generated_file = os.path.join('output', f'data_model_magnet_SIGMA.yaml')
        reference_file = os.path.join('references', f'data_model_magnet_SIGMA_REFERENCE.yaml')

        # act
        data = dS.DataPySIGMA()
        dict_to_yaml(data.model_dump(), generated_file, list_exceptions=['Conductors'])

        # assert
        # Check that the generated file exists
        self.assertTrue(os.path.isfile(generated_file))

        # Check that the generated file is identical to the reference
        # TODO: Check that order of the keys is the same
        a = yaml_to_data(generated_file)
        b = yaml_to_data(reference_file)
        d_diff = DeepDiff(a, b, ignore_order=False)
        self.assertTrue(len(d_diff) == 0)
