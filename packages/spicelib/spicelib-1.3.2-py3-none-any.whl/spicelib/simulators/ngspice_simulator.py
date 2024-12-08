#!/usr/bin/env python
# coding=utf-8

# -------------------------------------------------------------------------------
#
#  ███████╗██████╗ ██╗ ██████╗███████╗██╗     ██╗██████╗
#  ██╔════╝██╔══██╗██║██╔════╝██╔════╝██║     ██║██╔══██╗
#  ███████╗██████╔╝██║██║     █████╗  ██║     ██║██████╔╝
#  ╚════██║██╔═══╝ ██║██║     ██╔══╝  ██║     ██║██╔══██╗
#  ███████║██║     ██║╚██████╗███████╗███████╗██║██████╔╝
#  ╚══════╝╚═╝     ╚═╝ ╚═════╝╚══════╝╚══════╝╚═╝╚═════╝
#
# Name:        ngspice_simulator.py
# Purpose:     Tool used to launch NGspice simulations in batch mode.
#
# Author:      Nuno Brum (nuno.brum@gmail.com)
#
# Created:     23-02-2023
# Licence:     refer to the LICENSE file
# -------------------------------------------------------------------------------

from pathlib import Path
from typing import Union
import logging
from ..sim.simulator import Simulator, run_function, SpiceSimulatorError
import os
import shutil

_logger = logging.getLogger("spicelib.NGSpiceSimulator")


