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
# RECTIFICATION
####################################################################################################

figure1, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

####################################################################################################

circuit = Circuit('SCR half wave rectifier')

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
# Series resistor as load
circuit.R('load', 'output', circuit.gnd, 100@u_Ω)

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=source.period/200, end_time=source.period*2)

ax1.set_title('Half-Wave Rectification')
ax1.set_xlabel('Time [ms]')
ax1.set_ylabel('Voltage [V]')
ax1.grid()
ax1.plot(analysis['source'])
ax1.plot(analysis['gate'])
ax1.plot(analysis.output)
ax1.legend(('input', 'gate', 'output'), loc=(.05,.1))
ax1.set_ylim(float(-source.amplitude*1.1), float(source.amplitude*1.1))

####################################################################################################

# We add a capacitor to filter the output voltage
circuit.C('1', 'output', circuit.gnd, 1@u_mF)

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=source.period/200, end_time=source.period*2)

ax2.set_title('Half-Wave Rectification with filtering')
ax2.set_xlabel('Time [ms]')
ax2.set_ylabel('Voltage [V]')
ax2.grid()
ax2.plot(analysis['source'])
ax2.plot(analysis['gate'])
ax2.plot(analysis.output)
ax2.legend(('input', 'gate', 'output'), loc=(.05,.1))
ax2.set_ylim(float(-source.amplitude*1.1), float(source.amplitude*1.1))

plt.show()