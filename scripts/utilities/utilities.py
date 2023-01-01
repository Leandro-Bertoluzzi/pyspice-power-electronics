import numpy as np
import os

'''
- Name: format_output
- Parameter(s):
    - analysis: SPICE simulation result
    - simulation_mode: Type of simulation (operating_pint, transient, ac)
- Description:
    Receives a raw SPICE simulation result and creates a dictionary with a key/value pair for each node
'''

def format_output(analysis, simulation_mode):
    voltages = {}
    currents ={}

    # Loop through nodes
    for node in analysis.nodes.values():
        data_label = str(node)  # Extract node name
        if simulation_mode == 'operating_point':
            voltages[data_label] = float(node)
        elif simulation_mode == 'ac':
            voltages[data_label] = {}
            voltages[data_label]['magnitude'] = np.abs(node)
            voltages[data_label]['phase'] = np.angle(node)
        else:
            voltages[data_label] = np.array(node)
    
    # Loop through branches
    for branch in analysis.branches.values():
        data_label = str(branch)  # Extract node name
        if simulation_mode == 'operating_point':
            currents[data_label] = float(branch)
        elif simulation_mode == 'ac':
            currents[data_label] = {}
            currents[data_label]['magnitude'] = np.abs(branch)
            currents[data_label]['phase'] = np.angle(branch)
        else:
            currents[data_label] = np.array(branch)
    
    # If the simulation mode is "transient",  we also return time
    if simulation_mode == 'transient':
        t = []
        for val in analysis.time:
            t.append(val)
        voltages['time'] = np.array(t)
        currents['time'] = np.array(t)
    
    # If the simulation mode is "ac",  we also return frequency
    if simulation_mode == 'ac':
        f = []
        for val in analysis.frequency:
            f.append(val)
        voltages['frequency'] = np.array(f)
        currents['frequency'] = np.array(f)
    
    return voltages, currents

'''
- Name: get_output_file_name
- Parameter(s):
    - file_name: string
- Description:
    Generates the absolute path to save the output file in the "results" folder
'''

def get_output_file_name(file_name):
    my_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/results"

    if not os.path.isdir(my_path):
        os.makedirs(my_path)

    return os.path.join(my_path, file_name)