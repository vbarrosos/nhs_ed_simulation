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
import numpy as np
import pandas as pd
import simpy
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random
from tqdm import tqdm
import json
import os

class EDSimulation:
    """
    Base class for simulation of Emergency Department resources.
    =================
    """
    acuities = ["Major", "Minor", "Resus"]
    start_datetime = datetime(2024,1,1,0,0)
    RANDOM_SEED = 42
    def __init__(self, LENGTH_OF_STAY, ARRIVALS_BEFORE_9, ARRIVALS_AFTER_9, SIMULATION_DURATION, MIN_PATIENCE_MINOR, MAX_PATIENCE_MINOR, **kwargs):
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
        self.__dict__.update(**kwargs)
        self.LENGTH_OF_STAY = LENGTH_OF_STAY
        self.ARRIVALS_BEFORE_9  = ARRIVALS_BEFORE_9 
        self.ARRIVALS_AFTER_9 = ARRIVALS_AFTER_9
        self.SIMULATION_DURATION = SIMULATION_DURATION
        self.MIN_PATIENCE_MINOR = MIN_PATIENCE_MINOR
        self.MAX_PATIENCE_MINOR = MAX_PATIENCE_MINOR
        # set a seeded random generator, for consistency
        self.rng = np.random.default_rng(self.RANDOM_SEED)
        
    def reset_variables(self):
        """
        Reset the variables for the simulation.
        """
        # Initialise data structures for tracking patient counts, occupancy, and queue lengths
        self.patient_count = {acuity: np.zeros(self.SIMULATION_DURATION) for acuity in self.acuities}
        self.bed_usage = {acuity: np.zeros(self.SIMULATION_DURATION) for acuity in self.acuities}
        self.queue_lengths = {acuity: np.zeros(self.SIMULATION_DURATION) for acuity in self.acuities}
        self.total_occupancy = {acuity: np.zeros(self.SIMULATION_DURATION) for acuity in self.acuities}
        # Initialise preset storage for patient data (arrival, stay and wait time) and patient ID
        self.patient_data = []
        self.patient_id = 0
        # reset total beds
        self.total_beds = 0
        
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
        
    def patient_arrival(self, env, resources):
        """
        Generate patients from Poisson distributions following historical averages for each acuity level,
        and track the patients' length of stay.
        ===========
        ARGUMENTS:
        ===========
        - env: simpy.Environment
            Simulation environment.
        - resources: dict
            Resources for each acuity level, where keys are acuities and values are simpy.Resource objects.
        ============
        """
        patient_id = 0
        while True:
            current_hour = env.now % 24
            if current_hour <= 9:
                patients_per_acuities = {acuity: self.rng.poisson(self.ARRIVALS_BEFORE_9[acuity],size=1) for acuity in self.acuities}
            else:
                patients_per_acuities = {acuity: self.rng.poisson(self.ARRIVALS_AFTER_9[acuity],size=1) for acuity in self.acuities}
                
            for acuity, num_patients in patients_per_acuities.items():
                for _ in np.arange(0,num_patients):
                    stay_duration = self.rng.poisson(self.LENGTH_OF_STAY[acuity], size=1)
                    patient_id += 1
                    env.process(self.track_patient(env, patient_id, acuity, stay_duration, resources[acuity]))
            yield env.timeout(1)
            
    def track_patient(self, env, patient_id, acuity, stay_duration, resource):
        """
        Tracks the patient's arrival, wait time, length of stay and departure.
        ===========
        ARGUMENTS:
        ===========
        - env: simpy.Environment
            Simulation environment.
        - patient_id: int
            ID of the patient.
        - acuity: str
            Acuity level of the patient.
        - stay_duration: int
            Length of stay of the patient.
        - resource: simpy.Resource
            Resource for the patient.
        ============
        """
        arrival_time = int(env.now)
        self.patient_count[acuity][arrival_time] += 1
        self.total_occupancy[acuity][arrival_time] += 1
        
        if acuity == "Minor":
            reneging_time = self.rng.uniform(self.MIN_PATIENCE_MINOR, self.MAX_PATIENCE_MINOR, size=1)
            with resource.request() as req:
                result = yield req | env.timeout(reneging_time)
                if req in result:
                    bed_assigned_time = int(env.now)
                    wait_time = bed_assigned_time - arrival_time
                    self.update_patient_data(patient_id, acuity, arrival_time, wait_time)
                    yield env.timeout(stay_duration)
                    end_time = int(env.now)
                    self.patient_count[acuity][end_time] -= 1
                else:
                    renege_time = int(env.now)
                    wait_time = renege_time - arrival_time
                    self.update_patient_data(patient_id, acuity, arrival_time, wait_time)
                    self.patient_count[acuity][renege_time] -= 1
        else:
            with resource.request() as req:
                yield req
                bed_assigned_time = int(env.now)
                wait_time = bed_assigned_time - arrival_time
                self.update_patient_data(patient_id, acuity, arrival_time, wait_time)
                yield env.timeout(stay_duration)
                end_time = int(env.now)
                self.patient_count[acuity][end_time] -= 1
        
    def update_patient_data(self, patient_id, acuity, arrival_time, wait_time):
        """
        Update the patient data with the patient's ID, acuity, arrival time and wait time.
        ===========
        ARGUMENTS:
        ===========
        - acuity: str
            Acuity level of the patient.
        - patient_id: int
            ID of the patient.
        - arrival_time: int
            Arrival time of the patient.
        - wait_time: int
            Wait time of the patient.
        ============
        """
        # print(f"Saving data of patient {patient_id}.", end="\r", flush=True)
        self.patient_data.append({"Id":patient_id, 
                                  "Acuity":acuity, 
                                  "Arrival_Time":arrival_time, 
                                  "Wait_Time":wait_time
                                  })
        
    def collect_data(self, env, resources):
        """
        Collect data for tracking patient counts, occupancy, and queue lengths.
        ===========
        ARGUMENTS:
        ===========
        - env: simpy.Environment
            Simulation environment.
        - resources: dict
            Resources for each acuity level.
        ============
        """
        while True:
            for acuity in self.acuities:
                self.bed_usage[acuity][int(env.now)] = resources[acuity].count
                self.queue_lengths[acuity][int(env.now)] = len(resources[acuity].queue)
            yield env.timeout(1)
    
    @staticmethod 
    def calculate_average_wait_time(patient_data):
        """
        Calculate the average wait time for each acuity level.
        ===========
        ARGUMENTS:
        ===========
        - patient_data: pandas.DataFrame
            Patient data with ID, acuity, arrival time and wait time.
        ============
        RETURNS:
        ============
        - average_wait_time: dict
            Average wait time for each acuity level.
        ============
        """
        df = pd.DataFrame(patient_data)
        df["Hour"] = df["Arrival_Time"]
        average_wait_time = df.groupby(["Hour","Acuity"])["Wait_Time"].mean().unstack().fillna(0)
        return average_wait_time

    @staticmethod
    def calculate_wait_time_percentiles(average_wait_time, quantiles=np.arange(0.25,1.,0.25)):
        """
        Calculate the 25th, 50th and 75th percentiles of wait time for each acuity level.
        ===========
        ARGUMENTS:
        ===========
        - average_wait_time: dict
            Average wait time for each acuity level.
        ============
        OPTIONAL:
        ============
        - quantiles: float or list
            Single value or list of quantiles (between 0 and 1) to calculate. Default is [0.25,0.5,0.75].
        ============
        RETURNS:
        ============
        - percentiles: dict
            percentiles (corresponding to given quantiles) of wait time for each acuity level.
        ============
        """
        acuities = average_wait_time.columns
        percentiles = {acuity: average_wait_time[acuity].quantile(quantiles).to_dict() for acuity in acuities}
        return percentiles
    
    def plot_results(self, acuity_colors=['firebrick','olivedrab','navy'], row_size=3, aspect_ratio=1.5):
        """
        Plot the results of the simulation.
        ============
        OPTIONAL:
        ============
        - acuity_colors: list
            Colors for each acuity level. Default is ['red','green','blue'].
        - row_size: float
            Size of each row in the plot (in inches). Default is 3.
        - aspect_ratio: float
            Aspect ratio of the plot. Default is 1.5
        ============
        """
        x = [(self.start_datetime+timedelta(hours=i)) for i in range(self.SIMULATION_DURATION)]
        x_ticks = [x[i]  for i in range(0,len(x),24)]
        x_labels = [x[i].strftime("%Y-%m-%d")  for i in range(0,len(x),24)]
        average_wait_time = self.calculate_average_wait_time(self.patient_data)
        
        # set legend keyword arguments
        legend_kws = dict(loc='lower left', 
                          bbox_to_anchor=(0, 1.), 
                          ncol=3, 
                          fontsize=10,
                          title="Acuity level")
        
        fig = plt.figure(figsize=(aspect_ratio*4*row_size, 4*row_size), dpi=300)
        # Plot occupancy over time for each acuity
        ax = fig.add_subplot(4, 1, 1)
        for acuity, color in zip(self.acuities, acuity_colors):
            ax.plot(x, self.bed_usage[acuity], label=f'{acuity}', color=color)
        ax.set_xlabel("Time (Date)")
        ax.set_ylabel("Beds Occupied")
        ax.set_title(f"Beds Occupied over Time (Total Beds = {self.total_beds})")
        ax.set_xticks(x_ticks, x_labels, rotation=45, ha='right')
        ax.grid(True)
        ax.legend(**legend_kws)

        # Plot queue length over time for each acuity
        ax = fig.add_subplot(4, 1, 2)
        for acuity, color in zip(self.acuities, acuity_colors):
            ax.plot(x, self.queue_lengths[acuity], label=f'{acuity}', color=color)
        ax.set_xlabel("Time (date)")
        ax.set_ylabel("Queue Length")
        ax.set_title("Queue Length over Time")
        ax.set_xticks(x_ticks, x_labels, rotation=45, ha='right')
        ax.grid(True)
        ax.legend(**legend_kws)

        # Plot total bed usage over time for each acuity
        ax = fig.add_subplot(4, 1, 3)
        for acuity, color in zip(self.acuities, acuity_colors):
            ax.plot(x, self.total_occupancy[acuity], label=f'{acuity}', color=color)
        ax.set_xlabel("Time (date)")
        ax.set_ylabel("Beds requested")
        ax.set_title("Bed Usage over Time")
        ax.set_xticks(x_ticks, x_labels, rotation=45, ha='right')
        ax.grid(True)
        ax.legend(**legend_kws)
        
        # Plot average wait time for each acuity
        ax = fig.add_subplot(4, 1, 4)
        for acuity, color in zip(average_wait_time.columns, acuity_colors):
            ax.plot(x[:len(average_wait_time)], average_wait_time[acuity], label = f'{acuity}', color=color)
        ax.set_xlabel("Time (date)")
        ax.set_ylabel('Average wait time')
        ax.set_title("Average wait time over Time")
        ax.set_xticks(x_ticks, x_labels, rotation=45, ha='right')
        ax.grid(True)
        ax.legend(**legend_kws)
        
        plt.tight_layout()
        plt.show()
            
    def save_patient_data(self, filepath, file_format=".csv", meta_format=".txt"):
        """ 
        Save the patient data to a CSV file and the simulation metadata to a txt or json file.
        ============
        ARGUMENTS:
        ============
        - filepath: str
             File path to save the patient data.
        ============
        OPTIONAL: 
        ============
        - file_format: str
            File format to save the patient data. Default is ".csv".
        - meta_format: str
            File format to save the metadata. Default is ".txt".
        ============
        """
        outname, extension = os.path.splitext(filepath)
        if extension != file_format:
            filepath = os.path.join(outname,file_format)
        # Save metadata to json file
        metafile = outname+"_metadata"+meta_format
        metadata = {"start_datetime":self.start_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    "RANDOM_SEED":self.RANDOM_SEED,
                    "LENGTH_OF_STAY":self.LENGTH_OF_STAY,
                    "ARRIVALS_BEFORE_9":self.ARRIVALS_BEFORE_9,
                    "ARRIVALS_AFTER_9":self.ARRIVALS_AFTER_9,
                    "SIMULATION_DURATION":self.SIMULATION_DURATION,
                    "MIN_PATIENCE_MINOR":self.MIN_PATIENCE_MINOR,
                    "MAX_PATIENCE_MINOR":self.MAX_PATIENCE_MINOR,
                    "NUM_BEDS":self.NUM_BEDS,
                    "total_beds":self.total_beds,
                    }
        with open(metafile, 'w') as f:
            json.dump(metadata, f, ensure_ascii=True, indent=4)
        # Save patient data to csv file
        df = pd.DataFrame(self.patient_data)
        df.to_csv(filepath, index=False, sep="\t")
        print(f"Patient data saved to:\n{filepath}")