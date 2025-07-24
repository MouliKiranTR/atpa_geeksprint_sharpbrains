import json
import time
import requests
import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlencode
from dotenv import load_dotenv, set_key

class OpenArenaAuthenticator:
    def __init__(self, config=None):
        """
        Initialize the TR Authenticator with configuration
        
        Args:
            config (dict, optional): Configuration dictionary. If None, uses default config.
        """
        # Load environment variables from '.env' file 
        load_dotenv('.env')
        
        self.config = config or {
            "client_id": "tgUVZwXAqZWWByus9QSPi1yNyoN2lflI",
            "redirect_uri": "https://dataandanalytics.int.thomsonreuters.com",
            "auth_url": "https://auth.thomsonreuters.com/authorize",
            "token_url": "https://auth.thomsonreuters.com/oauth/token",
            "api_url": "https://aiopenarena.gcs.int.thomsonreuters.com/v1/user",
            "env_file": ".env", 
            "code_verifier": "vFV--SZvnyxmdapz62lNkKz0Nrbtnd_uO0huZe0A60c",
            "code_challenge": "BWtAOz7YKH24sAlLZAAc-xi_UFJm3hiP1stOedx9U00"
        }
    
    def save_tokens_to_env(self, access_token, refresh_token=None, expires_at=None):
        """
        Save tokens to environment file
        
        Args:
            access_token (str): Access token
            refresh_token (str, optional): Refresh token
            expires_at (float, optional): Token expiration timestamp
        """
        env_file = self.config["env_file"]
        
        set_key(env_file, "TR_ACCESS_TOKEN", access_token)
        
        if refresh_token:
            set_key(env_file, "TR_REFRESH_TOKEN", refresh_token)
        
        if expires_at:
            set_key(env_file, "TR_TOKEN_EXPIRES_AT", str(expires_at))
    
    def get_tokens_from_env(self):
        """
        Get tokens from environment variables
        
        Returns:
            dict: Dictionary containing token information
        """
        return {
            "access_token": os.getenv("TR_ACCESS_TOKEN"),
            "refresh_token": os.getenv("TR_REFRESH_TOKEN"),
            "expires_at": float(os.getenv("TR_TOKEN_EXPIRES_AT", "0"))
        }
    
    def get_auth_code(self):
        """
        Get authorization code using Chrome browser automation
        
        Returns:
            str: Authorization code if successful, None otherwise
        """
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            params = {
                "client_id": self.config["client_id"],
                "scope": "openid profile email",
                "redirect_uri": self.config["redirect_uri"],
                "audience": "49d70a58-9509-48a2-ae12-4f6e00ceb270",
                "connection": "sso-auth",
                "response_type": "code",
                "code_challenge": self.config["code_challenge"],
                "code_challenge_method": "S256"
            }
            
            auth_url = f"{self.config['auth_url']}?{urlencode(params)}"
            
            driver.get(auth_url)
            auth_code = None
            last_url = ""
            start_time = time.time()
            stability_count = 0
            stable_url = None
            
            while time.time() - start_time < 300:
                current_url = driver.current_url
                
                if self.config["redirect_uri"] in current_url and "code=" in current_url:
                    if current_url == last_url:
                        stability_count += 1
                        
                        if stability_count >= 3:
                            match = re.search(r'code=([^&]+)', current_url)
                            if match:
                                auth_code = match.group(1)
                                break
                    else:
                        stability_count = 1
                        stable_url = current_url
                
                last_url = current_url
                time.sleep(1)
            
            if not auth_code and stable_url and "code=" in stable_url:
                match = re.search(r'code=([^&]+)', stable_url)
                if match:
                    auth_code = match.group(1)
            
            if auth_code:
                return auth_code
            else:
                url_input = input("Please paste the URL from your browser: ").strip()
                if "code=" in url_input:
                    match = re.search(r'code=([^&]+)', url_input)
                    if match:
                        return match.group(1)
                return None
            
        finally:
            driver.quit()

    def get_tokens(self, auth_code):
        """
        Exchange authorization code for access tokens
        
        Args:
            auth_code (str): Authorization code from OAuth flow
            
        Returns:
            str: Access token if successful, None otherwise
        """
        token_data = {
            "client_id": self.config["client_id"],
            "code_verifier": self.config["code_verifier"],
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": self.config["redirect_uri"]
        }
        headers = {
            "content-type": "application/x-www-form-urlencoded"
        }
        
        response = requests.post(self.config["token_url"], data=token_data, headers=headers)
        
        if response.status_code == 200:
            token_response = response.json()
            
            expires_at = time.time() + token_response["expires_in"] - 300
            
            self.save_tokens_to_env(
                access_token=token_response["access_token"],
                refresh_token=token_response.get("refresh_token"),
                expires_at=expires_at
            )
                
            return token_response["access_token"]
        else:
            print(f"Token request failed with status {response.status_code}: {response.text}")
            return None

    def refresh_token(self):
        """
        Refresh the access token using refresh token
        
        Returns:
            str: New access token if successful, None otherwise
        """
        try:
            tokens = self.get_tokens_from_env()
            
            refresh_token = tokens.get("refresh_token")
            if not refresh_token:
                print("No refresh token available")
                return None
                
            token_data = {
                "client_id": self.config["client_id"],
                "grant_type": "refresh_token",
                "refresh_token": refresh_token
            }
            
            response = requests.post(self.config["token_url"], data=token_data)
            
            if response.status_code == 200:
                new_tokens = response.json()
                
                expires_at = time.time() + new_tokens["expires_in"] - 300
                
                self.save_tokens_to_env(
                    access_token=new_tokens["access_token"],
                    refresh_token=new_tokens.get("refresh_token", refresh_token),
                    expires_at=expires_at
                )
                    
                return new_tokens["access_token"]
            else:
                print(f"Token refresh failed with status {response.status_code}: {response.text}")
                return None
        except Exception as e:
            print(f"Error refreshing token: {e}")
            return None

    def get_access_token(self):
        """
        Get a valid access token (from cache, refresh, or new authentication)
        
        Returns:
            str: Valid access token if successful, None otherwise
        """
        try:
            tokens = self.get_tokens_from_env()
            
            # Check if current token is still valid
            if tokens["access_token"] and time.time() < tokens.get("expires_at", 0):
                return tokens["access_token"]
                
            # Try to refresh token
            token = self.refresh_token()
            if token:
                return token
        except Exception as e:
            print(f"Error getting access token from env: {e}")
            
        # Fall back to full authentication
        auth_code = self.get_auth_code()
        if auth_code:
            return self.get_tokens(auth_code)
            
        return None

    def make_api_request(self, token, endpoint=None):
        """
        Make an authenticated API request
        
        Args:
            token (str): Access token
            endpoint (str, optional): API endpoint. If None, uses default user endpoint
            
        Returns:
            dict: API response if successful, None otherwise
        """
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        url = endpoint or self.config["api_url"]
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API request failed with status {response.status_code}: {response.text}")
            return None

    def authenticate_and_get_token(self):
        """
        Main method to authenticate and get a valid token
        
        Returns:
            str: Valid access token if successful, None otherwise
        """
        token = self.get_access_token()
        
        if token:
            result = self.make_api_request(token)
            if result:
                print(f"Authenticated as: {result.get('first_name', '')} {result.get('last_name', '')}")
            return token
        else:
            print("Authentication failed")
            return None