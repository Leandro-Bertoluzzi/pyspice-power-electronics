#r# ============================================
#r#  Full converter with SCR
#r# ============================================

#r# This example shows the simulation of a controlled full converter with SCRs

######################################### IMPORT MODULES #########################################

import matplotlib.pyplot as plt
import numpy as np

######################################### IMPORT UTILITIES #########################################

import sys, os

if os.environ.get('IN_CONTAINER') == 'Yes':
    sys.path.insert(1, '/root/utilities/')
else:
    sys.path.insert(1, '../utilities/')

from utilities import format_output, get_output_file_name

####################################################################################################

import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

####################################################################################################

from PySpice.Probe.Plot import plot
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

############################# LIBRARIES WITH DEFINITIONS OF COMPONENTS #############################

if os.environ.get('IN_CONTAINER') == 'Yes':
    libraries_path = '/root/libraries'
else:
    libraries_path = '../libraries'
spice_library = SpiceLibrary(libraries_path)

#####################################################################################################
# DEFINING PLOTS
#####################################################################################################

figure1, (ax1, ax2) = plt.subplots(2, 1, figsize=(20, 10))

####################################################################################################
# CIRCUIT DEFINITION
####################################################################################################

circuit = Circuit('Full converter with SCR')

# Input voltage
source = circuit.SinusoidalVoltageSource('input', 'A', circuit.gnd, amplitude=10@u_V, frequency=500@u_Hz)

# Simple RC circuit
circuit.R('1', 'A', 'output', 100@u_Ω)
circuit.C('1', 'output', circuit.gnd, 10@u_nF)

# Show the netlist
print('**** Circuit netlist: ****')
print(circuit)

####################################################################################################
# SIMULATION
####################################################################################################

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.ac(start_frequency=20@u_kHz, stop_frequency=20@u_MHz, number_of_points=10,  variation='dec')

# Conversion factor
RAD_TO_DEG = 180 / np.pi

# Formatting results
voltages, currents = format_output(analysis, 'ac')
v_output_magnitude = voltages['output']['magnitude']
v_output_phase = voltages['output']['phase'] * RAD_TO_DEG
f = voltages['frequency']

# Plot magnitude
ax1.set_title('Magnitude')
ax1.set_xlabel('Frequency [Hz]')
ax1.set_ylabel('Voltage [V]')
ax1.grid()
ax1.set_xscale("log")
ax1.plot(f, v_output_magnitude)
ax1.legend('output', loc=(.05,.1))
ax1.set_ylim(-0.1, 1.1)

# Plot phase
ax2.set_title('Phase')
ax2.set_xlabel('Frequency [Hz]')
ax2.set_ylabel('Voltage [V]')
ax2.grid()
ax2.set_xscale("log")
ax2.plot(f, v_output_phase)
ax2.legend('output', loc=(.05,.1))
ax2.set_ylim(-190.0, 190.0)

####################################################################################################

# Save/show plots
if os.environ.get('IN_CONTAINER') == 'Yes':
    file_name = get_output_file_name("RC-lowpass.png")
    plt.savefig(file_name)
else:
    plt.show()