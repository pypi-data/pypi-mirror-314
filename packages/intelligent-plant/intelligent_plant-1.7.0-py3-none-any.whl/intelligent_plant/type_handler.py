"""This module defines types used by the Industrial App Store API"""
__author__ = "Ross Kelso"
__docformat__ = 'reStructuredText'


from datetime import datetime

# the definition of the tag map type
# keys should be data source names, values lists of tags to query on that data source
tag_map = type[dict[str,list[str]]]

# define type for json response objects, which are either and object (dict) or array (list)
json = type[dict[str]|list]

# types of data that can be posted that aren't json
post_data = type[dict[str,str] | list[tuple[str,str]] | bytes]

# define time_stamp type as string for relative times and datetime for absolute times
time_stamp = type[str|datetime]

def format_time_stamp(time_stamp: time_stamp) -> str:
    """
    Format a time stamp as an ISO date if possible.

    :param time_stamp: The time stampt to format.

    :return: The time stamp as an ISO format string or the original timestamp.
    """
    try:
        return time_stamp.isoformat()
    except:
        return time_stamp
