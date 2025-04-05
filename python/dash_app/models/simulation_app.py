#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
Created on 08 Mar 2025
@Author  :   Vitor Barroso
@Version :   1.0
@Contact :   vitor.barroso.s@gmail.com
@License :   (C)Copyright 2025, Vitor Barroso
@Desc    :   Base class for simulation of Emergency Department resources
                using SimPy and prophet.
'''
import sys
import os
sys.path.append(os.path.abspath("./"))
from python.simulation_base import EDSimulation
import numpy as np
import pandas as pd
import simpy
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random
from tqdm import tqdm
import json

class AppSimulation(EDSimulation):
    """
    Base class for simulation of Emergency Department resources.
    =================
    """
    acuities = ["Major", "Minor", "Resus"]
    start_datetime = datetime(2024,1,1,0,0)
    RANDOM_SEED = 42
    def __init__(self, *args, **kwargs):
        """
        Initialize the simulation.
        ===========
        ARGUMENTS:
        ===========
        - LENGTH_OF_STAY: dict
            Average length of stay for each acuity level.
        - ARRIVALS_BEFORE_9: dict
            Average number of arrivals before 9am for each acuity level.
        - ARRIVALS_AFTER_9: dict
            Average number of arrivals after 9am for each acuity level.
        - SIMULATION_DURATION: int
            The duration of the simulation in hours.
        - MIN_PATIENCE_MINOR: int
            Minimum patience of minor acuity patients.
        - MAX_PATIENCE_MINOR: int
            Maximum patience of minor acuity patients.
        ============
        OPTIONAL:
        ============
        - acuities: list
            Acuity levels of patients. Default is ["Major", "Minor", "Resus"].
        - start_datetime: datetime
            Start datetime of the simulation. Default is datetime(2024,1,1,0,0).
        - RANDOM_SEED: int
            Random seed for the simulation. Default is 42.
        ============   
        """
        super().__init__(*args,**kwargs)
        
    def run_simulation(self, NUM_BEDS):
        """
        Prepare the simulation environment, create separate resources for each acuity and run simulation.
        ===========
        ARGUMENTS:
        ===========
        - NUM_BEDS: dict
            Number of beds for each acuity level.
        ============
        RETURNS:
        ============
        - patient_count: dict
            Patient count for each acuity level.
        - patient_data: pd.DataFrame
            Patient data with ID, acuity, arrival time and wait time.
        ============
        """
        self.reset_variables()
        self.NUM_BEDS = NUM_BEDS
        
        random.seed(self.RANDOM_SEED)
        env = simpy.Environment()
        
        # Create data structure of resources for each acuity level
        resources = {acuity: simpy.Resource(env, capacity=beds) for acuity, beds 
                     in NUM_BEDS.items()}
        self.total_beds = sum(list(NUM_BEDS.values()))
        
        env.process(self.patient_arrival(env,resources))
        env.process(self.collect_data(env, resources))
        [env.run(until=i) for i in tqdm(range(1,self.SIMULATION_DURATION), desc="Running Simulation")]
        
        return pd.DataFrame(self.patient_data)
        
    def prepare_output_dict(self,):
        """
        Prepare output dictionary with simulation data.
        ============
        RETURNS:
        ============
        - output_dict: dict
            Dictionary with simulation data processed for plotting.
        ============
        """
        x = [(self.start_datetime+timedelta(hours=i)) for i in range(self.SIMULATION_DURATION)]
        average_wait_time = self.calculate_average_wait_time(self.patient_data)
        average_wait_time = {k:list(v) for k,v in average_wait_time.items()}
        len_dif = {acuity:len(average_wait_time[acuity])-len(x) for acuity in self.acuities}
        for acuity,lds in len_dif.items():
            if lds!=0:
                average_wait_time[acuity] += abs(lds)*[None]
        DATA = {'Bed Usage':self.bed_usage, 
                'Queue Lengths':self.queue_lengths, 
                'Total Occupancy':self.total_occupancy, 
                'Average Wait Time':average_wait_time}
        output_dict = {key:[] for key in DATA.keys()}
        output_dict['Acuity'] = []
        output_dict['Time'] = []
        for acuity in self.acuities:
            for key,dset in DATA.items():
                output_dict[key] += list(dset[acuity])
            output_dict['Time'] += x
            output_dict["Acuity"] += len(x)*[acuity]
        return output_dict