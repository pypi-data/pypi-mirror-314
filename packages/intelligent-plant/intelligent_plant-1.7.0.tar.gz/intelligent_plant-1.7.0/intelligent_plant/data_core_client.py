"""This module implments a client for the Intelligent Plant Data Core API"""
__author__ = "Ross Kelso"
__docformat__ = 'reStructuredText'

import urllib.parse as urlparse
from datetime import datetime


import intelligent_plant.http_client as http_client
from intelligent_plant.type_handler import json, time_stamp, tag_map, format_time_stamp


def normalise_tag_map(tags):
    for entry in tags.items():
        if isinstance(entry[1], str):
            tags[entry[0]] = [entry[1]]

    return tags


class DataCoreClient(http_client.HttpClient):
    """Access the Intelligent Plant Data Core API"""

    def __init__(self, base_url: str = "https://api.intelligentplant.com/datacore/", **kwargs):
        """
        Initialise a data core client with the specified authoriation haeder value and base URL.
        It is recommended that you use AppStoreClient.get_data_core_client(..) rather than calling this directly.

        :param authorization_header: The authorization header that will be used for all requests.
        :param base_url: The base URL to make requests from. The default value is "https://api.intelligentplant.com/datacore/" (the app store data api)
        """
        super().__init__(base_url, **kwargs)
    
    def get_data_sources(self) -> json:
        """
        Get the list of available data sources

        :return: The available data sources as a parsed JSON object.

        :raises: :class:`HTTPError` if an HTTP error occurrs.
        :raises: :class:`JSONDecodeError` if JSON decoding fails.
        """
        params = {}
        
        return self.get_json('api/data/datasources', params)

    def get_tags(self, dsn: str, page: int = 1, page_size: int = 20, filters: dict = {}) -> json:
        """
        Search the provided data source fo tags.

        :param dsn: The fully qualified name of the data source. seealso::get_data_sources
        :param page: The number of the current page of results. Default: 1.
        :param page_size: The number of results to return on a page. Default: 20.
        :param filters: A dictionary of filters where the key is the field name (e.g. name, description, unit)
            and the value is the filter to apply.

        :return: The available tags as a parsed JSON object.

        :raises: :class:`HTTPError` if an HTTP error occurrs.
        :raises: :class:`JSONDecodeError` if JSON decoding fails.
        """
        params = filters.copy()
        params["page"] = page
        params["pageSize"] = page_size
        
        return self.get_json(urlparse.urljoin('api/data/tags/', dsn), params)

    def get_snapshot_data(self, tags: tag_map) -> json:
        """
        Get the snapshot values of the provided tags.

        :param tags: A dictionary where the keys are the fully qualified data source names and the values are lists of tags.

        :return: A dictionary of data source names, containg dictionarys of tag names whos values are tag values.

        :raises: :class:`HTTPError` if an HTTP error occurrs.
        :raises: :class:`JSONDecodeError` if JSON decoding fails.
        """
        return self.post_json('api/data/v2/snapshot', json={"tags": normalise_tag_map(tags)})

    def get_raw_data(self, tags: tag_map, start_time: time_stamp, end_time: time_stamp, point_count: int) -> json:
        """
        Get raw data for the provided tags.

        :param tags: A dictionary where the keys are the fully qualified data source names and the values are lists of tags.
        :param start_time: The absolute or relative quiery start time.
        :param end_time: The absolute or relative quiery end time.
        :param point_count: The maximum number of point to return. Set to 0 for as many as possible.

        :return: A dictionary of data source names, containg dictionarys of tag names whos values are historical tag values.

        :raises: :class:`HTTPError` if an HTTP error occurrs.
        :raises: :class:`JSONDecodeError` if JSON decoding fails.
        """
        req = {
            "tags": normalise_tag_map(tags),
            "startTime": format_time_stamp(start_time),
            "endTime": format_time_stamp(end_time),
            "pointCount": point_count
        }

        return self.post_json('api/data/v2/raw', json=req)

    def get_plot_data(self, tags: tag_map, start_time: time_stamp, end_time: time_stamp, intervals: int) -> json:
        """
        Get raw data for the provided tags.

        :param tags: A dictionary where the keys are the fully qualified data source names and the values are lists of tags.
        :param start_time: The absolute or relative quiery start time.
        :param end_time: The absolute or relative quiery end time.
        :param intervals: How many intervals to divide the rtequest range into. Must be greater than 0

        :return: A dictionary of data source names, containg dictionarys of tag names whos values are historical tag values.

        :raises: :class:`HTTPError` if an HTTP error occurrs.
        :raises: :class:`JSONDecodeError` if JSON decoding fails.
        """
        req = {
            "tags": normalise_tag_map(tags),
            "startTime": format_time_stamp(start_time),
            "endTime": format_time_stamp(end_time),
            "intervals": intervals
        }

        return self.post_json('api/data/v2/plot', json=req)

    def get_processed_data(self, tags: tag_map, start_time: time_stamp, end_time: time_stamp, sample_interval: str, data_function: str) -> json:
        """
        Get processed data for the provided tags.

        :param tags: A dictionary where the keys are the fully qualified data source names and the values are lists of tags.
        :param start_time: The absolute or relative quiery start time.
        :param end_time: The absolute or relative quiery end time.
        :param sample_interval: The length of a sample interval
        :param data_function: The data function to use. Normal values are "interp", "avg", "min" and "max"

        :return: A dictionary of data source names, containg dictionarys of tag names whos values are historical tag values.

        :raises: :class:`HTTPError` if an HTTP error occurrs.
        :raises: :class:`JSONDecodeError` if JSON decoding fails.
        """
        req = {
            "tags": normalise_tag_map(tags),
            "startTime": format_time_stamp(start_time),
            "endTime": format_time_stamp(end_time),
            "sampleInterval": sample_interval,
            "dataFunction": data_function
        }

        return self.post_json('api/data/v2/processed', json=req)

    def get_data_at_times(self, tags: tag_map, utc_sample_times: list[time_stamp]) -> json:
        """
        Get the value of the provided tags at the specified times.

        :param tags: A dictionary where the keys are the fully qualified data source names and the values are lists of tags.
        :param utc_sample_times: The time stamps to retrieve the values for,

        :return: A dictionary of data source names, containg dictionarys of tag names whos values are historical tag values.

        :raises: :class:`HTTPError` if an HTTP error occurrs.
        :raises: :class:`JSONDecodeError` if JSON decoding fails.
        """
        req = {
            "tags": normalise_tag_map(tags),
            "utcSampleTimes": list(map(format_time_stamp, utc_sample_times))
        }

        return self.post_json('api/data/v2/history-at-times', json=req)

    def write_snapshot_values(self, dsn: str, values: list[dict]) -> json:
        """
        Write a set of tag values into the specified datasource.

        :param dsn: The data source name the values are to be written to.
        :param values: A list of TagValue Objects that specifiy the values and the time stamps they are to be written at.

        :return: A dictionary of tag names, containg dictionarys of Write Results detailing the success of the write.

        :raises: :class:`HTTPError` if an HTTP error occurrs.
        :raises: :class:`JSONDecodeError` if JSON decoding fails.
        """

        return self.put_json(urlparse.urljoin('api/data/v2/snapshot/', dsn), json=values)

    def write_historical_values(self, dsn: str, values: list[dict]) -> json:
        """
        Write a set of tag values into the specified datasource.
        :param dsn: The data source name the values are to be written to.
        :param values: A list of TagValue Objects that specifiy the values and the time stamps they are to be written at.

        :return: A dictionary of tag names, containg dictionarys of Write Results detailing the success of the write.

        :raises: :class:`HTTPError` if an HTTP error occurrs.
        :raises: :class:`JSONDecodeError` if JSON decoding fails.
        """

        return self.put_json(urlparse.urljoin('api/data/v2/history/', dsn), json=values)

    def create_tag(self, dsn: str, tag_definition: dict) -> json:
        """
        Create a new tag in the specified data source.
        :param dsn: The data source name where the new tag should be created.
        :param tag_definition: A tag definition object defining tag properties. This will be data source specific.

        :return: The tag definition object as created in the data source.

        :raises: :class:`HTTPError` if an HTTP error occurrs.
        :raises: :class:`JSONDecodeError` if JSON decoding fails.
        """
        return self.put_json(urlparse.urljoin('api/configuration/tags/', dsn), json=tag_definition)
    
    def get_annotations(self, dsn: str, tags: list[str], start_time: time_stamp, end_time: time_stamp) -> json:
        """
        Get annotations for the specifed tags on the specified data source within the time range.
        :param dsn: The data source to query for annotations.
        :param tags: A list of tags to request annotations for.
        :param start_time: The start of the time range to query for.
        :param end_time: The end of the time range to query for.

        :return: The annotations matching the spcified query parameters.

        :raises: :class:`HTTPError` if an HTTP error occurrs.
        :raises: :class:`JSONDecodeError` if JSON decoding fails.
        """
        annotation_request = {
            'dsn': dsn,
            'tags': tags,
            'start': format_time_stamp(start_time),
            'end': format_time_stamp(end_time)
        }
        return self.post_json('api/data/annotations/', json=annotation_request)
    
    def write_annotation(self, dsn: str, annotation: dict) -> json:
        """
        Write an annotation to a data source.
        :param dsn: The data source name where the new annotation should be created.
        :param annotation: The annotation object.

        :return: The annotation as saved to the data source. Additional fields will be populated by data core.

        :raises: :class:`HTTPError` if an HTTP error occurrs.
        :raises: :class:`JSONDecodeError` if JSON decoding fails.
        """
        return self.post_json(urlparse.urljoin('api/data/annotations/', dsn), json=annotation)

    def update_annotation(self, dsn: str, annotation: dict) -> json:
        """
        Update an annotation on the data source.
        :param dsn: The data source name where the new annotation should be created.
        :param annotation: The updated annotation object.

        :raises: :class:`HTTPError` if an HTTP error occurrs.
        """
        self.put(urlparse.urljoin('api/data/annotations/', dsn), json=annotation)
