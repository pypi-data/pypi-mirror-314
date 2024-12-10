#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2024- SATURN
# AUTHORS
# Sukbong Kwon (Galois)

"""
파스칼 표기법 (PascalCase):

	- 각 단어의 첫 글자를 대문자로 쓰며, 첫 번째 단어도 대문자로 시작합니다.
	- 예: VoiceSeparation, MyVariableName, TotalCount
	- 클래스 이름이나 타입 이름에 자주 사용됩니다.

로워카멜 표기법 (lowerCamelCase):

	- 첫 단어의 첫 글자를 소문자로 시작하고, 나머지 단어의 첫 글자를 대문자로 씁니다.
	- 주로 변수명이나 함수명에 사용됩니다.
	- 예: voiceSeparation, myVariableName, calculateTotal

스네이크 표기법 (snake_case):

	- 단어를 밑줄로 구분하며, 모든 글자를 소문자로 씁니다.
	- 예: voice_separation, my_variable_name, total_count
	- 파이썬에서는 변수명이나 함수명에 자주 사용됩니다.

케밥 표기법 (kebab-case):

	- 단어를 하이픈(-)으로 구분하며, 모든 글자를 소문자로 씁니다.
	- 예: voice-separation, my-variable-name, total-count
	- URL 경로나 HTML/CSS 클래스 이름에서 자주 사용됩니다.
*/
"""

from typing import Text

# Snake -> Pascal
# service_plan -> ServicePlan
def snake_to_pascal(snake: Text) -> Text:
    return ''.join(word.capitalize() for word in snake.split('_'))

# Pascal -> Snake
# ServicePlan -> service_plan
def pascal_to_snake(pascal: Text) -> Text:
    return ''.join(['_' + c.lower() if c.isupper() else c for c in pascal]).lstrip('_')

# Snake -> Camel
# service_plan -> servicePlan
def snake_to_camel(snake: Text) -> Text:
    pascal = snake_to_pascal(snake)
    return pascal[0].lower() + pascal[1:]

# Camel -> Snake
# servicePlan -> service_plan
def camel_to_snake(camel: Text) -> Text:
    return pascal_to_snake(camel)


# Camel -> Pascal
# servicePlan -> ServicePlan
def camel_to_pascal(camel: Text) -> Text:
    return camel.capitalize()

# Pascal -> Camel
# ServicePlan -> servicePlan
def pascal_to_camel(pascal: Text) -> Text:
    return pascal[0].lower() + pascal[1:]


