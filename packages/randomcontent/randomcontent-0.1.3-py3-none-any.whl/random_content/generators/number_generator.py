# randomcontent/generators/number_generator.py

import random

def generate_number(type="int", min=0, max=100):
    if type == "int":
        return random.randint(min, max)  # Use min/max here
    elif type == "float":
        return random.uniform(min, max)  # Use min/max here
    else:
        raise ValueError("Invalid type. Use 'int' or 'float'.")
