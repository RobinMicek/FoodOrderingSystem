"""
********************************************************

    Tento kód je součástí projektu 'K Okénku',
    který je psán jako maturitní práce z informatiky.

    Gymnázium Sokolov a Krajské vzdělávací centrum,
    příspěvková organizace

    Robin Míček, 8.E

********************************************************
"""

# PACKAGES IMPORTS
import os
import sys
import requests

# IMPORTS FROM PACKAGES

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from database.handle_database import Database
from logs import create_log

# IMPORT CONSTANT VARIABLES (/app/variables.py)
from getConfig import getConfig


class ServerRequests():

    def __init__(self) -> None:

        CONFIG = getConfig()
        
        self.serverUrl = CONFIG["serverUrl"] if CONFIG != None else None
        self.establishmentSlug = CONFIG["establishmentSlug"] if CONFIG != None else None
        self.establishmentToken = CONFIG["establishmentToken"] if CONFIG != None else None

        self.auth_data = {
            "EstablishmentSlug": self.establishmentSlug,
            "EstablishmentToken": self.establishmentToken
        }
        

    def get_establishment_fts(self, serverUrl = None, establishmentSlug = None, establishmentToken = None):

        self.auth_data = {
            "EstablishmentSlug": establishmentSlug,
            "EstablishmentToken": establishmentToken
        }

        try:
            response = requests.get(f"{serverUrl}/kitchenhub/get-establishment", headers=self.auth_data, verify=False)

            if int(response.status_code) == 200:
                create_log(type="ALERT", message=f"Request sucessful [Request Type: Get Establishment]")
                return response.json()["data"]
            else:
                raise requests.exceptions.RequestException
    
        except requests.exceptions.RequestException as e:
            create_log(type="ERROR", message=f"Something went wrong with the server request [Request Type: Get Establishment] [{e}]")
            return False

        except Exception as e:
            create_log(type="ERROR", message=f"Server request could not have been fulfilled [Request Type: Get Establishment] [{e}]")
            return False


    def get_all_orders(self):

        try:
            response = requests.get(f"{self.serverUrl}/kitchenhub/get-all-orders", headers=self.auth_data, verify=False)
            
            if int(response.status_code) == 200:
                create_log(type="ALERT", message=f"Request sucessful [Request Type: Get All Orders]")
                return response.json()["data"]
            else:
                raise requests.exceptions.RequestException
    
        except requests.exceptions.RequestException as e:
            create_log(type="ERROR", message=f"Something went wrong with the server request [Request Type: Get All Orders] [{e}]")
            return False

        except Exception as e:
            create_log(type="ERROR", message=f"Server request could not have been fulfilled [Request Type: Get All Orders] [{e}]")
            return False
        

    def update_order_status(self, orderId = None, newStatus = None):
       
        try:
            response = requests.post(f"{self.serverUrl}/kitchenhub/update-order-status", headers=self.auth_data, json={"orderId": f"{orderId}", "newStatus": f"{newStatus}"}, verify=False)
            
            if int(response.status_code) == 200:
                create_log(type="ALERT", message=f"Request sucessful [Request Type: Update Order Status]")
                return True
            else:
                raise requests.exceptions.RequestException
    
        except requests.exceptions.RequestException as e:
            create_log(type="ERROR", message=f"Something went wrong with the server request [Request Type: Update Order Status] [{e}]")
            return False

        except Exception as e:
            create_log(type="ERROR", message=f"Server request could not have been fulfilled [Request Type: Update Order Status] [{e}]")
            return False