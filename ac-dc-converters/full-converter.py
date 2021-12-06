#r# ============================================
#r#  Full converter with SCR
#r# ============================================

#r# This example shows the simulation of a controlled full converter with SCRs

######################################### IMPORT MODULES #########################################

import matplotlib.pyplot as plt
import numpy as np

######################################### IMPORT UTILITIES #########################################

import sys
sys.path.insert(1, '../utilities/')
from utilities import format_output

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

#####################################################################################################
# DEFINING PLOTS
#####################################################################################################

figure1, (ax1, ax2) = plt.subplots(2, 1, figsize=(20, 10))
figure2, (ax3, ax4) = plt.subplots(2, 1, figsize=(20, 10))

####################################################################################################
# CIRCUIT DEFINITION
####################################################################################################

circuit = Circuit('Full converter with SCR')

# Input voltage
source = circuit.SinusoidalVoltageSource('input', 'A', 'B', amplitude=220@u_V, frequency=50@u_Hz)
# SCR gate triggering signal
alpha = 0.3 # trigger angle [0; 1]
delay_time1 = (source.period/2) * alpha
pulse_width = (source.period/2) * (1- alpha)
circuit.PulseVoltageSource('trigger1', 'gate1', 'output', 0@u_V, 1@u_V, delay_time=delay_time1, pulse_width=pulse_width, period=source.period, rise_time=1@u_ms, fall_time=1@u_ms)
circuit.PulseVoltageSource('trigger2', 'gate2', 'B', 0@u_V, 1@u_V, delay_time=delay_time1, pulse_width=pulse_width, period=source.period, rise_time=1@u_ms, fall_time=1@u_ms)

delay_time2 = (source.period/2) * alpha + source.period/2
circuit.PulseVoltageSource('trigger3', 'gate3', 'output', 0@u_V, 1@u_V, delay_time=delay_time2, pulse_width=pulse_width, period=source.period, rise_time=1@u_ms, fall_time=1@u_ms)
circuit.PulseVoltageSource('trigger4', 'gate4', 'A', 0@u_V, 1@u_V, delay_time=delay_time2, pulse_width=pulse_width, period=source.period, rise_time=1@u_ms, fall_time=1@u_ms)

# Define the rectifier bridge
circuit.include(spice_library['EC103D1'])
circuit.X('t1', 'EC103D1', 'A', 'gate1', 'output')
circuit.X('t2', 'EC103D1', circuit.gnd, 'gate2', 'B')
circuit.X('t3', 'EC103D1', 'B', 'gate3', 'output')
circuit.X('t4', 'EC103D1', circuit.gnd, 'gate4', 'A')

# Series resistor as load
circuit.R('load', 'output', circuit.gnd, 100@u_Ω)

# Show the netlist
print('**** Circuit netlist: ****')
print(circuit)

####################################################################################################
# SIMULATION
####################################################################################################

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=source.period/5000, end_time=source.period*6)

# Formatting results
voltages, currents = format_output(analysis, 'transient')
v_source = np.subtract(voltages['a'], voltages['b'])
v_gate1 = voltages['gate1']
v_gate2 = voltages['gate2']
v_output = voltages['output']
t = voltages['time']

# Plot
ax1.set_title('Full converter with resistive load')
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Voltage [V]')
ax1.grid()
ax1.plot(t, v_source)
ax1.plot(t, v_gate1)
ax1.plot(t, v_gate2)
ax1.plot(t, v_output)
ax1.legend(('input', 'gate1', 'gate2', 'output'), loc=(.05,.1))
ax1.set_ylim(float(-source.amplitude*1.1), float(source.amplitude*1.1))

####################################################################################################
# CIRCUIT DEFINITION - FILTERED
####################################################################################################

# We add a capacitor to filter the output voltage
circuit.C('1', 'output', circuit.gnd, 1@u_mF)

# Show the netlist
print('**** Circuit netlist (with filter): ****')
print(circuit)

####################################################################################################
# SIMULATION
####################################################################################################

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=source.period/200, end_time=source.period*6)

# Formatting results
voltages, currents = format_output(analysis, 'transient')
v_source = np.subtract(voltages['a'], voltages['b'])
v_gate1 = voltages['gate1']
v_gate2 = voltages['gate2']
v_output = voltages['output']
t = voltages['time']

# Plot
ax2.set_title('Full converter with resistive load -- Filtered')
ax2.set_xlabel('Time [s]')
ax2.set_ylabel('Voltage [V]')
ax2.grid()
ax2.plot(t, v_source)
ax2.plot(t, v_gate1)
ax2.plot(t, v_gate2)
ax2.plot(t, v_output)
ax2.legend(('input', 'gate1', 'gate2', 'output'), loc=(.05,.1))
ax2.set_ylim(float(-source.amplitude*1.1), float(source.amplitude*1.1))

####################################################################################################
# CIRCUIT DEFINITION - RL LOAD
####################################################################################################

# We remove the filter capacitor and the resistive load
circuit.C1.detach()
circuit.Rload.detach()
# We add the RL load
circuit.R('_load', 'output', 'RL', 0.5@u_Ω)
circuit.L('_load', 'RL', circuit.gnd, 10@u_mH)

# Show the netlist
print('**** Circuit netlist (with RL load): ****')
print(circuit)

####################################################################################################
# SIMULATION
####################################################################################################

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=source.period/5000, end_time=source.period*6)

# Formatting results
voltages, currents = format_output(analysis, 'transient')
v_source = np.subtract(voltages['a'], voltages['b'])
v_gate1 = voltages['gate1']
v_gate2 = voltages['gate2']
v_output = voltages['output']
t = voltages['time']
i_load = currents['l_load']

# Voltages
ax3.set_title('Full converter with RL load')
ax3.set_xlabel('Time [s]')
ax3.set_ylabel('Voltage [V]')
ax3.grid()
ax3.plot(t, v_source)
ax3.plot(t, v_gate1)
ax3.plot(t, v_gate2)
ax3.plot(t, v_output)
ax3.legend(('input', 'gate1', 'gate2', 'output'), loc=(.05,.1))
ax3.set_ylim(float(-source.amplitude*1.1), float(source.amplitude*1.1))

# Current
max_current = i_load.max()
min_current = i_load.min()

ax4.set_title('Full converter with RL load - Current')
ax4.set_xlabel('Time [s]')
ax4.set_ylabel('Current [A]')
ax4.grid()
ax4.plot(t, i_load)
ax4.legend('Load current', loc=(.05,.1))
ax4.set_ylim(float(1.1 * min_current), float(1.1 * max_current))

####################################################################################################

# Adjusts the spacing between subplots
figure1.tight_layout(pad=3.0)
figure2.tight_layout(pad=3.0)
# Shows all plots
plt.show()