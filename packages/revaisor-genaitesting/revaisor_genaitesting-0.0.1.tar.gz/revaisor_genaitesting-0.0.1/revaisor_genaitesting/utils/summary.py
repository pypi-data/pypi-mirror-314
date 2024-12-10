import pandas as pd
from typing import Dict

def simulation_summary(filepath: str):
    """
    Creates a summary of the simulation process from an Excel file.

    Args:
        filepath (str): The path to the Excel file that contains the simulation.

    Returns:
        Dict: A dictionary containing the summary of the evaluation process, including the total number of samples and samples per category.
        Also prints said dictionary to a table
    """

    # Read the necessary sheets from the Excel file
    df_inputs = pd.read_excel(filepath, sheet_name="prompts")
    df_info = pd.read_excel(filepath, sheet_name="simulation_info")

    # Convert DataFrames to dictionaries with list values
    dict1 = df_inputs.to_dict('list')
    dict1['outputs'] = []  # Add an empty list for 'outputs'
    dict2 = df_info.to_dict('list')

    # Combine the dictionaries into a single dictionary
    data = {**dict1, 'simulation_info': dict2}

    # Create the dictionary for the summary
    summary = {
        "Total samples": 0,
        "Samples per type": {k: 0 for k in data['simulation_info']['validator'] if k != 'coherency2'},
    }
    #Get the id for each type
    id_validator = {k: data["simulation_info"]["validator"][k-1] for k in data['simulation_info']['id_test']}
    
    # Count the number of samples per type
    for id_test in id_validator.keys():
        for id_sample in data['id_test']:
            if id_validator[id_test] != 'coherency2' and id_test == id_sample:
                summary["Total samples"] += 1
                summary["Samples per type"][id_validator[id_test]] += 1

    return summary

def evaluation_summary(filepath: str):
    """
    Creates a summary of the evaluation process from an Excel file.

    Args:
        filepath (str): The path to the Excel file that contains the evaluation results.

    Returns:
        Dict: A dictionary containing the summary of the evaluation process, including 
        the total number of samples, samples per category, total passed and failed samples and per category, and fail rates.
        Also prints said dictionary to a table
    """
    # Read the Excel file
    data = pd.read_excel(filepath)
    
    # Create the dictionary for the summary
    summary = {
        "Total samples": data.shape[0],
        "Samples per category": {},
        "Passed samples": 0,
        "Passed samples per category": {},
        "Failed samples": 0,
        "Failed samples per category": {},
        "Pass rate": 0,
        "Pass rate per category": {},
        "Fail rate": 0,
        "Fail rate per category": {}
    }

    # Calculate passed samples and passed per category
    passed = int(data['validation_result'].value_counts()['PASSED'])
    passed_per_category = {k: v for k,v in data.groupby(['validation_result', 'category']).size()['PASSED'].items()}

    # Get sample per category 
    summary['Samples per category'] = {k: v for k,v in data.groupby(['category']).size().items()}

    #Add passed and failed samples per category (failed = total - passed)
    summary["Passed samples"] = passed
    summary["Passed samples per category"] = passed_per_category
    summary["Failed samples"] = summary["Total samples"] - passed
    summary["Failed samples per category"] = {k: summary["Samples per category"][k] - v for k, v in passed_per_category.items()}

    # Calculate pass rate and fail rate (pass rate = passed / total, fail rate = 1 - pass rate)
    summary["Pass rate"] = passed / summary["Total samples"]
    summary["Pass rate per category"] = {k: v / summary["Samples per category"][k] for k, v in passed_per_category.items()}
    summary["Fail rate"] = 1 - passed / summary["Total samples"]
    summary["Fail rate per category"] = {k: 1 - summary["Pass rate per category"][k] for k, _ in passed_per_category.items()}
    
    return summary