from pathlib import Path
from subprocess import call
from typing import Union
import os

class DriverCOSIM:
    '''
        Class to run COSIM models in Windows.
        This class was written with the help of G. Vallone (LBNL).
    '''

    def __init__(self, COSIM_path: str, path_folder_COSIM: str, verbose: bool = False):
        '''
        Initialize class to run COSIM models.

        :param COSIM_path: Path to COSIM executable, for example: \\eosproject-smb\eos\project\s\steam\download\cosim\steam-cosim_v0.5.exe
        :param path_folder_COSIM: Path to COSIM library folder
        :param verbose: If True, print some logging information
        '''

        # Unpack arguments
        self.COSIM_path = COSIM_path
        self.path_folder_COSIM = path_folder_COSIM
        self.verbose = verbose
        if verbose:
            print(f'COSIM_path: {COSIM_path}')
            print(f'path_folder_COSIM: {path_folder_COSIM}')
            print(f'verbose: {verbose}')

    def run(self, simulation_name: str, sim_number: Union[str, int], verbose: bool = None):
        '''
        Run the COSIM model
        :param simulation_name: Name of the co-simulation model to run
        :param sim_number: String or number identifying the simulation to run
        :param verbose: If True, print some logging information
        :return: null
        '''
        if verbose == None:
            verbose = self.verbose
        # Define string to run
        callString = self._make_callString(model_name=simulation_name, sim_number=sim_number)
        if verbose:
            print(f'DriverCOSIM - Call string:\n{callString}')

        # Run
        call(callString, shell=False)
        if verbose:
            print(f'DriverCOSIM - Run finished for the called string:\n{callString}')


    def _make_callString(self, model_name: str, sim_number: Union[str, int], ):
        '''
        Write the sring that will be used to call COSIM
        :param model_name: Name of the co-simulation model to run
        :param sim_number: String or number identifying the simulation to run
        :return: null
        '''
        config_file_name = Path(os.path.join(self.path_folder_COSIM, model_name, str(sim_number), 'Input', 'COSIMConfig.json')).resolve()
        callString = (f'java -jar {self.COSIM_path} {config_file_name}')
        return callString