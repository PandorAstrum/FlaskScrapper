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
    "ListConverter",
    "JSONEncoder",
    "SCRAPPING_LIKERS",
    "SCRAPPING_COMMENTERS",
    "SCRAPPING_LIKERS_LIKE",
    "SCRAPPING_COMMENTERS_LIKE",
    "SCRAPE_COMPLETE",
    "LIKERS_NAME",
    "LIKERS_PROFILE",
    "LIKERS_LIKE",
    "COMMENTERS_NAME",
    "COMMENTERS_PROFILE",
    "COMMENTERS_LIKE"
]

SCRAPPING_INPROGRESS = False            # flag for if scrapping started or not
SCRAPPING_LIKERS = False                # flag for if likers scrapping done or not
SCRAPPING_COMMENTERS = False            # flag for if commenters scrapping done or not
SCRAPPING_LIKERS_LIKE = False           # flag for if likers like scrapping done or not
SCRAPPING_COMMENTERS_LIKE = False       # flag for if commenters like scrapping done or not
SCRAPE_COMPLETE = False                 # flag for if entire scrapping done or not
LIKERS_NAME = []
LIKERS_PROFILE = []
LIKERS_LIKE = []
COMMENTERS_NAME = []
COMMENTERS_PROFILE = []
COMMENTERS_LIKE = []

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

TEST_JSON_DUMPS = { "job1":
    {
        "id": 1,
        "postLink": "https://facebook.com",
        "Likers":{
            "Name":[],
            "profileLink":[],
            "like":[]
        },
        "Commenters": {
            "Name":[],
            "profileLink":[],
            "like":[]
        },
        "dateStamp": "22/03/2018"
    }
}

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class ListConverter(BaseConverter):

    def to_python(self, value):
        return value.split('+')

    def to_url(self, values):

        return '+'.join(BaseConverter.to_url(self, value)
                        for value in values)