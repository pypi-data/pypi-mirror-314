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
# Name:        xyce_simulator.py
# Purpose:     Tool used to launch xyce simulations in batch mode.
#
# Author:      Nuno Brum (nuno.brum@gmail.com)
#
# Created:     14-03-2023
# Licence:     refer to the LICENSE file
# -------------------------------------------------------------------------------

from pathlib import Path
from typing import Union
import logging
from ..sim.simulator import Simulator, run_function, SpiceSimulatorError

_logger = logging.getLogger("spicelib.XYCESimulator")


class XyceSimulator(Simulator):
    """Stores the simulator location and command line options and runs simulations."""
    spice_exe = ["C:/Program Files/Xyce 7.6 NORAD/bin/xyce.exe"]
    process_name = "XVIIx64.exe"
    xyce_args = {
        '-b'                : ['-b'],  # batch mode flag for spice compatibility (ignored)
        '-h'                : ['-h'],  # print usage and exit
        '-v'                : ['-v'],  # print version info and exit
        '-capabilities'     : ['-capabilities'],  # print compiled-in options and exit
        '-license'          : ['-license'],  # print license and exit
        '-param'            : ['-param', '<param_options>'],
        # [device [level [<inst|mod>]]] print a terse summary of model and/or device parameters
        '-doc'              : ['-doc', '<param_options>'],
        # [device [level [<inst|mod>]]] output latex tables of model and device parameters to files
        '-doc_cat'          : ['-doc_cat', '<param_options>'],
        # [device [level [<inst|mod>]]] output latex tables of model and device parameters to files
        '-count'            : ['-count'],  # device count without netlist syntax or topology check
        '-syntax'           : ['-syntax'],  # check netlist syntax and exit
        '-norun'            : ['-norun'],  # netlist syntax and topology and exit
        '-namesfile'        : ['-namesfile', '<path>'],  # output internal names file to <path> and exit
        '-noise_names_file' : ['-noise_names_file', '<path>'],  # output noise source names file to <path> and exit
        '-quiet'            : ['-quiet'],  # suppress some of the simulation-progress messages sent to stdout
        '-jacobian_test'    : ['-jacobian_test'],  # jacobian matrix diagnostic
        '-hspice-ext'       : ['-hspice-ext', '<hsext_options>'],
        # apply hspice compatibility features during parsing.  option=all applies them all
        '-redefined_params' : ['-redefined_params', '<redef_param_option>'],
        # set option for redefined .params as ignore (use last), usefirst, warn or error
        '-subckt_multiplier': ['-subckt_multiplier', '<truefalse_option>'],
        # set option to true(default) or false to apply implicit subcircuit multipliers
        '-delim'            : ['-delim', '<delim_option>'],  # <TAB|COMMA|string>   set the output file field delimiter
        '-o'                : ['-o', '<basename>'],  # <basename> for the output file(s)
        '-l'                : ['-l', '<path>'],  # place the log output into <path>, "cout" to log to stdout
        '-per-processor'    : ['-per-processor'],  # create log file for each processor, add .<n>.<r> to log path
        '-remeasure'        : ['-remeasure', '<path>'],
        # [existing Xyce output file] recompute .measure() results with existing data
        '-nox'              : ['-nox', 'onoff_option'],  # <on|off>               NOX nonlinear solver usage
        '-linsolv'          : ['-linsolv', '<solver>'],  # <solver>           force usage of specific linear solver
        '-maxord'           : ['-maxord', '<int_option>'],  # <1..5>              maximum time integration order
        '-max'              : ['-max', '<int_option>'],  # -warnings <#>           maximum number of warning messages
        '-prf'              : ['-prf', '<path>'],  # <param file name>      specify a file with simulation parameters
        '-rsf'              : ['-rsf', '<path>'],  # specify a file to save simulation responses functions.
        '-r'                : ['-r', '<path>'],  # <file>   generate a rawfile named <file> in binary format
        '-a'                : ['-a', '<path>'],  # use with -r <file> to output in ascii format
        '-randseed'         : ['-randseed', '<int_option>'],
        # <number>          seed random number generator used by expressions and sampling methods
    }
    """:meta private:"""

    @classmethod
    def valid_switch(cls, switch, parameter='') -> list:
        """
        Validates a command line switch. The following options are available for Xyce:

        :param switch: switch to be added. If the switch is not on the list above, it should be correctly formatted with the preceding '-' switch
        :type switch: str
        :param parameter: parameter for the switch
        :type parameter: str, optional
        :return: the correct formatting for the switch
        :rtype: list
        """
        ret = []  # This is an empty switch
        if switch in cls.xyce_args:
            switch_list = cls.xyce_args[switch]
            if len(switch_list) == 2:
                param_token = switch_list[1]
                if param_token == '<path>':
                    ret = [switch_list[0], parameter]
                elif param_token == '<param_options>':
                    # Check for [device [level [<inst|mod>]]] syntax ??
                    ret = [switch_list[0], parameter]
                elif param_token == '<hsext_options>':
                    ret = [switch_list[0], parameter]
                elif param_token == '<redef_param_option>':
                    if parameter in ('ignore', 'uselast', 'usefirst', 'warn', 'error'):
                        ret = [switch_list[0], parameter]
                elif param_token == '<truefalse_option>':
                    if parameter.lower() in ('true', 'false'):
                        ret = [switch_list[0], parameter]
                elif param_token == '<delim_option>':
                    ret = [switch_list[0], parameter]
                elif param_token == '<onoff_option>':
                    if parameter.lower() in ('on', 'off'):
                        ret = [switch_list[0], parameter]
                elif param_token == '<int_option>':
                    try:
                        int(parameter)
                    except ValueError:
                        pass
                    else:
                        ret = [switch_list[0], parameter]
                else:
                    _logger.warning(f"Invalid parameter {parameter} for switch '{switch}'")
            else:
                ret = switch_list
        else:
            _logger.error(f"Invalid Switch {switch}")
        return ret

    @classmethod
    def run(cls, netlist_file: Union[str, Path], cmd_line_switches: list = None, timeout: float = None, stdout=None, stderr=None) -> int:
        """Executes a LTspice simulation run.

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
            _logger.error("Unable to find the Xyce executable.")
            _logger.error("A specific location of the Xyce can be set")
            _logger.error("using the create_from(<location>) class method")
            _logger.error("==============================================")
            raise SpiceSimulatorError("Simulator executable not found.")
        
        if cmd_line_switches is None:
            cmd_line_switches = []
        elif isinstance(cmd_line_switches, str):
            cmd_line_switches = [cmd_line_switches]
        netlist_file = Path(netlist_file)
        
        cmd_run = cls.spice_exe + cmd_line_switches + [netlist_file]
        # start execution
        return run_function(cmd_run, timeout=timeout, stdout=stdout, stderr=stderr)
