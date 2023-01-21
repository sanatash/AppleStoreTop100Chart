"""
Test file used to test application with PyTest
Tests included:
    - test_invalid_url - check that it raises the InvalidUrlError
"""
import pytest
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

sys.path.append(project_root)

from src.web_scraping import *

test_path = os.path.dirname(__file__)

def test_invalid_url():

    with pytest.raises(InvalidUrlError):
        web_get_chart_list("test/invalid_chart_url.txt")

