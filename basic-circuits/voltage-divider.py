#r# ============================================
#r#  Resistive voltage divider
#r# ============================================

#r# This example shows the simulation of a simple voltage divider made of resistances

####################################################################################################

import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

####################################################################################################

from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

####################################################################################################
# CIRCUIT DEFINITION
####################################################################################################

circuit = Circuit('Voltage divider')

# Define the netlist
circuit.V('in', 'input', circuit.gnd, 10@u_V)
circuit.R(1, 'input', 'out', 8@u_kOhm)
circuit.R(2, 'out', circuit.gnd, 2@u_kOhm)

# Show the netlist
print('**** Circuit netlist: ****')
print(circuit)

####################################################################################################
# SIMULATION
####################################################################################################

# Set up the simulation
simulator = circuit.simulator(temperature=25, nominal_temperature=25)

# Run the simulation
analysis = simulator.operating_point()

# Show results
print('**** Simulation result: ****')
out_value = float(analysis.nodes['out'])
print(out_value)