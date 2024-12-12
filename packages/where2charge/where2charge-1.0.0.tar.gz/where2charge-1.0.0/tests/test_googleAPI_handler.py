"""This module contains the tests for the googleAPI_handler module."""
import pytest
import pandas as pd
from src.where2charge.logic.googleAPI_handler import GoogleAPIHandler
from src import util

GOOGLE_API_KEY = util.read_config('src/config.yaml')['GOOGLE_API_KEY']
# Smoke tests 1. Check if we get any output
def test_smoke():
    client = GoogleAPIHandler(GOOGLE_API_KEY)
    assert client is not None

# Smoke Test 2. the output type of the data
def test_output_type():
    client = GoogleAPIHandler(GOOGLE_API_KEY)
    output = client.get_all_data_from_google(latitude=47.616303606504985, longitude=-122.32454538345338)
    assert type(output) == pd.DataFrame

# Smoke tests 3. Check if we get any error
def test_smoke_error():
    with pytest.raises(Exception):
        GoogleAPIHandler(GOOGLE_API_KEY)

# Edge tests 1. Check if it works with invalid data