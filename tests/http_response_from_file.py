# -*- coding: utf-8 -*-
import os

import pathlib

from scrapy.http import TextResponse, Request

URL = 'http://www.dummy.ons.gov.uk'
DIRECTORY = os.path.dirname(os.path.realpath(__file__))


def dummy_http_response(file_name, meta=None):

    request = Request(url=URL, meta=meta)
    file_path = os.path.join(DIRECTORY, 'resources', file_name)

    content = pathlib.Path(file_path).read_text()

    response = TextResponse(url=URL, request=request, body=content, encoding='utf-8')

    return response
