from revaisor_genaitesting.api_requests import *
from revaisor_genaitesting.utils import *

from tabulate import tabulate
from urllib.request import urlretrieve
from urllib.parse import urlparse
import requests
from functools import wraps

from typing import List, Dict
import os

NOT_HISTORY_KEYS = ['parameters', 'user', 'createdAt', 'startDate', 'endDate', 'pathToResult', 'pathToUploadedOutput', 'companyId', 'teamId', 'userId']
NOT_ITEMS_KEYS = ['description', 'inventoryItemCategory', 'idProvider', 'passedInternalAudit', 'passedExternalAudit', 'levelOfTrust', 'internalRiskAssessment', 'linkMoreInfo', 'controls', 'risks', 'score']

#To retry a function when a 401 Unauthorized exception occurs, getting new token
def retry_on_http_401():
    """Decorator to retry a function once after refreshing the token if a 401 Unauthorized occurs."""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)  # Attempt the first call
            except Exception as e:
                if "401" in str(e):  # Check for 401 Unauthorized
                    print("401 Unauthorized. Refreshing token and retrying...")
                    self.refresh_token()  # Refresh the token
                    return func(self, *args, **kwargs)  # Retry once
                raise  # Re-raise other exceptions
        return wrapper
    return decorator

class GenAIClient:
    def __init__(self, user: str, password:str):#, client_certificate_path:str = None, client_key_path:str = None, ca_certificate_path:str = None):
        """
        Initialize the client.
        
        Args:
            user (str): The user name.
            password (str): The user password.
        """
        """ Not yet implemented:
            client_certificate_path (str): The path to the client certificate.
            client_key_path (str): The path to the client key.
            ca_certificate_path (str): The path to the CA certificate.
        """
        self.user = user
        self.password = password
        # self.client_cert = (client_certificate_path, client_key_path)
        # self.ca_cert= ca_certificate_path

        self.token = get_token(user, password)
        self.user_id = get_user_id(self.token)

        companies = self.get_companies(table=False)
        self.current_company_id = companies[0]['id']
    
    def refresh_token(self):
        self.token = get_token(self.user, self.password)

    @retry_on_http_401()
    def get_companies(self, table: bool = True):
        """
        Get the list of companies.

        Args:
            table (bool, optional): If True, the companies will be displayed in a table. Defaults to True.

        Returns:
            List[Dict]: A list of dictionaries containing the companies.
        """
        companies = get_companies_request(self)
        if table:
            print(tabulate(companies, tablefmt='fancy_grid', headers='keys'))
        return companies
    
    @retry_on_http_401()
    def change_company(self, company_id: int):
        """
        Change the company.

        Args:
            company_id (int): The id of the company.
        """
        print(change_company_request(self, company_id))
        self.current_company_id = company_id

    
    @retry_on_http_401()
    def get_current_company(self):
        companies = get_companies_request(self)
        for company in companies:
            if company['id'] == self.current_company_id:
                print(f"Current company: {company['name']}")

    @retry_on_http_401()
    def get_teams(self, table: bool = True):
        """
        Get the list of teams.

        Args:
            table (bool, optional): If True, the teams will be displayed in a table. Defaults to True.

        Returns:
            List[Dict]: A list of dictionaries containing the teams.
        """
        teams = get_teams_request(self)
        for team in teams:
            team.pop('users', None)

        if table:
            print(tabulate(teams, tablefmt='fancy_grid', headers='keys'))
        return teams
    
    @retry_on_http_401()
    def get_controls(self, team_id: int, table: bool = True):
        """
        Get the list of controls.

        Args:
            team_id (int): The id of the team.
            table (bool, optional): If True, the controls will be displayed in a table. Defaults to True.

        Returns:
            List[Dict]: A list of dictionaries containing the controls.
        """
        controls = get_controls_request(self, team_id)
        if table:
            print(tabulate(controls, tablefmt='fancy_grid', headers='keys'))
        return controls
    
    @retry_on_http_401()
    def get_items(self, table: bool = True):
        """
        Get the list of items.

        Args:
            table (bool, optional): If True, the items will be displayed in a table. Defaults to True.

        Returns:
            List[Dict]: A list of dictionaries containing the items.
        """
        items = get_inventory_items_request(self)

        for key in NOT_ITEMS_KEYS:
            for h in items:
                h.pop(key, None)

        if table:
            print(tabulate(items, tablefmt='fancy_grid', headers='keys'))
        return items
    
    @retry_on_http_401()
    def create_simulation(self, description: str, language: str, num_samples: int, generators: List[str], name: str, control_id: int = -1, inventory_item_id: int = -1):
        """
        Create a new simulation.

        Args:
            description (str): A description of the model (this description is used to generate the prompts).
            language (str): The language the prompts are written in.
            num_samples (int): The number of samples to generate (per generator).
            generators (List[str]): A list of generators to use in the simulation. Options: plausibility, coherency, toxicity, harmful content, information disclosure, stereotypes, prompt injection, grc, cybersecurity.
            name (str): The name of the simulation.
            control_id (int, optional): The id of the control. Optional, if not provided, the simulation will be created without a control. If provided, an inventory item must alse be provided.
            inventory_item_id (int, optional): The id of the inventory item. Optional, if not provided, the simulation will be created without an inventory item. If provided, a control must alse be provided.
        """
        create_simulation_request(self, description, language, num_samples, generators, name, control_id, inventory_item_id)
    
    @retry_on_http_401()
    def create_evaluation(self, name: str, filepath: str, control_id: int = -1, inventory_item_id: int = -1):
        """
        Create a new evaluation.

        Args:
            name (str): The name for the evaluation.
            filepath (str): The path to the Excel file that was created by the simulation with the outputs from the model.
            control_id (int, optional): The id of the control. Optional, if not provided, the evaluation will be created without a control. If provided, an inventory item must alse be provided.
            inventory_item_id (int, optional): The id of the inventory item. Optional, if not provided, the evaluation will be created without an inventory item. If provided, a control must alse be provided.
        """
        create_evaluation_request(self, name, filepath, control_id, inventory_item_id)
    
    @retry_on_http_401()
    def get_simulation_history(self, page: int = 0, table: bool = True):
        """
        Get the history of the simulation.

        Args:
            page (int, optional): The page number of the history (10 per page). Defaults to 0.
            table (bool, optional): Whether to print the history in a table. Defaults to True.

        Returns:
            List[Dict]: A list of dictionaries containing the history of the simulation.

        Outputs:
            A table with the history (if requested)
        """
        #Get the history
        history = get_simulation_history_request(self, page)['content']

        for key in NOT_HISTORY_KEYS:
            for h in history:
                h.pop(key, None)

        #Organize it for printing the table if requested
        if table:
            print(tabulate(history, tablefmt='fancy_grid', headers='keys'))

        #Return the history
        return history

    @retry_on_http_401()
    def get_evaluation_history(self, page: int = 0, table: bool = True):
        """
        Get the history of the evaluation.

        Args:
            page (int, optional): The page number of the history (10 per page). Defaults to 0.
            table (bool, optional): Whether to print the history in a table. Defaults to True.

        Returns:
            List[Dict]: A list of dictionaries containing the history of the evaluation.
        
        Outputs:
            A table with the history (if requested)
        """
        #Get the history
        history = get_evaluation_history_request(self, page)['content']

        for key in NOT_HISTORY_KEYS:
            for h in history:
                h.pop(key, None)

        #Organize it for printing the table if requested
        if table:
            print(tabulate(history, tablefmt='fancy_grid', headers='keys'))

        #Return the history
        return history

    @retry_on_http_401()
    def get_full_history(self, page: int = 0, table: bool = True):
        """
        Get the history of simulation and evaluation combined.

        Args:
            page (int, optional): The page number of the history (10 per page). Defaults to 0.
            table (bool, optional): Whether to print the history in a table. Defaults to True.

        Returns:
            List[Dict]: A list of dictionaries containing the history of simulation and evaluation.
        
        Outputs:
            A table with the history (if requested)
        """
        #Get the history
        history = get_simulation_evaluation_history_request(self, page)['content']

        for key in NOT_HISTORY_KEYS:
            for h in history:
                h.pop(key, None)

        #Organize it for printing the table if requested
        if table:
            print(tabulate(history, tablefmt='fancy_grid', headers='keys'))

        #Return the history
        return history
    
    @retry_on_http_401()
    def get_simulation_summary(self, filepath: str = "", id: int = -1, table: bool = True):
        """
        Get a summary of the simulation process.

        Args:
            filepath (str): The path to the Excel file that contains the simulation results.
            table (bool, optional): Whether to print the summary in a table. Defaults to True.

        Returns:
            Dict: A dictionary containing the summary of the evaluation process, including the total number of samples and samples per category.

        Outputs:
            A table with the summary (if requested)
        """
        #Get the summary
        if filepath:
            summary = simulation_summary(filepath)
        elif id != -1:
            summary = get_simulation_summary_request(self, id)
        else:
            raise ValueError("Either filepath and id must be provided, verify that they are not empty or invalid.")
        #Organize it for printing the table
        if table:
            data = [[k,v] for k,v in summary['Samples per type'].items()]
            data.append(['Total', summary['Total samples']])
            headers = ['Type', 'Samples']
            print(tabulate(data, headers=headers, tablefmt='fancy_grid'))

        #Return the summary
        return summary
    
    @retry_on_http_401()
    def get_evaluation_summary(self, filepath: str = "", id: int = -1, table: bool = True):
        """
        Get a summary of the evaluation process.

        Args:
            filepath (str): The path to the Excel file that contains the simulation results.
            table (bool, optional): Whether to print the summary in a table. Defaults to True.

        Returns:
            Dict: A dictionary containing the summary of the evaluation process, including 
            the total number of samples, samples per category, total passed and failed samples and per category, and fail rates.

        Outputs:
            A table with the summary (if requested)
        """
        #Get the summary
        if filepath:
            summary = evaluation_summary(filepath)
        elif id != -1:
            summary = get_evaluation_summary_request(self, id)
        else:
            raise ValueError("Either filepath and id must be provided, verify that they are not empty or invalid.")

        #Organize it for printing the table
        if table:
            categories = summary['Samples per category'].keys()
            data = [[category] + [d[category] for d in summary.values() if type(d) == dict] for category in categories] 
            data.append(['Total'] + [v for k,v in summary.items() if type(v) != dict])
            headers = ['Category', 'Total Samples', 'Passed Samples', 'Failed Samples', 'Pass Rate', 'Fail Rate']
            print(tabulate(data, headers=headers, tablefmt='fancy_grid'))

        #Return the summary
        return summary
    
    @retry_on_http_401()
    def download_simulation_results(self, id: int, filepath: str =""):
        """
        Download the simulation results file.

        Args:
            id (int): The id of the simulation.
            filename (str): The name for the downloaded file without extension. Defaults to the name in the cloud. 
            If you want to save the file to a directory, give the value as "path/name", the directory must exist.

        Downloads the simulation results file.
        """
        url = get_simulation_download_url_request(self, id)
        if not filepath:
            data = urlparse(url)
            filepath = os.path.basename(data.path)
        else:
            filepath = filepath + ".xlsx"
        urlretrieve(url, filepath)
        print("File successfully downloaded to " + filepath)

    @retry_on_http_401()
    def download_evaluation_results(self, id: int, filepath: str = ""):
        """
        Get the download URL for the evaluation.

        Args:
            id (int): The id of the evaluation.
            filename (str): The name for the downloaded file without extension. Defaults to the name in the cloud. 
            If you want to save the file to a directory, give the value as "path/name", the directory must exist.

        Downloads the evaluation results file.
        """
        url = get_evaluation_download_url_request(self, id)
        if not filepath:
            data = urlparse(url)
            filepath = os.path.basename(data.path)
        else:
            filepath = filepath + ".xlsx"
        urlretrieve(url, filepath)
        print("File successfully downloaded to " + filepath)