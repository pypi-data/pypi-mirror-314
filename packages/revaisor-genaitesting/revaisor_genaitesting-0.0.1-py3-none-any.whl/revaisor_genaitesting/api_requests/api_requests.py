import requests
from typing import List
from revaisor_genaitesting.utils import convert_keys_to_title


API_URL = "https://spring-boot-core-master-343581670632.europe-west2.run.app/core/api"

def get_token(user: str, password: str):
    """
    Get the token for authenticating the user.

    Args:
        user (str): The user name.
        password (str): The password.

    Returns:
        str: The token for the user.
    """
    data = {"email": user, "password": password, "returnSecureToken": True}
    r = requests.post(f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyAim5IQ13frsJQ7FHM_EGJ86tayn_U8iNU", json = data)
    if r.status_code == 200:
        return r.json()['idToken']
    
def get_user_id(token: str):
    """
    Get the user id from the token.

    Args:
        token (str): The token for the user.

    Returns:
        str: The user id.
    """
    r = requests.get(f"{API_URL}/users/basic", headers={"Authorization": f"Bearer {token}"})
    if r.status_code == 200:
        return r.json()['id']
    
def get_companies_request(client):
    """
    Get the list of companies.

    Args:
        client (GenAIClient): The client object.

    Returns:
        List[Dict]: A list of dictionaries containing the companies.
    """
    # Token for authentication    
    token = client.token

    r = requests.get(f"{API_URL}/users/getCompanies", headers={"Authorization": f"Bearer {token}"})

    if r.status_code == 200:
        return r.json()
    else:
        raise Exception("status code: " + str(r.status_code) + " " + r.text)
    
def change_company_request(client, company_id: int):
    """
    Change the company.

    Args:
        client (GenAIClient): The client object.
        company_id (int): The id of the company.
    """
    # Token for authentication
    token = client.token

    r = requests.post(f"{API_URL}/users/changeCompany", headers={"companyId": f"{company_id}", "Authorization": f"Bearer {token}"})
    
    if r.status_code == 200:
        return f"Company successfully changed!"
    else:
        raise Exception("status code: " + str(r.status_code) + " " + r.text)

def get_teams_request(client):
    """
    Get the list of teams.

    Args:
        client (GenAIClient): The client object.

    Returns:
        List[Dict]: A list of dictionaries containing the teams.
    """
    # Token for authentication
    token = client.token
    user_id = client.user_id

    r = requests.get(f"{API_URL}/users/{user_id}/teams", headers={"Authorization": f"Bearer {token}"})

    if r.status_code == 200:
        return r.json()
    else:
        raise Exception("status code: " + str(r.status_code) + " " + r.text)
    
def get_controls_request(client, team_id: int):
    """
    Get the list of controls.

    Args:
        client (GenAIClient): The client object.
        team_id (int): The id of the team.

    Returns:
        List[Dict]: A list of dictionaries containing the controls.
    """
    # Token for authentication
    token = client.token

    r = requests.get(f"{API_URL}/teams/{team_id}/basicControls", headers={"Authorization": f"Bearer {token}"})

    if r.status_code == 200:
        return r.json()
    else:
        raise Exception("status code: " + str(r.status_code) + " " + r.text)
    
def get_inventory_items_request(client):
    """
    Get the list of inventory items.

    Args:
        client (GenAIClient): The client object.

    Returns:
        List[Dict]: A list of dictionaries containing the inventory items.
    """
    # Token for authentication
    token = client.token

    r = requests.get(f"{API_URL}/inventoryItems", headers={"Authorization": f"Bearer {token}"})

    if r.status_code == 200:
        return r.json()
    else:
        raise Exception("status code: " + str(r.status_code) + " " + r.text)

def create_simulation_request(client, description: str, language: str, num_samples: int, generators: List[str], filename: str, control_id: int = -1, inventory_item_id: int = -1):
    """
    Request to create a new simulation.

    Args:
        client (GenAIClient): The client object.
        description (str): A description of the model (this description is used to generate the prompts).
        language (str): The language the prompts are written in.
        num_samples (int): The number of samples to generate (per generator).
        num_samples (int): The number of samples to generate (per generator).
        generators (List[str]): A list of generators to use in the simulation. Options: plausibility, coherency, toxicity, harmful content, information disclosure, stereotypes, prompt injection, grc, cybersecurity.
        filename (str): The name of the file that is created.
        control_id (int, optional): The id of the control. Optional, if not provided, the simulation will be created without a control. If provided, an inventory item must alse be provided.
        inventory_item_id (int, optional): The id of the inventory item. Optional, if not provided, the simulation will be created without an inventory item. If provided, a control must alse be provided.
    """
    # Token for authentication
    token = client.token

    # Json request body
    json_gen = {
        "description": description,
        "language": language,
        "num_samples": num_samples,
        "generators": generators
    }

    params={"name": filename}
    if control_id != -1 and inventory_item_id != -1:
        params["controlId"] = control_id
        params["inventoryItemId"] = inventory_item_id
    elif control_id != -1 and inventory_item_id == -1:
        raise Exception("inventory_item_id must be provided if control_id is provided")
    elif control_id == -1 and inventory_item_id != -1:
        raise Exception("control_id must be provided if inventory_item_id is provided")        
    # Request
    r = requests.post(f"{API_URL}/simulations/llm", json=json_gen, headers={"Authorization": f"Bearer {token}"}, params=params)

    # Check status, if not 201 (Created), raise exception
    if r.status_code != 201: 
        raise Exception("status code: " + str(r.status_code) + " " + r.text)
    
    print("Simulation created successfully!")

def create_evaluation_request(client, name: str, filepath: str, control_id: int = -1, inventory_item_id: int = -1):
    """
    Request to create a new evaluation.

    Args:
        client (GenAIClient): The client object.
        name (str): The name for the evaluation.
        filepath (str): The path to the Excel file that was created by the simulation with the outputs from the model.
        control_id (int, optional): The id of the control. Optional, if not provided, the evaluation will be created without a control. If provided, an inventory item must alse be provided.
        inventory_item_id (int, optional): The id of the inventory item. Optional, if not provided, the evaluation will be created without an inventory item. If provided, a control must alse be provided.
    """
    # Token for authentication
    token = client.token

    # Open file
    with open(filepath, 'rb') as f:
        files = {"file": ("evaluation.xlsx", f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}

        params={"name": name}
        if control_id != -1 and inventory_item_id != -1:
            params["controlId"] = control_id
            params["inventoryItemId"] = inventory_item_id
        elif control_id != -1 and inventory_item_id == -1:
            raise Exception("inventory_item_id must be provided if control_id is provided")
        elif control_id == -1 and inventory_item_id != -1:
            raise Exception("control_id must be provided if inventory_item_id is provided")   

        r = requests.post(f"{API_URL}/evaluations/llm", files=files, headers={"Authorization": f"Bearer {token}"}, params=params)

    # Check status, if not 201 (Created), raise exception
    if r.status_code != 201: 
        raise Exception("status code: " + str(r.status_code) + " " + r.text)
    print("Evaluation created successfully!")


def get_simulation_history_request(client, page: int = 0):
    """
    Get the history of the simulation.

    Args:
        client (GenAIClient): The client object.
        page (int, optional): The page number of the history (10 per page). Defaults to 0.

    Returns:
        List[Dict]: A list of dictionaries containing the history of the simulation.

    Outputs:
        A table with the history
    """
    # Token for authentication
    token = client.token

    r = requests.get(f"{API_URL}/simulations/llm/company", params={"page": page}, headers={"Authorization": f"Bearer {token}"})
    if r.status_code == 200:
        return r.json()
    elif r.status_code == 204:
        raise Exception(f"status code {r.status_code}: No simulations found in page {page}")
    else:
        raise Exception("status code: " + str(r.status_code) + " " + r.text)

def get_evaluation_history_request(client, page: int = 0):
    """
    Get the history of the evaluation.

    Args:
        client (GenAIClient): The client object.
        page (int, optional): The page number of the history (10 per page). Defaults to 0.

    Returns:
        List[Dict]: A list of dictionaries containing the history of the evaluation.

    Outputs:
        A table with the history
    """
    # Token for authentication
    token = client.token
    r = requests.get(f"{API_URL}/evaluations/llm/company", params={"page": page}, headers={"Authorization": f"Bearer {token}"})
    if r.status_code == 200:
        return r.json()
    elif r.status_code == 204:
        raise Exception(f"status code {r.status_code}: No evaluations found in page {page}")
    else:
        raise Exception("status code: " + str(r.status_code) + " " + r.text)

def get_simulation_evaluation_history_request(client, page: int = 0):
    """
    Get the history of simulation and evaluation combined.

    Args:
        client (GenAIClient): The client object.
        page (int, optional): The page number of the history (10 per page). Defaults to 0.

    Returns:
        List[Dict]: A list of dictionaries containing the history of the simulation and evaluation.

    Outputs:
        A table with the history
    """
    # Token for authentication
    token = client.token
    r = requests.get(f"{API_URL}/simulationsEvaluations/company", params={"page": page, "simulationType": "LLM"}, headers={"Authorization": f"Bearer {token}"})
    if r.status_code == 200:
        return r.json()
    elif r.status_code == 204:
        raise Exception(f"status code {r.status_code}: No simulations or evaluations found in page {page}")
    else:
        raise Exception("status code: " + str(r.status_code) + " " + r.text)

def get_simulation_summary_request(client, id: int):
    """
    Get a summary of the simulation process.

    Args:
        client (GenAIClient): The client object.
        id (int): The id of the simulation.

    Returns:
        Dict: A dictionary containing the summary of the simulation process, including the total number of samples and samples per category.
    """
    # Token for authentication
    token = client.token

    r = requests.get(f"{API_URL}/simulations/llm/summary/{id}", headers={"Authorization": f"Bearer {token}"})

    if r.status_code == 200:
        resp = r.json()
        resp.pop('downloadUrl', None)
        resp = convert_keys_to_title(resp)
        return resp
    else:
        raise Exception("status code: " + str(r.status_code) + " " + r.text)
    
def get_evaluation_summary_request(client, id: int):
    """
    Get a summary of the simulation process.

    Args:
        client (GenAIClient): The client object.
        id (int): The id of the simulation.

    Returns:
        Dict: A dictionary containing the summary of the simulation process, including the total number of samples and samples per category.
    """
    # Token for authentication
    token = client.token

    r = requests.get(f"{API_URL}/evaluations/llm/summary/{id}", headers={"Authorization": f"Bearer {token}"})

    if r.status_code == 200:
        resp = r.json()
        resp.pop('downloadUrl', None)
        resp = convert_keys_to_title(resp)
        return resp
    else:
        raise Exception("status code: " + str(r.status_code) + " " + r.text)


def get_simulation_download_url_request(client, id: int):
    """
    Get the download url for the simulation.

    Args:
        client (GenAIClient): The client object.
        id (str): The id of the simulation.

    Returns:
        str: The download url for the simulation.
    """
    # Token for authentication
    token = client.token

    r = requests.get(f"{API_URL}/simulations/llm/signed-url/{id}", headers={"Authorization": f"Bearer {token}"})

    if r.status_code == 200:
        resp = r.json()
        return resp['signedUrl']
    else:
        raise Exception("status code: " + str(r.status_code) + " " + r.text)

def get_evaluation_download_url_request(client, id: int):
    """
    Get the download url for the evaluation.

    Args:
        client (GenAIClient): The client object.
        id (str): The id of the evaluation.

    Returns:
        str: The download url for the evaluation.
    """
    # Token for authentication
    token = client.token

    r = requests.get(f"{API_URL}/evaluations/llm/signed-url/{id}", headers={"Authorization": f"Bearer {token}"})

    if r.status_code == 200:    
        resp = r.json()
        return resp['signedUrl']
    else:
        raise Exception("status code: " + str(r.status_code) + " " + r.text)
