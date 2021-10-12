#!/usr/bin/env python3
#
# INTEL CONFIDENTIAL
#
# Copyright 2021 (c) Intel Corporation.
#
# This software and the related documents are Intel copyrighted materials, and
# your use of them  is governed by the  express license under which  they were
# provided to you ("License"). Unless the License provides otherwise, you  may
# not  use,  modify,  copy, publish,  distribute,  disclose  or transmit  this
# software or the related documents without Intel"s prior written permission.
#
# This software and the related documents are provided as is, with no  express
# or implied  warranties, other  than those  that are  expressly stated in the
# License.
#
# ----------------------------------------------------------------------------

import logging
import os

import yaml


class YAMLParserError(Exception):
    """
    Class for YML parser exceptions
    """
    pass


class YAMLParser(object):
    """
    YAML file parser

    """

    def __init__(self, path: str = "GenVT.yml", mode: str = "breakpoint_serial"):
        """
        Init YAML parser with file path and WLC command. Default is breakpoint_serial
        :param path: YML file path, default is wlc_config.yml
        :param mode: WLC command, default is breakpoint_serial
        """
        self._path = path
        self._mode = mode

    def parse(self):
        """
        Parse, load YML file
        :return: parsed file as a dictionary
        """
        if not self._path or not os.path.isfile(self._path):
            raise YAMLParserError(f"File {self._path} does not exist!")

        data = yaml.load(open(self._path), Loader=yaml.Loader)

        if YAMLParser.check_exists(self._mode, data):
            logging.info(f"Runner YML file {self._path} loaded, will run in mode:{self._mode}")

        return data

    @staticmethod
    def check_exists(key, dictionary):
        """
        Check if given key exists in the given dictionary
        :param key: input key string
        :param dictionary: input dictionary
        :return: true if present, else raise exception
        """
        if key not in dictionary:
            raise YAMLParserError(f"Key {key} not found!")
        return True

    @staticmethod
    def get(key, dictionary):
        """
        Get key value from input dictionary
        :param key: input key string
        :param dictionary: input dictionary
        :return: value of key if present, else raise exception
        """
        if not YAMLParser.check_exists(key, dictionary):
            raise YAMLParserError(f"{key} - Key/Value error. Please check YML file")

        return dictionary[key]

    @staticmethod
    def pretty_print(data):
        """
        Print formatted dictionary
        :param data: input dictionary
        :return: formatted dictionary
        """
        return yaml.dump(data)
