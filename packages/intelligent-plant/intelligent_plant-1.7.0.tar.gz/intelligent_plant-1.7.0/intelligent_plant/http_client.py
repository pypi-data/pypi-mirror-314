"""This module implments a generic HTTP client and is used as the base of the App Store and Data Core clients"""
__author__ = "Ross Kelso"
__docformat__ = 'reStructuredText'

import urllib.parse as urlparse

import requests
from requests import Response

from intelligent_plant.type_handler import json, post_data

class HttpClient(object):
    """A base HTTP client that has an authorization header and base url"""

    def __init__(self, base_url: str, **kwargs):
        """
        Initialise this HTTP client with an authorization header and base url.

        :param authorization_header: The value of the 'Authorization' HTTP header that should be sent with each request.
        :param base_url: The URL that relative URLs should be appended to.
        :type authorization_header: string
        :type base_url: string
        """
        self.base_url = base_url

        self.session = requests.Session()

        if ("authorization_header" in kwargs):
            self.session.headers = { 'Authorization': kwargs["authorization_header"] }

        if ("auth" in kwargs):
            self.session.auth = kwargs["auth"]

    def get(self, path: str, params: dict[str,str]) -> Response:
        """
        Make a GET request to the specified path (relative to the client base url), with the specified parameters
        :param path: The path to the target endpoint.
        :param params: The query string parameters as a dictionary with the parameter name as the key
        :type path: string
        :type params: dict

        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        :raises: :class:`HTTPError`, if one occurred.
        """
        url = urlparse.urljoin(self.base_url, path)
        r = self.session.get(url, params=params)

        r.raise_for_status()

        return r


    def post(self, path: str, params: dict[str,str] = None, data: post_data = None, json: json = None) -> Response:
        """
        Make a POST request to the specified path (relative to the client base url), with the specified parameters
        :param path: The path to the target endpoint.
        :param params: The query string parameters as a dictionary with the parameter name as the key
        :param data: The data to be included in the request body.
        :type path: string
        :type params: dict

        :return: :class:`Response <Response>` object
        :rtype: requests.Response

        :raises: :class:`HTTPError`, if one occurred.
        """
        url = urlparse.urljoin(self.base_url, path)
        r = self.session.post(url, data=data, params=params, json=json)

        r.raise_for_status()

        return r

    def put(self, path: str, params: dict[str,str] = None, data: post_data = None, json: json = None) -> Response:
        """
        Make a PUT request to the specified path (relative to the client base url), with the specified parameters
        :param path: The path to the target endpoint.
        :param params: The query string parameters as a dictionary with the parameter name as the key
        :param data: The data to be included in the request body.
        :type path: string
        :type params: dict

        :return: :class:`Response <Response>` object
        :rtype: requests.Response

        :raises: :class:`HTTPError`, if one occurred.
        """

        url = urlparse.urljoin(self.base_url, path)
        r = self.session.put(url, data=data, params=params, json=json)

        r.raise_for_status()

        return r

    def get_json(self, path: str, params: dict[str,str] = None) -> json:
        """
        Make a GET request to the specified path (relative to the client base url), with the specified parameters
        This method additionally parses the JSON response object.
        :param path: The path to the target endpoint.
        :param params: The query string parameters as a dictionary with the parameter name as the key.
        :type path: string
        :type params: dict

        :return: The parsed JSON response object.

        :raises: :class:`HTTPError` if an HTTP error occurrs.
        :raises: :class:`JSONDecodeError` if JSON decoding fails.
        """
        return self.get(path, params).json()

    def get_text(self, path: str, params: dict[str,str] = None) -> str:
        """
        Make a GET request to the specified path (relative to the client base url), with the specified parameters
        This method returns the text content of the response body.
        :param path: The path to the target endpoint.
        :param params: The query string parameters as a dictionary with the parameter name as the key.
        :type path: string
        :type params: dict

        :return: The conetent body as text.
        :raises: :class:`HTTPError`, if one occurred.
        """
        return self.get(path, params).text

    def post_text(self, path: str, params: dict[str,str] = None, data: post_data = None) -> str:
        """
        Make a POST request to the specified path (relative to the client base url), with the specified parameters
        This method returns the response content as text
        :param path: The path to the target endpoint.
        :param params: The query string parameters as a dictionary with the parameter name as the key
        :param data: The data to be included in the request body.
        :type path: string
        :type params: dict

        :return: The resposne body content as text
        :raises: :class:`HTTPError`, if one occurred.
        """
        return self.post(path, params=params, data=data).text

    def post_json(self, path: str, params: dict[str,str] = None, data: post_data = None, json: json = None) -> json:
        """
        Make a POST request to the specified path (relative to the client base url), with the specified parameters
        This method returns parses the reponse body as JSON.
        :param path: The path to the target endpoint.
        :param params: The query string parameters as a dictionary with the parameter name as the key
        :param data: The data to be included in the request body.
        :type path: string
        :type params: dict

        :return: The parsed response JSON object

        :raises: :class:`HTTPError` if an HTTP error occurrs.
        :raises: :class:`JSONDecodeError` if JSON decoding fails.
        """
        return self.post(path, params=params, data=data, json=json).json()

    def put_json(self, path: str, params: dict[str,str] = None, data: post_data = None, json: json = None) -> json:
        """
        Make a PUT request to the specified path (relative to the client base url), with the specified parameters
        This method returns parses the reponse body as JSON.
        :param path: The path to the target endpoint.
        :param params: The query string parameters as a dictionary with the parameter name as the key
        :param data: The data to be included in the request body.
        :type path: string
        :type params: dict

        :return: The parsed response JSON object

        :raises: :class:`HTTPError` if an HTTP error occurrs.
        :raises: :class:`JSONDecodeError` if JSON decoding fails.
        """
        return self.put(path, params=params, data=data, json=json).json()