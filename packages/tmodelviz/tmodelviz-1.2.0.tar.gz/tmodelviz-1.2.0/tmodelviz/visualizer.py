# visualizer.py

import matplotlib.pyplot as plt
from ipywidgets import FloatSlider, Play, jslink, interact, HBox
from IPython.display import display
from .utils import calculate_rolling_average, extract_fluxes
from .simulator import load_and_simulate

def plotviz(model_input: str, start_time=0, end_time=10, steps=101):
    """
    Creates an interactive visualization for species concentrations, concentration changes, rolling averages, and fluxes.
    
    Parameters:
    model_input (str): The model input for the simulation.
    start_time (int): The start time for the simulation.
    end_time (int): The end time for the simulation.
    steps (int): The number of steps for the simulation.
    """
    # Load and simulate the model
    runner, data = load_and_simulate(model_input, start_time, end_time, steps)
    time = data[:, 0]
    species_names = runner.getFloatingSpeciesIds()
    species_concentrations = data[:, 1:]
    prev_timestep = [0]

    # Precompute global ranges for plotting
    max_concentration_change = max(abs(species_concentrations.max() - species_concentrations.min()), 1)
    max_flux = max(abs(runner.getReactionRates().max()), 1)  # Simulate once to get max flux

    def plot_bars(timestep):
        """
        Plots the species concentrations, concentration changes, rolling averages, and fluxes at a given timestep.
        
        Parameters:
        timestep (float): The current time point for the visualization.
        """
        plt.figure(figsize=(12, 8))

        # Find the indices for the current and previous timesteps
        current_index = (abs(time - timestep)).argmin()
        previous_index = (abs(time - prev_timestep[0])).argmin()

        # Get the current and previous concentrations
        current_concentrations = species_concentrations[current_index]
        previous_concentrations = species_concentrations[previous_index]

        # Calculate the differences in concentrations
        differences = (
            current_concentrations - previous_concentrations
            if timestep > prev_timestep[0]
            else previous_concentrations - current_concentrations
        )
        # Calculate the rolling average
        rolling_average = calculate_rolling_average(
            species_concentrations, time, current_index, window_size=10
        )
        # Extract the fluxes and reaction names
        fluxes, reaction_names = extract_fluxes(
            runner, species_names, species_concentrations, current_index
        )
        
        # Update the previous timestep
        prev_timestep[0] = timestep

        # Plot species concentrations
        plt.subplot(2, 2, 1)
        plt.bar(species_names, current_concentrations, color="skyblue")
        plt.title(f"Species Concentrations at Time = {timestep:.2f}s")
        plt.ylabel("Concentration")
        plt.ylim(0, max(species_concentrations.max(), 1))   
        plt.xticks(rotation=45)

        # Plot concentration differences
        plt.subplot(2, 2, 2)
        plt.bar(species_names, differences, color="lightcoral")
        plt.title("Concentration Changes")
        plt.ylabel("Difference")
        plt.ylim(-max_concentration_change, max_concentration_change)
        plt.xticks(rotation=45)

        # Plot rolling averages
        plt.subplot(2, 2, 3)
        plt.bar(species_names, rolling_average, color="mediumseagreen")
        plt.title("Rolling Average")
        plt.ylabel("Average")
        plt.ylim(0, max(species_concentrations.max(), 1))
        plt.xticks(rotation=45)

        # Plot reaction fluxes
        plt.subplot(2, 2, 4)
        plt.bar(reaction_names, fluxes, color="gold", alpha=0.7)
        plt.title("Reaction Fluxes")
        plt.ylabel("Flux")
        plt.ylim(0, max_flux)
        plt.xticks(rotation=45)

        # Adjust layout to prevent overlap
        plt.tight_layout()
        plt.show()

    # Create interactive visualization with slider and play button
    slider = FloatSlider(min=start_time, max=end_time, step=(end_time - start_time) / steps, description="Time (s)")
    play = Play(value=0, min=start_time, max=end_time, step=1, interval=250)
    jslink((play, "value"), (slider, "value"))

    # Link the slider to the plot_bars function
    interact(plot_bars, timestep=slider)
    # Display the play button and slider
    display(HBox([play]))