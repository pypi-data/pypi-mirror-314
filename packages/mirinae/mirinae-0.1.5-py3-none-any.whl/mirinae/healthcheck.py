#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2024- MAGO
# AUTHORS:
# Sukbong Kwon (Galois)

import json
import requests
from typing import Text, Dict
from config import (
    FRAMEWORK_ENDPOINT,
    HEADERS,
)
from utils.show import show_response

def healthcheck() -> Dict[Text, Text]:
    url = f"{FRAMEWORK_ENDPOINT}/"
    response = requests.get(url, headers=HEADERS)
    show_response('HealthCheck', url, response)


def get_info() -> Dict[Text, Text]:
    url = f"{FRAMEWORK_ENDPOINT}/info"
    response = requests.get(url, headers=HEADERS)
    show_response('Info', url, response)


def test():
    url = f"{FRAMEWORK_ENDPOINT}/test"
    response = requests.get(url, headers=HEADERS)
    show_response('Test', url, response)



<<<<<<< HEAD
#healthcheck()
=======
# healthcheck()
>>>>>>> develop
get_info()
# test()
