# randomcontent/generators/number_generator.py

import random

def generate_number(type="int", min=0, max=100, mean=0, std_dev=1, step=1, options=None):
    """
    Generates a random number based on the specified type.
    
    Parameters:
        type (str): Type of number ('int', 'float', 'gaussian', 'choice', 'range', 'probability', etc.).
        min (int or float): Minimum value for number generation.
        max (int or float): Maximum value for number generation.
        mean (float): Mean for Gaussian distribution (used if type='gaussian').
        std_dev (float): Standard deviation for Gaussian distribution (used if type='gaussian').
        step (int): Step size for range (used if type='range').
        options (list): Custom list of values (used if type='choice').
        
    Returns:
        A random number based on the specified parameters.
    """
    if type == "int":
        return random.randint(min, max)
    
    elif type == "float":
        return random.uniform(min, max)
    
    elif type == "gaussian":
        # Generate a random number from Gaussian distribution
        return random.gauss(mean, std_dev)
    
    elif type == "choice":
        if options is None:
            raise ValueError("Options must be provided for type 'choice'.")
        return random.choice(options)
    
    elif type == "range":
        return random.randrange(min, max, step)
    
    elif type == "probability":
        # Generate a random number between 0 and 1
        return random.random()
    
    else:
        raise ValueError("Invalid type. Use 'int', 'float', 'gaussian', 'choice', 'range', or 'probability'.")
