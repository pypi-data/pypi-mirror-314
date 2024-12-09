import json
import csv
import pandas as pd  # For handling Parquet files
from randomcontent.utils.data_utils import generate_name, generate_email
from randomcontent.generators.number_generator import generate_number


def parse_params(params_str):
    """
    Convert a string like 'min=18, max=60' to a dictionary {'min': 18, 'max': 60}.
    """
    params = {}
    param_pairs = params_str.split(",")
    for pair in param_pairs:
        pair = pair.strip()
        if "=" in pair:
            key, value = pair.split("=", 1)
            params[key.strip()] = eval(value.strip())  # Safe eval usage for literals
        else:
            print(f"Warning: Skipping malformed parameter: {pair}")
    return params


def generate_structured_data(schema, count=1):
    """
    Generates mock data based on the provided schema.
    
    Parameters:
        schema (dict): A dictionary defining the data generation rules for each field.
        count (int): Number of rows of data to generate.
        
    Returns:
        list: A list of dictionaries containing generated data.
    """
    data = []
    for _ in range(count):
        row = {}
        for field, rule in schema.items():
            if rule == "random_name":
                row[field] = generate_name()
            elif rule == "random_email":
                row[field] = generate_email()
            elif rule.startswith("random_int"):
                params_str = rule.split("(")[1].rstrip(")")
                params = parse_params(params_str)
                row[field] = generate_number(type="int", **params)
            else:
                row[field] = None
        data.append(row)
    return data


def format_data(data, format_type="json", file_name="data"):
    """
    Formats the generated data into the specified format.
    
    Parameters:
        data (list): The generated data as a list of dictionaries.
        format_type (str): The desired format ('json', 'csv', 'parquet').
        file_name (str): Name of the output file (without extension).
        
    Returns:
        str: The file path of the formatted data.
    """
    file_path = f"{file_name}.{format_type}"
    
    if format_type == "json":
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
    
    elif format_type == "csv":
        with open(file_path, "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    
    elif format_type == "parquet":
        df = pd.DataFrame(data)
        df.to_parquet(file_path, engine="pyarrow", index=False)
    
    else:
        raise ValueError(f"Unsupported format: {format_type}")
    
    print(f"Data successfully saved as {file_path}")
    return file_path



