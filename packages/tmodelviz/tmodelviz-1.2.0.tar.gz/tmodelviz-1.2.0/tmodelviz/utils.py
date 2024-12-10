# utils.py

import numpy as np

def calculate_rolling_average(concentrations, time, index, window_size):
    """
    Calculates the rolling average for species concentrations.
    
    Parameters:
    concentrations (np.array): Array of species concentrations.
    time (np.array): Array of time points.
    index (int): The index at which to calculate the rolling average.
    window_size (int): The size of the window over which to calculate the average.
    
    Returns:
    float: The rolling average of the concentrations within the window.
    """
    # Determine the start and end indices for the window
    start = max(0, index - window_size // 2)
    end = min(len(time), index + window_size // 2 + 1)
    # Calculate and return the mean concentration within the window
    return np.mean(concentrations[start:end], axis=0)

def extract_fluxes(runner, species_names, species_concentrations, index):
    """
    Extracts reaction fluxes by resetting the runner state to match the species concentrations.
    
    Parameters:
    runner (object): The simulation runner object.
    species_names (list): List of species names.
    species_concentrations (np.array): Array of species concentrations.
    index (int): The index at which to extract the fluxes.
    
    Returns:
    tuple: A tuple containing the reaction rates and reaction IDs.
    """
    # Reset the runner to its initial state
    runner.reset()
    # Set the runner's species concentrations to the values at the given index
    for species, conc in zip(species_names, species_concentrations[index]):
        runner[species] = conc
    # Return the reaction rates and reaction IDs from the runner
    return runner.getReactionRates(), runner.getReactionIds()