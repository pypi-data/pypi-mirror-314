from randomcontent.utils.data_utils import generate_name, generate_email
from randomcontent.generators.number_generator import generate_number

def parse_params(params_str):
    """
    Convert a string like 'min=18, max=60' to a dictionary {'min': 18, 'max': 60}
    Also handles potential empty or malformed parameters.
    """
    params = {}
    param_pairs = params_str.split(",")
    for pair in param_pairs:
        pair = pair.strip()
        if "=" in pair:  # Ensure it's a valid key-value pair
            key, value = pair.split("=", 1)  # Split only on the first '=' found
            # Strip spaces and use eval to ensure values are correctly interpreted as integers
            params[key.strip()] = eval(value.strip())
        else:
            print(f"Warning: Skipping malformed parameter: {pair}")
    return params



def generate_mock_data(schema, count=1):
    data = []
    for _ in range(count):
        row = {}
        for field, rule in schema.items():
            if rule == "random_name":
                row[field] = generate_name()
            elif rule == "random_email":
                row[field] = generate_email()
            elif rule.startswith("random_int"):
                # Parse the parameters to a dictionary
                params_str = rule.split("(")[1].rstrip(")")
                params = parse_params(params_str)  # Use the new parse_params function
                row[field] = generate_number(type="int", **params)  # Ensure params is a dictionary
            else:
                row[field] = None
        data.append(row)
    return data
