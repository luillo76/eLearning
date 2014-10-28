import pandas as pd
import numpy as np

from prediction import predictions


def compute_r_squared(data, predictions):
    # Write a function that, given two input numpy arrays, 'data', and 'predictions,'
    # returns the coefficient of determination, R^2, for the model that produced 
    # predictions.
    # 
    # Numpy has a couple of functions -- np.mean() and np.sum() --
    # that you might find useful, but you don't have to use them.

    # YOUR CODE GOES HERE
    mean = np.mean(data)
    r_squared = 1.0 - np.sum( (data-predictions)**2)/np.sum( (data-mean)**2 ) 

    return r_squared


if __name__ == "__main__":
    input_filename = "../turnstile_data_master_with_weather.csv"
    turnstile_master = pd.read_csv(input_filename)
    predicted_values = predictions(turnstile_master)
    r_squared = compute_r_squared(turnstile_master['ENTRIESn_hourly'], predicted_values)
    print r_squared