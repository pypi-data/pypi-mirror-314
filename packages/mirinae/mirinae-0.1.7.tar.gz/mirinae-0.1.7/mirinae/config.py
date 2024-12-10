#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2024- MAGO
# AUTHORS:
# Sukbong Kwon (Galois)

# 환경변수를 가져옵니다. ('ENDPOINT' 라는 이름으로)
import os
ENDPOINT = os.getenv("ENDPOINT")


if ENDPOINT == "snu3":
    FRAMEWORK_ENDPOINT = "http://snu3.mago52.com:8506/v1/go"       # wawa 개발 환경
elif ENDPOINT == "m3":
    FRAMEWORK_ENDPOINT = "http://audion.mago52.com:8506/v1/go"     # Audion
elif ENDPOINT == "snu1":
    FRAMEWORK_ENDPOINT = "http://dev.mago52.com:8506/v1/go"     # Audion
else:
    FRAMEWORK_ENDPOINT = "http://localhost:8506/v1/go"

HEADERS = {
    "Accept": "application/json",
    "Authorization": "Bearer eadc5d8d-ahno-9559-yesa-8c053e0f1f69",
}
