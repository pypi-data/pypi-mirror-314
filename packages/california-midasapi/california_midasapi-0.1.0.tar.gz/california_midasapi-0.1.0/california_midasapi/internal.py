from typing import Literal
import requests
import base64
import jwt
import time

from .exception import MidasAuthenticationException, MidasException

class Midas():
    def __request(self, method: Literal['GET', 'POST'], url: str):
        """Preform a request with the stored auth token and return the body."""
        if (self.auth_token is None or not Midas.__isTokenValid(self.auth_token)):
            self.__loginAndStore(self.username, self.password)
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'california-midasapi.py',
            'Authorization': "Bearer " + self.auth_token,
        }
        response = requests.request(method, url, headers=headers)
        if (not response.ok):
            raise MidasException(f"Error preforming request: {response.status_code} {response.text}")
        return response.text
    
    def __loginAndStore(self, username: str, password: str):
        '''
        Logs in with a username and password, storing the JWT token for use in future calls.
        '''
        credentials = username + ":" + password
        credentials_encodedBytes = base64.b64encode(credentials.encode("utf-8"))
    
        headers = {b'Authorization': b'BASIC ' + credentials_encodedBytes}
        url = 'https://midasapi.energy.ca.gov/api/token'

        response = requests.get(url,headers=headers)

        if (not response.ok):
            raise MidasAuthenticationException(response.text)

        self.auth_token = response.headers['Token']
    
    @staticmethod
    def __isTokenValid(token: str) -> bool:
        """Return if the provided token is still valid"""
        decoded = jwt.decode(token, algorithms=["HS256"], options={"verify_signature": False})
        future = time.time() + 120 # 2 minutes from now
        return decoded["exp"] > future # expires more than set time from now