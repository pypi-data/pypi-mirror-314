"""This module implments a client for the Intelligent Plant App Store API"""
__author__ = "Ross Kelso"
__docformat__ = 'reStructuredText'

import time

import urllib

import requests

import intelligent_plant.data_core_client as data_core_client
import intelligent_plant.http_client as http_client

from intelligent_plant.http_client import json

class AppStoreClient(http_client.HttpClient):
    """Access the Intelligent Plant Appstore API"""

    def __init__(self, access_token: str, refresh_token: str = None, expires_in: int = None, base_url: str = "https://appstore.intelligentplant.com/", **kwargs):
        """
        Initialise an App Store Client
        :param access_token: The access token used to authenticate this client. 
            Get this by using the authorization code c#grant flow (for web servers) or
            the implicit grant flow (for clients e.g. native apps, JS web clients, Jupyter Notebook)
            Examples of this can be found in the "examples" folder and Jupyter notebook.
        :param refresh_token: The refresh token for this client (currently unused).
        :param base_url: The URL of the app store (optional, default value is "https://appstore.intelligentplant.com/").

        :return: An app store client that uses the provided access token for authorization.
        """
        self.access_token = access_token
        self.refresh_token = refresh_token

        if expires_in is None:
            self.expiry_time = None
        else:
            self.expiry_time = time.time() + expires_in

        http_client.HttpClient.__init__(self, base_url, authorization_header ="Bearer " + self.access_token, **kwargs)

    def get_data_core_client(self, *args, **kwargs):
        """
        Get the data core client with the same authorization details as this app store client.
        :param base_url: The base URL for the data core API. The default value is "https://api.intelligentplant.com/datacore/" (the app store data api)

        :return: The data core client with the same authorization as this app store client.
        """
        kwargs['authorization_header'] = "Bearer " + self.access_token
        return data_core_client.DataCoreClient(*args, **kwargs)

    def get_user_info(self) -> json:
        """
        Get the authenticated user's user info from the app store.

        :return: The users info as a parsed JSON object.

        :raises: :class:`HTTPError` if an HTTP error occurrs.
        :raises: :class:`JSONDecodeError` if JSON decoding fails.
        """
        return self.get_json("api/resource/userinfo")

    def get_user_balance(self) -> json:
        """
        Get the authenticated user's balance of credits.

        :return: The users balance as a float.

        :raises: :class:`HTTPError` if an HTTP error occurrs.
        :raises: :class:`JSONDecodeError` if JSON decoding fails.
        """
        return float(self.get_text("api/resource/userbalance"))

    def debit_account(self, amount: int) -> json:
        """
        Debit the user's app store account.
        :param amount: The number of credits that should be debited from the user's account.

        :return: The transaction reference of the user's payment.

        :raises: :class:`HTTPError` if an HTTP error occurrs.
        :raises: :class:`JSONDecodeError` if JSON decoding fails.
        """
        params = {
            "debitAmount": amount
        }

        return self.post_json("api/resource/debit", params=params)

    def refund_account(self, transaction_ref: str) -> json:
        """
        Refund a transaction
        :param transaction_ref: The transaction reference of the transation you want to refund.

        :return: The requests response object.

        :raises: :class:`HTTPError` if an HTTP error occurrs.
        :raises: :class:`JSONDecodeError` if JSON decoding fails.
        """

        params = {
            "transactionRef": transaction_ref
        }

        return self.post("api/resource/refund", params=params)

    def refresh_session(self, app_id: str, app_secret: str):
        """
        Refresh the inustrial app store session using the refresh token.
        :param app_id: The ID of the app to authenticate under (found under Developer > Applications > Settings on the app store)
        :param app_secret: The secret of the app to authenticate under (found under Developer > Applications > Settings on the app store) :warn This should not be published.

        :return: A new instance of AppStoreClient with the refreshed access token.
        
        :raises: :class:`HTTPError` if an HTTP error occurrs.
        :raises: :class:`JSONDecodeError` if JSON decoding fails.
        """
        if self.refresh_token is None:
            raise ValueError("Cannot refresh. No refresh token specified.")

        path = "AuthorizationServer/OAuth/Token"
        url = urllib.parse.urljoin(self.base_url, path)
        r = requests.post(url, data = {"grant_type": "refresh_token", "refresh_token": self.refresh_token}, auth=requests.auth.HTTPBasicAuth(app_id, app_secret))

        r.raise_for_status()

        token_details = r.json()

        return token_details_to_client(token_details, self.base_url)
                    

