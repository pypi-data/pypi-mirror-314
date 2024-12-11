import os
from typing import List, Union
import requests
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import tempfile
from brynq_sdk.brynq import BrynQ
from brynq_sdk.sodeco.address import Address
from brynq_sdk.sodeco.car import Car
from brynq_sdk.sodeco.leavecounters import LeaveCounters
from .costcentres import CostCentres
from .department import Departments
from .dimona import Dimona
from .family import Family
from .modifications import Modifications
from .parcom import Parcom
from .schedule import Schedule
from .nssocat import NssoCat
from .profcat import ProfCat
from .tax import Tax
from .worker import Workers
from .absences import Absences
from .schemas import DATEFORMAT

# Set the base class for Persinio. This class will be used to set the credentials and those will be used in all other classes.
class Sodeco(BrynQ):
    """
    Class to handle all Sodeco API requests.
    """

    def __init__(self, label: Union[str, List], employers: Union[str, List], debug: bool = False):
        super().__init__()
        credentials = self._get_credentials(label=label)
        self.base_url = credentials.get("base_url")
        
        # Get certificate and private key
        certificate = credentials.get("certificate")
        private_key = credentials.get("private_key")
        
        # Create temporary files for certificate and decrypted private key
        self.cert_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pem')
        self.key_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pem')
        
        # Write certificate to temporary file
        self.cert_file.write(certificate.encode())
        self.cert_file.close()
        
        # Decrypt and write private key to temporary file
        private_key_obj = serialization.load_pem_private_key(
            private_key.encode(),
            password=b'',  # Empty string password
            backend=default_backend()
        )
        
        # Write decrypted private key to temporary file
        with open(self.key_file.name, 'wb') as f:
            f.write(private_key_obj.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        # Create session with certificate authentication
        self.session = requests.Session()
        self.session.cert = (self.cert_file.name, self.key_file.name)
        
        self.employers = employers if isinstance(employers, List) else [employers]
        self.workers = Workers(self)
        self.modifications = Modifications(self)
        self.absences = Absences(self)
        self.cars = Car(self)
        self.costcentres = CostCentres(self)
        self.departments = Departments(self)
        self.leavecounters = LeaveCounters(self)
        self.parcom = Parcom(self)
        self.schedule = Schedule(self)
        self.nssocat = NssoCat(self)
        self.profcat = ProfCat(self)
        self.debug = debug

    def __del__(self):
        """Cleanup temporary files when the object is destroyed"""
        try:
            if hasattr(self, 'cert_file'):
                os.unlink(self.cert_file.name)
            if hasattr(self, 'key_file'):
                os.unlink(self.key_file.name)
        except Exception:
            pass

    def _get_credentials(self, label):
        """
        Sets the credentials for the SuccessFactors API.
        :param label (str): The label for the system credentials.
        :returns: headers (dict): The headers for the API request, including the access token.
        """
        credentials = self.get_system_credential(system='prisma-sodeco', label=label)
        base_url = credentials.get("base_url")
        certificate = credentials.get("certificate")
        private_key = credentials.get("private_key")

        return {"base_url": base_url, "certificate": certificate, "private_key": private_key}

    def update_headers(self, employer: str):
        self.session.headers.update({"Employer": employer})

    def send_request(self, request: requests.Request) -> requests.Response:
        """
        Send a request using the session with proper certificate authentication.
        
        Args:
            request: The request to send
            
        Returns:
            Response: The response from the server
            
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        # Prepare the request with session headers
        prepped = request.prepare()
        if hasattr(self.session, 'headers'):
            prepped.headers.update(self.session.headers)
            
        # Send the request and handle response
        response = self.session.send(prepped)
        response.raise_for_status()
        
        return response

    def get_new_worker_number(self):
        data = requests.get(url=f"{self.base_url}newworkernumber")
        return data