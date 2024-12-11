"""This module implments utility functions for interacting with IP Hist"""
__author__ = "Ross Kelso"
__docformat__ = 'reStructuredText'

from intelligent_plant.utility import construct_tag_definition_property


def construct_ip_hist_tag_properties(compression_type: str = 'percent', exception_deviation: float = 2, compression_deviation: float = 8, resample_limit: int = 8640000, 
        interface_archiving_enabled: bool = False, interface_dsn: str = None, interface_tag: str = None, is_digital: bool = False, prefer_stepped_visualization: bool = False, record_history: bool = True):
    """Construct tag defintion property objects needed to create a tag in IP Hist.
    Usage: data_core.create_tag(dsn, utility.construct_tag_definition('tag-name', properties=ip_hist.construct_ip_hist_tag_properties()))

    :param compression_type: The type of compression to use. 'percent' or 'absolute'. Default value 'percent'.
    :param exception_deviation: The amount an incoming sample must deviate from the last archived value to pass the exception filter. Default: 2
    :param compression_deviation: Specifies the change in gradient that needs to be exceded to pass the compression filter, in terms of deviation from the snapshot value. Default: 8
    :param resample_limit: The maximum difference in timestamp in milliseconds between the last archived value and the current value being ingested before a guaranteeing an archive write. Default: 8640000
    :param interface_archiving_enabled: Whether this tag is automaticlly recorded from another data source.Default: False
    :param interface_dsn: The name of the source data source this tag is being archived from. Only used if interface_archiving_enabled is set.
    :param interface_tag: The name of the source tag in the data source this tag is being archived from. Only used if interface_archiving_enabled is set.
    :param is_digital: Whether this tag is a digital state. Default: False.
    :param prefer_stepped_visualization: Whether this tag prefers stepped visualisation. Default: False.
    :param record_history: Whether this tag should record history. Default: True.


    :return: A tag definition property dictionary.
    """
    return {
        'CompressionType': construct_tag_definition_property('CompressionType', compression_type),
        'ExceptionDeviation': construct_tag_definition_property('ExceptionDeviation', exception_deviation),
        'CompressionDeviation': construct_tag_definition_property('CompressionDeviation', compression_deviation),
        'ResampleLimit': construct_tag_definition_property('ResampleLimit', resample_limit),
        'InterfaceArchivingEnabled': construct_tag_definition_property('InterfaceArchivingEnabled', interface_archiving_enabled),
        'InterfaceDsn': construct_tag_definition_property('InterfaceDsn', interface_dsn),
        'InterfaceTag': construct_tag_definition_property('InterfaceTag', interface_tag),
        'IsDigital': construct_tag_definition_property('IsDigital', is_digital),
        'PreferSteppedVisualization': construct_tag_definition_property('PreferSteppedVisualization', prefer_stepped_visualization),
        'RecordHistory': construct_tag_definition_property('RecordHistory', record_history)
    }
