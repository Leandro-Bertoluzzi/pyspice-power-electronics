#r# ============================================
#r#  Controlled half-wave rectifier with an SCR
#r# ============================================

#r# This example shows the simulation of a controlled half-wave rectifier with an SCR with an RL load

#####################################################################################################

import matplotlib.pyplot as plt
import numpy

#####################################################################################################

import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

#####################################################################################################

from PySpice.Probe.Plot import plot
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

############################# LIBRARIES WITH DEFINITIONS OF COMPONENTS #############################

libraries_path = '..\libraries'
spice_library = SpiceLibrary(libraries_path)

#####################################################################################################
# DEFINING PLOTS
#####################################################################################################

figure1, (ax1, ax2) = plt.subplots(2, 1, figsize=(20, 10))
figure2, (ax3, ax4) = plt.subplots(2, 1, figsize=(20, 10))

####################################################################################################
# CIRCUIT DEFINITION
####################################################################################################

circuit = Circuit('SCR half wave rectifier')
R = 10@u_Ω
L = 100@u_mH
periods = 10 # Amount of periods of source signal to show in plot

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
circuit.X('scr', 'EC103D1', 'source', 'gate', 'output')
# Flyback diode Dm
circuit.include(spice_library['1N4148'])
circuit.X('Dm', '1N4148', circuit.gnd, 'output')
# Series RL load
circuit.R('load', 'output', 'RL_middle', R)
circuit.L('1', 'RL_middle', circuit.gnd, L)

# Show the netlist
print('**** Circuit netlist: ****')
print(circuit)

####################################################################################################
# SIMULATION
####################################################################################################

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
simulator.save_currents = True
analysis = simulator.transient(step_time=source.period/50000, end_time=source.period*periods)

# Formatting results
v_source = numpy.array(analysis.nodes['source'])
v_gate = numpy.array(analysis.nodes['gate'])
v_output = numpy.array(analysis.nodes['output'])
i_load = numpy.array(analysis.branches['l1'])

#Voltages
ax1.set_title('Half-Wave Rectification - Voltage')
ax1.set_xlabel('Time [ms]')
ax1.set_ylabel('Voltage [V]')
ax1.grid()
ax1.plot(v_source)
ax1.plot(v_gate)
ax1.plot(v_output)
ax1.legend(('source', 'gate', 'output'), loc=(.05,.1))
ax1.set_ylim(float(-source.amplitude*1.1), float(source.amplitude*1.1))

# Current
max_current = i_load.max()
min_current = i_load.min()

ax2.set_title('Half-Wave Rectification - Current')
ax2.set_xlabel('Time [ms]')
ax2.set_ylabel('Current [A]')
ax2.grid()
ax2.plot(i_load)
ax2.legend('l1', loc=(.05,.1))
ax2.set_ylim(float(1.1 * min_current), float(1.1 * max_current))

####################################################################################################
# CIRCUIT DEFINITION - FILTERED
####################################################################################################

# We add a capacitor to filter the output voltage
circuit.C('1', 'output', circuit.gnd, 10@u_mF)

# Show the netlist
print('**** Circuit netlist (with filter): ****')
print(circuit)

####################################################################################################
# SIMULATION
####################################################################################################

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
simulator.save_currents = True
analysis = simulator.transient(step_time=source.period/1000, end_time=source.period*periods)

# Formatting results
v_source = numpy.array(analysis.nodes['source'])
v_gate = numpy.array(analysis.nodes['gate'])
v_output = numpy.array(analysis.nodes['output'])
i_load = numpy.array(analysis.branches['l1'])

# Voltages
ax3.set_title('Half-Wave Rectification with filtering')
ax3.set_xlabel('Time [ms]')
ax3.set_ylabel('Voltage [V]')
ax3.grid()
ax3.plot(v_source)
ax3.plot(v_gate)
ax3.plot(v_output)
ax3.legend(('source', 'gate', 'output'), loc=(.05,.1))
ax3.set_ylim(float(-source.amplitude*1.1), float(source.amplitude*1.1))

# Current
max_current = i_load.max()
min_current = i_load.min()

ax4.set_title('Half-Wave Rectification with filtering - Current')
ax4.set_xlabel('Time [ms]')
ax4.set_ylabel('Current [A]')
ax4.grid()
ax4.plot(i_load)
ax4.legend('l1', loc=(.05,.1))
ax4.set_ylim(float(1.1 * min_current), float(1.1 * max_current))

plt.show()

####################################################################################################