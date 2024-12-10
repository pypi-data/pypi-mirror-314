# simulator.py

import tellurium as te

def load_and_simulate(model_input: str, start_time: float, end_time: float, steps: int):
    """
    Loads a model (from an SBML URL/path or an Antimony string) and simulates it.
    
    Args:
        model_input (str): URL/path to the SBML file or an Antimony string.
        start_time (float): Start time for the simulation.
        end_time (float): End time for the simulation.
        steps (int): Number of steps in the simulation.
    
    Returns:
        tuple: A tuple containing the runner object and simulation data.
    """
    # Check if input is a URL or file path
    if model_input.startswith("http") and model_input.endswith(".xml"):
        runner = te.loadSBMLModel(model_input)  # Load from URL
    else:
        runner = te.loada(model_input)  # Load from Antimony string

    data = runner.simulate(start_time, end_time, steps) #return simulation data
    return runner, data