def token_details_to_client(token_details: dict[str,str], base_url: str = "https://appstore.intelligentplant.com/") -> AppStoreClient:
    """
    Convert access token details as provided by the app store API into an AppStoreClient.
    :param token_details: The token details as requested from the API.
    :param base_url: The app store base url (optional, default value is "https://appstore.intelligentplant.com/")

    :return: An instance of AppStoreClient using the speicifed acccess token.
    """
    access_token = token_details['access_token']
    refresh_token = token_details.get('refresh_token', None)
    expires_in = float(token_details['expires_in'])

    return AppStoreClient(access_token, refresh_token, expires_in, base_url)

def get_authorization_code_grant_flow_url(app_id: str, redirect_uri: str, scopes: list[str], code_challenge: str = None, code_challenge_method: str = None, state: str = None, access_type: str = None, base_url: str = "https://appstore.intelligentplant.com/") -> str:
    """
    Get the url that the client should use for authorization code grant flow
    This grant flow should be used by web servers as it requires the app secret (which should not be made public).
    For information on the authorisation flow see: https://appstore.intelligentplant.com/wiki/doku.php?id=dev:app_store_developers
    :param app_id: The ID of the app to authenticate under (found under Developer > Applications > Settings on the app store)
    :param redirect_uri: The URI to redirect the user to after they log in with the authentication token (must be an authorized redirect URI in the app developer settings)
    :param code_challenge: A PKCE code challenge. This should be generated from the verifier using sha256. A challenge verifier pair can be generated with the pkce package.
    :param code_challenge_method: The method used to generate the code challenge from the code verifier, should be 'plain' or 'S256' for sha256 (recommended).
    :param scopes: A list of string that are the scopes the user is granting (e.g. "UserInfo" and "DataRead")
    :param state: The OAuth state parameter. This can be used to prevent cross site request forgery or track application state (Optional).
    :param access_type: Set the access type to "offline" to enable refresh tokens (Optional).
    :param base_url: The app store base url (optional, default value is "https://appstore.intelligentplant.com/")

    :return: The URL that the user should be redirected to to log in.
    """
    params = {
        'response_type': "code",
        'client_id': app_id,
        'redirect_uri': redirect_uri,
        'scope': " ".join(scopes)
    }

    if code_challenge is not None:
        assert not code_challenge_method is None, 'code_challenge_method must be specified if code_challenge is specified'

        params['code_challenge'] = code_challenge
        params['code_challenge_method'] = code_challenge_method

    if state is not None:
        params['state'] = state

    if access_type is not None:
        params["access_type"] = access_type
        
    url = base_url + "authorizationserver/oauth/authorize?" + urllib.parse.urlencode(params)

    return url

def complete_authorization_code_grant_flow(auth_code: str, app_id: str, app_secret: str, redirect_uri: str, code_verifier: str = None, base_url: str = "https://appstore.intelligentplant.com/") -> AppStoreClient:
    """
    Complete logging in the user using authroization grant flow
    This grant flow should be used by web servers as it requires the app secret (which should not be made public).
    For information on the authorisation flow see: https://appstore.intelligentplant.com/wiki/doku.php?id=dev:app_store_developers
    :param auth_code: The code that was returned to the redirect URI after the user logged in.
    :param app_id: The ID of the app to authenticate under (found under Developer > Applications > Settings on the app store)
    :param app_secret: The secret of the app to authenticate under (found under Developer > Applications > Settings on the app store). If no secret is registered in app store, this can be set to `None` as long as the PKCE extension is used. :warn This should not be published.
    :param redirect_uri: An authorized redirect URI in the app developer settings
    :param code_verifier: The code verifier that was used to generate the code_challenge in the first step of the flow

    :param base_url: The app store base url (optional, default value is "https://appstore.intelligentplant.com/")

    :return: An app store client with the access token specified
    """
    url = base_url + "authorizationserver/oauth/token"

    params = {
        'grant_type': "authorization_code",
        'code': auth_code,
        'client_id': app_id,
        'redirect_uri': redirect_uri
    }

    if app_secret is not None:
        params['client_secret'] = app_secret

    if code_verifier is not None:
        params['code_verifier'] = code_verifier
    
    r = requests.post(url, params)

    r.raise_for_status()

    token_details = r.json()

    return token_details_to_client(token_details, base_url)
  
def get_implicit_grant_flow_url(app_id: str, redirect_url: str, scopes: list[str], state: str = None, base_url: str = "https://appstore.intelligentplant.com/") -> str:
    """
    Get the url that the client should use for implicit grant flow.
    This grant flow can be used by native applications and clients, as it doesn't require the app secret.
    For security reasons the PKCE grant flow is recommended over the implicit grant flow.
    For information on the authorisation flow see: https://appstore.intelligentplant.com/wiki/doku.php?id=dev:app_store_developers
    :param app_id: The ID of the app to authenticate under (found under Developer > Applications > Settings on the app store)
    :param redirect_url: The URL to redirect the user to after they log in with the access token (must be an authorized redirect URI in the app developer settings)
    :param scopes: A list of string that are the scopes the user is granting (e.g. "UserInfo" and "DataRead")
    :param state: The OAuth state parameter. This can be used to prevent cross site request forgery or track application state (Optional).

    :param base_url: The app store base url (optional, default value is "https://appstore.intelligentplant.com")

    :return: The URL that the user should be redirected to to log in.
    """
    params = {
        'response_type': "token",
        'client_id': app_id,
        'redirect_uri': redirect_url,
        'scope': " ".join(scopes)
    }

    if state is not None:
        params['state'] = state

    url = base_url + "authorizationserver/oauth/authorize?" + urllib.parse.urlencode(params)

    return url

