import numpy as np
import os

'''
- Name: format_output
- Parameter(s):
    - analysis: SPICE simulation result
    - simulation_mode: Type of simulation (operating_pint, transient, etc)
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
        else:
            voltages[data_label] = np.array(node)
    
    # Loop through branches
    for branch in analysis.branches.values():
        data_label = str(branch)  # Extract node name
        if simulation_mode == 'operating_point':
            currents[data_label] = float(node)
        else:
            currents[data_label] = np.array(branch)
    
    # If the simulation mode is "transient",  we also return time
    if simulation_mode == 'transient':
        t = []
        for val in analysis.time:
            t.append(val)
        voltages['time'] = np.array(t)
        currents['time'] = np.array(t)
    
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