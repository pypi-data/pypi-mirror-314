#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2024- MAGO
# AUTHORS:
# Sukbong Kwon (Galois)

import json
from typing import Text, Dict
from pathlib import Path
from ..config import HEADERS

# Set the session path under the user's home directory
session_path = f"{Path.home()}/.mirinae/session.json"

def get_session_headers(
    session_path: Text,
)-> Dict:
    """세션 데이터 헤더 가져오기

    Parameters
    ----------
    session_path: Text
        세션 데이터 파일 경로

    Returns
    -------
    Dict
        세션 데이터 헤더
    """
    if not Path(session_path).exists():
        raise ValueError('Session data is required')

    with open(session_path, 'r') as f:
        sess_data = json.load(f)

    headers = {
        'Cookie': '; '.join([f'{key}={value}' for key, value in sess_data.items()])
    }
    headers.update(HEADERS)

    return headers
