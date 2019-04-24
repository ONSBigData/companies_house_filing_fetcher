# -*- coding: utf-8 -*-
"""
@author: Philip Lee
"""
from tests.http_response_from_file import dummy_http_response

import json


def test_simple_filing_history():

    response = dummy_http_response('simple_filing_history.json')

    json_response = json.loads(response.body_as_unicode())

    assert "filing_history_status" in json_response
