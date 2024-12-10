#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2024- MAGO
# AUTHORS:
# Sukbong Kwon (Galois)

import json
from typing import Text, Any, Dict

def show_response(
    title: Text,
    url: Text,
    response: Any,
):
    print ("=" * 100)
    print (f"Title: {title}")
    print (f"URL: {url}")
    print (f"Status Code: {response.status_code}")
    print ("Response:")
    # Show the content in the response
    # print(response.__dict__)

    try:
        print (json.dumps(response.json(), indent=4, ensure_ascii=False))
    except:
        print ("\t", response.text)
        # content = response.__dict__.get('_content')
        # if type(content) == bytes:
        #     print (content.decode('utf-8'))
        # else:
        #     json_data = json.loads(response.__dict__.get('_content').decode('utf-8'))
        #     print (json.dumps(json_data), indent=4, ensure_ascii=False)

    print ("=" * 100)


def show_status(
    title: Text,
    response,
)-> None:
    if response:
        # Check the status code
        if response.status_code == 200:
            print (f"[{title}] Success")
        else:
            print (f"[{title}] {response.json()}")
    else:
        print (f"[{title}] {response.json()}")



