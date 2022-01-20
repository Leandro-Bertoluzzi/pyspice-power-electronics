#r# ============================================
#r#  Resistive voltage divider
#r# ============================================

#r# This example shows the simulation of a simple voltage divider made of resistances

######################################### IMPORT UTILITIES #########################################

import sys, os
# Insert at 1, 0 is the script path
# Inserting it at the beginning has the benefit of guaranteeing that the path is searched before others (even built-in ones) in the case of naming conflicts
if os.environ.get('IN_CONTAINER') == 'Yes':
    sys.path.insert(1, '/root/utilities/')
else:
    sys.path.insert(1, '../utilities/')

from utilities import format_output

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
voltages, currents = format_output(analysis, 'operating_point')
out_value = voltages['out']
print(out_value, " [V]")