class NGspiceSimulator(Simulator):
    """Stores the simulator location and command line options and runs simulations."""
    # Placed in order of preference. The first to be found will be used.
    _spice_exe_paths = ["C:/Apps/NGSpice64/bin/ngspice.exe",  # Windows
                        "C:/Spice64/ngspice.exe",  # Windows, older style
                        "/usr/local/bin/ngspice",  # MacOS and linux
                        "ngspice"  # linux, when in path
                        ]
    
    # the default lib paths, as used by get_default_library_paths
    # none
    _default_lib_paths = []
    
    # defaults:
    spice_exe = []
    process_name = None      
    
    # determine the executable to use
    for exe in _spice_exe_paths:
        if exe.startswith("~"):
            exe = os.path.expanduser(exe)
        if os.path.exists(exe):
            spice_exe = [exe]
            break
        else:
            # check if file in path
            if shutil.which(exe):
                spice_exe = [exe]
                break

    # The following variables are not needed anymore. This also makes sphinx not mention them in the documentation.
    del exe

    # fall through        
    if len(spice_exe) == 0:
        spice_exe = []
        process_name = None
    else:
        process_name = Simulator.guess_process_name(spice_exe[0])
        _logger.debug(f"Found ngspice installed in: '{spice_exe}' ")
    
    ngspice_args = {
        '-a'            : ['-a'],
        '--autorun'     : ['--autorun'],  # run the loaded netlist
        '-b'            : ['-b'],
        '--batch'       : ['--batch'],  # process FILE in batch mode
        '-c'            : ['-c', '<FILE>'],  #
        '--circuitfile' : ['--circuitfile', '<FILE>'],  # set the circuitfile
        '-D'            : ['-D', 'var_value'],  #
        '--define'      : ['--define', 'var_value'],  # define variable to true/[value]
        '-i'            : ['-i'],  #
        '--interactive' : ['--interactive'],  # run in interactive mode
        '-n'            : ['-n'],  #
        '--no-spiceinit': ['--no-spiceinit'],  # don't load the local or user's config file
        '-o'            : ['-o', '<FILE>'],  #
        '--output'      : ['--output', '<FILE>'],  # set the outputfile
        '-p'            : ['-p'],  #
        '--pipe'        : ['--pipe'],  # run in I/O pipe mode
        '-q'            : ['-q'],  #
        '--completion'  : ['--completion'],  # activate command completion
        '-r'            : ['-r'],  #
        '--rawfile'     : ['--rawfile', '<FILE>'],  # set the rawfile output
        '--soa-log'     : ['--soa-log', '<FILE>'],  # set the outputfile for SOA warnings
        '-s'            : ['-s'],  #
        '--server'      : ['--server'],  # run spice as a server process
        '-t'            : ['-t', '<TERM>'],  #
        '--term'        : ['--term', '<TERM>'],  # set the terminal type
        '-h'            : ['-h'],  #
        '--help'        : ['--help'],  # display this help and exit
        '-v'            : ['-v'],  #
        '--version'     : ['--version'],  # output version information and exit
    }
    """:meta private:"""
    
    _default_run_switches = ['-b', '-o', '-r', '-a']
    _compatibility_mode = 'kiltpsa'

    @classmethod
    def valid_switch(cls, switch, parameter='') -> list:
        """
        Validates a command line switch. The following options are available for NGSpice:

        :param switch: switch to be added. If the switch is not on the list above, it should be correctly formatted with
                    the preceding '-' switch
        :type switch: str
        :param parameter: parameter for the switch
        :type parameter: str, optional
        :return: the correct formatting for the switch
        :rtype: list
        """
        ret = []  # This is an empty switch
        parameter = parameter.strip()
        if switch in cls.ngspice_args:
            if switch in cls._default_run_switches:
                _logger.info(f"Switch {switch} is already in the default switches")
                return ret
            if cls.set_compatibility_mode and (switch == '-D' or switch == '--define') and parameter.lower().startswith("ngbehavior"):
                _logger.info(f"Switch {switch} {parameter} is already in the default switches, use 'set_compatibility_mode' instead")
                return ret                
            switch_list = cls.ngspice_args[switch]
            if len(switch_list) == 2:
                param_token = switch_list[1]
                if param_token == '<FILE>' or param_token == '<TERM>' or (param_token == 'var_value' and '=' in parameter):
                    ret = [switch_list[0], parameter]
                else:
                    _logger.warning(f"Invalid parameter {parameter} for switch '{switch}'")
            else:
                ret = switch_list
        else:
            _logger.warning(f"Invalid Switch {switch}")
        return ret

    @classmethod
    def run(cls, netlist_file: Union[str, Path], cmd_line_switches: list = None, timeout: float = None, stdout=None, stderr=None) -> int:
        """Executes a NGspice simulation run.

        :param netlist_file: path to the netlist file
        :type netlist_file: Union[str, Path]
        :param cmd_line_switches: additional command line options. Best to have been validated by valid_switch(), defaults to None
        :type cmd_line_switches: list, optional
        :param timeout: If timeout is given, and the process takes too long, a TimeoutExpired exception will be raised, defaults to None
        :type timeout: float, optional
        :param stdout: control redirection of the command's stdout. Valid values are None, subprocess.PIPE, subprocess.DEVNULL, an existing file descriptor (a positive integer), and an existing file object with a valid file descriptor. With the default settings of None, no redirection will occur. 
        :type stdout: _FILE, optional
        :param stderr: Like stdout, but affecting the command's error output.
        :type stderr: _FILE, optional
        :raises SpiceSimulatorError: when the executable is not found.
        :raises NotImplementedError: when the requested execution is not possible on this platform.
        :return: return code from the process
        :rtype: int
        """
        if not cls.spice_exe:
            _logger.error("================== ALERT! ====================")
            _logger.error("Unable to find the NGSPICE executable.")
            _logger.error("A specific location of the NGSPICE can be set")
            _logger.error("using the create_from(<location>) class method")
            _logger.error("==============================================")
            raise SpiceSimulatorError("Simulator executable not found.")    
        
        if cmd_line_switches is None:
            cmd_line_switches = []
        elif isinstance(cmd_line_switches, str):
            cmd_line_switches = [cmd_line_switches]
        netlist_file = Path(netlist_file)        
            
        logfile = Path(netlist_file).with_suffix('.log').as_posix()
        rawfile = Path(netlist_file).with_suffix('.raw').as_posix()
        extra_switches = []
        if cls._compatibility_mode:
            extra_switches = ['-D', f"ngbehavior={cls._compatibility_mode}"]
        #TODO: -a seems useless with -b, however it is still defined in the default switches. Need to check if it is really needed.
        cmd_run = cls.spice_exe + cmd_line_switches + extra_switches + ['-b'] + ['-o'] + [logfile] + ['-r'] + [rawfile] + [netlist_file]
        # start execution
        return run_function(cmd_run, timeout=timeout, stdout=stdout, stderr=stderr)
    
    @classmethod
    def set_compatibility_mode(cls, mode: str):
        """
        Set the compatibility mode. It has become mandatory in recent ngspice versions, as the default 'all' is no longer valid.
        
        A good default seems to be "kiltpsa" (KiCad, LTspice, PSPICE, netlists)
        
        The following compatibility modes are available (as of mid 2024, ngspice v43):
        
        * a : complete netlist transformed
        
        * ps : PSPICE compatibility
        
        * hs : HSPICE compatibility
        
        * spe : Spectre compatibility
        
        * lt : LTSPICE compatibility
        
        * s3 : Spice3 compatibility
        
        * ll : all (currently not used)
        
        * ki : KiCad compatibility
        
        * eg : EAGLE compatibility
        
        * mc : for ’make check’
        
        :param mode: the compatibility mode to be set. Set to None to remove the compatibility setting.
        :type mode: str
        """
        cls._compatibility_mode = mode

