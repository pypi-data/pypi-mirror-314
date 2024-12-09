import numpy as np

def convert_to_stationary(target_variable):
    data_log = np.log(target_variable)
    stationary_data = data_log.diff().dropna()
    return stationary_data