def begin_device_code_flow(app_id: str, app_secret: str = None, scopes: list[str] = None, base_url: str = "https://appstore.intelligentplant.com/") -> json:
    """
    Begin the device code OAuth flow. This will return with the device code, user code and validation URI to allow the user to log in to the app store.
    :param app_id: The ID of the app to authenticate under (found under Developer > Applications > Settings on the app store)
    :param app_secret: The secret of the app to authenticate under (found under Developer > Applications > Settings on the app store) :warn This should not be published.
    :param scopes: A list of string that are the scopes the user is granting (e.g. "UserInfo" and "DataRead")
    :param base_url: The app store base url (optional, default value is "https://appstore.intelligentplant.com")

    :return: An object containing the device code, user code, validation URI and polling interval for this instance of the device code flow.
    
    :raises: :class:`HTTPError` if an HTTP error occurrs.
    :raises: :class:`JSONDecodeError` if JSON decoding fails.
    """
    url = base_url + "authorizationserver/oauth/authorizedevice"

    body = {
        'client_id': app_id,
    }

    if app_secret is not None:
        body['client_secret'] = app_secret

    if scopes is not None:
        body['scope'] = " ".join(scopes)
    
    r = requests.post(url, data=body)

    r.raise_for_status()

    return r.json()

def fetch_device_token(app_id: str, device_code: str, app_secret: str = None, base_url: str = "https://appstore.intelligentplant.com/") -> json:
    """
    Make a request to the token endpoint to see if the user has completed the device code flow.
    :param app_id: The ID of the app to authenticate under (found under Developer > Applications > Settings on the app store)
    :param device_code: The device code specified in the reponse of begin_device_code_flow(..)
    :param app_secret: The secret of the app to authenticate under (found under Developer > Applications > Settings on the app store) :warn This should not be published.
    
    :param base_url: The app store base url (optional, default value is "https://appstore.intelligentplant.com")

    :return: The access token details (if the user has completed the flow) or an error object indicating that we are still waiting or why the flow has failed.
    
    :raises: :class:`HTTPError` if an HTTP error occurrs.
    :raises: :class:`JSONDecodeError` if JSON decoding fails.
    """
    url = base_url + "authorizationserver/oauth/token"

    body = {
        'client_id': app_id,
        'device_code': device_code,
        'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'
    }

    if app_secret is not None:
        body['client_secret'] = app_secret

    r = requests.post(url, data=body)

    return r.json()


class DeviceCodeFlowError(Exception):
    def __init__(self, error, error_detail):
        super().__init__(f'{error}: {error_detail}')

def poll_device_token(app_id: str, device_code: str, interval: int = 5, app_secret: str = None,  base_url: str = "https://appstore.intelligentplant.com/") -> AppStoreClient:
    """
    Repeatadly poll the token endpoint until the flow is complete or an unrecoverable error occurs.
    :param app_id: The ID of the app to authenticate under (found under Developer > Applications > Settings on the app store)
    :param device_code: The device code specified in the reponse of begin_device_code_flow(..)
    :param interval: The polling interval specified in the reponse of begin_device_code_flow(..)
    :param app_secret: The secret of the app to authenticate under (found under Developer > Applications > Settings on the app store) :warn This should not be published.
    
    :param base_url: The app store base url (optional, default value is "https://appstore.intelligentplant.com")

    :return: The logged in app store client.
    
    :raises: :class:`DeviceCodeFlowError` if an unrecoverable error occurs with the flow.
    :raises: :class:`HTTPError` if an HTTP error occurrs.
    :raises: :class:`JSONDecodeError` if JSON decoding fails.
    """
    while True:
        time.sleep(interval)
        token_response = fetch_device_token(app_id, device_code, app_secret=app_secret, base_url=base_url)

        if 'error' in token_response:
            # an error occurred
            if token_response['error'] == 'access_denied' or token_response['error'] == 'expired_token':
                raise DeviceCodeFlowError(token_response['error'], token_response.get('error_description', 'Unspecified'))
            
            # in other cases we keep polling
            # TODO suport the 'slow_down' error
        else:
            #this should be the token details
            return token_details_to_client(token_response, base_url)