#r# ============================================
#r#  Controlled half-wave rectifier with an SCR
#r# ============================================

#r# This example shows the simulation of ...

####################################################################################################

import matplotlib.pyplot as plt

####################################################################################################

import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

####################################################################################################

from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Probe.Plot import plot
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

############################# LIBRARIES WITH DEFINITIONS OF COMPONENTS #############################

libraries_path = '..\libraries'
spice_library = SpiceLibrary(libraries_path)

####################################################################################################
# DEFINING PLOTS
####################################################################################################

figure1, (ax1, ax2) = plt.subplots(2, 1, figsize=(20, 10))
figure2, (ax3, ax4) = plt.subplots(2, 1, figsize=(20, 10))

####################################################################################################
# RECTIFICATION
####################################################################################################

circuit = Circuit('SCR half wave rectifier')
R = 10@u_Ω
L = 100@u_mH
periods = 20 # Amount of periods of source signal to show in plot

####################################### UNFILTERED OUTPUT #######################################

# Input voltage
source = circuit.SinusoidalVoltageSource('input', 'source', circuit.gnd, amplitude=10@u_V, frequency=50@u_Hz)
# SCR gate triggering signal
alpha = 0.5 # trigger angle [0; 1]
delay_time = (source.period/2) * alpha
pulse_width = (source.period/2) * (1- alpha)
circuit.PulseVoltageSource('trigger', 'gate', 'output', 0@u_V, 1@u_V, delay_time=delay_time, pulse_width=pulse_width, period=source.period, rise_time=1@u_ms, fall_time=1@u_ms)
# SCR
circuit.include(spice_library['EC103D1'])
circuit.X('SCR', 'EC103D1', 'source', 'gate', 'output')
# Fli}yback diode Dm
circuit.include(spice_library['1N4148'])
circuit.X('Dm', '1N4148', circuit.gnd, 'output')
# Serie RL load
circuit.R('load', 'output', 'RL_middle', R)
circuit.L('1', 'RL_middle', circuit.gnd, L)

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
simulator.save_currents = True
analysis = simulator.transient(step_time=source.period/200, end_time=source.period*periods)

#for node in analysis.branches.values():
#    print(str(node)) # Fixme: format value + unit

ax1.set_title('Half-Wave Rectification - Voltage')
ax1.set_xlabel('Time [ms]')
ax1.set_ylabel('Voltage [V]')
ax1.grid()
ax1.plot(analysis['source'])
ax1.plot(analysis['gate'])
ax1.plot(analysis.output)
ax1.legend(('source', 'gate', 'output'), loc=(.05,.1))
ax1.set_ylim(float(-source.amplitude*1.1), float(source.amplitude*1.1))

output_current = analysis['l1'].as_ndarray()
max_current = output_current.max()
min_current = output_current.min()

print('Without filtering')
print(max_current)
print(min_current)

ax2.set_title('Half-Wave Rectification - Current')
ax2.set_xlabel('Time [ms]')
ax2.set_ylabel('Current [A]')
ax2.grid()
ax2.plot(analysis['l1'])
ax2.legend('l1', loc=(.05,.1))
ax2.set_ylim(float(1.1 * min_current), float(1.1 * max_current))

######################################## FILTERED OUTPUT ########################################

C = 10@u_mF

# We add a capacitor to filter the output voltage
circuit.C('1', 'output', circuit.gnd, C)

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
simulator.save_currents = True
analysis = simulator.transient(step_time=source.period/200, end_time=source.period*periods)

output_current = analysis['l1'].as_ndarray()
max_current = output_current.max()
min_current = output_current.min()

print('With filtering')
print(max_current)
print(min_current)

ax3.set_title('Half-Wave Rectification with filtering')
ax3.set_xlabel('Time [ms]')
ax3.set_ylabel('Voltage [V]')
ax3.grid()
ax3.plot(analysis['source'])
ax3.plot(analysis['gate'])
ax3.plot(analysis.output)
ax3.legend(('source', 'gate', 'output'), loc=(.05,.1))
ax3.set_ylim(float(-source.amplitude*1.1), float(source.amplitude*1.1))

ax4.set_title('Half-Wave Rectification with filtering - Current')
ax4.set_xlabel('Time [ms]')
ax4.set_ylabel('Current [A]')
ax4.grid()
ax4.plot(analysis['l1'])
ax4.legend('l1', loc=(.05,.1))
ax4.set_ylim(float(1.1 * min_current), float(1.1 * max_current))

plt.show()

####################################################################################################