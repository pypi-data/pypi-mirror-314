import requests
import webbrowser
import time
from typing import Optional, Dict, Any
import logging

AUTH0_CLIENT_ID="h1MJ9eaKPGkOvbMCqCeZjgsBJaf4AN7Y"
AUTH0_DOMAIN="https://snowdropquantum.ca.auth0.com"
AUTH0_SCOPE="openid profile email name picture"
AUTH0_AUDIENCE="https://www.snowdropquantum.com"

class Auth0DeviceAuthorization:
    def __init__(self):
        """
        Initialize the Auth0DeviceAuthorization class with environment variables.
        
        Example of environment variables:
        - AUTH0_CLIENT_ID: Your Auth0 Client ID
        - AUTH0_SCOPE: Your Auth0 Scope (default: 'openid profile email')
        - AUTH0_AUDIENCE: Your Auth0 API Audience
        - AUTH0_DOMAIN: Your Auth0 Domain (e.g., your-domain.auth0.com)
        """

        self.client_id = AUTH0_CLIENT_ID
        self.audience = AUTH0_AUDIENCE
        self.scope = AUTH0_SCOPE
        self.domain = AUTH0_DOMAIN

        self.device_code = None
        self.user_code = None
        self.verification_uri = None
        self.verification_uri_complete = None
        self.interval = 5  # Default polling interval (can be updated by the response)

    def start_device_authorization(self) -> bool:
        """
        Start the device authorization process by making a request to Auth0.

        Returns:
            bool: True if the request was successful, False otherwise.
        """

        url = f'{self.domain}/oauth/device/code'
        payload = {
            'client_id': self.client_id,
            'scope': self.scope,
            'audience': self.audience
        }
        headers =  { 'content-type': "application/x-www-form-urlencoded" }
        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            self.device_code = data['device_code']
            self.user_code = data['user_code']
            self.verification_uri = data['verification_uri']
            self.verification_uri_complete = data.get('verification_uri_complete')
            self.expires_in = data.get('expires_in')
            self.interval = data.get('interval', self.interval)
            return True
        else:
            logging.error("Error initiating device authorization:", response.json())
            return False

    def prompt_user(self) -> None:
        """
        Prompt the user to visit the verification URI and enter the user code.
        """
        if self.verification_uri_complete:
            print(f"Please go to {self.verification_uri_complete} to authenticate.")
            webbrowser.open(self.verification_uri_complete)
        else:
            print(f"Please go to {self.verification_uri} and enter the code: {self.user_code}")
            webbrowser.open(self.verification_uri)

    def poll_token(self) -> Optional[Dict[str, Any]]:
        """
        Poll Auth0 for the authentication token.

        Returns:
            Optional[Dict[str, Any]]: The token response if successful, None otherwise.
        """
        url = f'{self.domain}/oauth/token'
        payload = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
            'device_code': self.device_code,
            'client_id': self.client_id,
            'audience': "https://www.snowdropquantum.com"
        }
        headers = { 'content-type': "application/x-www-form-urlencoded" }

        while True:
            response = requests.post(url, data=payload, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                data = response.json()
                if error:= data.get('error'):
                    if error == 'authorization_pending':
                        logging.info("Waiting for user authorization...")
                        time.sleep(self.interval)
                    elif error == 'slow_down':
                        logging.debug("Slowing down polling...")
                        self.interval += 5
                        time.sleep(self.interval)
                    elif error == 'expired_token':
                        logging.error("Device authorization expired.")
                        return None
                    elif error == 'access_denied':
                        logging.error("User denied access.")
                        return None
                    else:
                        logging.error("Error polling token:", data)
                        return None

    def authenticate(self) -> Optional[dict]:
        """
        Perform the authentication process.

        Returns:
            Optional[str]: The access token if authentication is successful, None otherwise.
        """
        if self.start_device_authorization():
            self.prompt_user()
            token_response = self.poll_token()
            if token_response:
                print("Successfully authenticated!")
                logging.debug("Access Token:", token_response['access_token'])
                logging.debug("ID Token:", token_response['id_token'])
                return token_response
            else:
                logging.critical("Failed to authenticate.")
                return None


__all__ = ["Auth0DeviceAuthorization"]
