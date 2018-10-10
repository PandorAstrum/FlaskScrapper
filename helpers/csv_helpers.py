# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "file to execute various csv related operations"
"""
import csv

__all__ = [
    'readCSV',
    'writeCSV',
]

def readCSV(_filename, _columnName):
    """
    functions to read csv file
    :param _filename: a given file with the extension csv
    :param _columnName: string name of the column to read
    :return: a list
    """
    _list = []
    with open(_filename, 'r') as csvFile:
        r = csv.DictReader(csvFile)
        for row in r:
            _list.append(row[_columnName])
    return _list

def writeCSV(_filename, _dict_list, _dict_tuple, _dict_tuple_with_header, _path):
    """
        Function for creating a csv file with the provided dictionary list
        :param filename:
        :param _dict_list: list of dictionary
        :param _dict_tuple: tuple of dictionary
        :param _dict_tuple_with_header: tuple of dictionary with named keys
        :return:
    """
    final_out_file = _path + "\\" + filename
    with open(final_out_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = list(_dict_tuple)[0]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in _dict_tuple_with_header:
            writer.writerow(dict(zip(fieldnames, row)))