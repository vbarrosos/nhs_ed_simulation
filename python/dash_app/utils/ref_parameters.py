ACUITIES = ['Major', 'Minor', 'Resus']

SIMULATION_PARAMETERS_ACUITY = {
    "LENGTH OF STAY":{
        'Major':9,
        'Minor':4,
        'Resus':6,
    },
    "ARRIVALS BEFORE 9": {
        'Major':6,
        'Minor':4,
        'Resus':1,
    },
    "ARRIVALS AFTER 9":{
        'Major':16,
        'Minor':12,
        'Resus':2,
    },
    "NUMBER OF AVAILABLE BEDS": {
        'Major':110,
        'Minor':35,
        'Resus':16,
    },
}
SIMULATION_PARAMETERS = {
    "SIMULATION DURATION (DAYS)": 30,
    "MIN PATIENCE MINOR": 4,
    "MAX PATIENCE MINOR": 8,
}
