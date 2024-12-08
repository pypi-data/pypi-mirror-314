from spicelib import SpiceEditor, SimRunner, RawRead, LTSteps
from spicelib.simulators.ltspice_simulator import LTspice
from pathlib import Path

# You should replace it by your own executor path.

output_folder = "./py_sim_out"

runner = SimRunner(output_folder=output_folder, parallel_sims=16, simulator=LTspice)

for time in range(1, 200, 1):
    netlist = SpiceEditor('stuck_template.net')
    runner.run(netlist, run_filename=f'test{time}.net')

runner.wait_completion()