import time
import pandas as pd
from datetime import datetime
from models.simulation_app import AppSimulation

def run_simulation(data_dict):
    ACUITIES = ['Major', 'Minor', 'Resus']
    LENGTH_OF_STAY = {}
    ARRIVALS_BEFORE_9 = {}
    ARRIVALS_AFTER_9 = {}
    NUM_BEDS = {}
    for acuity, dic in zip(ACUITIES, data_dict[4:]):
        LENGTH_OF_STAY[acuity] = dic['length_of_stay']
        ARRIVALS_BEFORE_9[acuity] = dic['arrivals_before_9']
        ARRIVALS_AFTER_9[acuity] = dic['arrivals_after_9']
        NUM_BEDS[acuity] = dic['number_of_available_beds']
    SIMULATION_DURATION = data_dict[0]['value'] * 24  # Total simulation time in hours
    MIN_PATIENCE_MINOR = data_dict[1]['value']
    MAX_PATIENCE_MINOR = data_dict[2]['value']
    start_datetime = datetime.strptime(data_dict[3]['value'], "%Y-%m-%d")
    simulation = AppSimulation(
    LENGTH_OF_STAY,
    ARRIVALS_BEFORE_9,
    ARRIVALS_AFTER_9,
    SIMULATION_DURATION,
    MIN_PATIENCE_MINOR,
    MAX_PATIENCE_MINOR,
    start_datetime = start_datetime
    )
    patient_data = simulation.run_simulation(NUM_BEDS)
    output = simulation.prepare_output_dict()
    return output