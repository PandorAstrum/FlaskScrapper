# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Generic files to help in various task"
"""
import json
from datetime import datetime
from bson import ObjectId
from werkzeug.routing import BaseConverter

__all__ = [
    "get_curr_date_time",
    "get_outputFile",
    "allowed_file",
    "ListConverter",
    "JSONEncoder",
    "SCRAPE_COMPLETE",
]

SCRAPPING_INPROGRESS = False            # flag for if scrapping started or not
SCRAPE_COMPLETE = False                 # flag for if entire scrapping done or not
ALLOWED_EXTENSIONS = set(['csv'])

def get_curr_date_time(_strft="%Y_%b_%d_%H.%M.%S"):
    """
    functions for getting current time
    :param strft: format to use on time
    :return: datetime now with provided format
    """
    return datetime.now().strftime(_strft)

def get_outputFile(_extension="csv"):
    """
    functions to get filename
    :param _extension: extension of the file name
    :return: a string
    """
    return f"{get_curr_date_time()}.{_extension}"

def allowed_file(_filename):
    """
    functions to set allowed file in upload
    :param _filename: string filename
    :return: string of allowed file name
    """
    return '.' in _filename and _filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class JSONEncoder(json.JSONEncoder):
    """
    helps to encode mongo nested collections to json
    """
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

class ListConverter(BaseConverter):
    """
    custom list argument parser for route
    """
    def to_python(self, value):
        return value.split('+')

    def to_url(self, values):

        return '+'.join(BaseConverter.to_url(self, value)
                        for value in values)