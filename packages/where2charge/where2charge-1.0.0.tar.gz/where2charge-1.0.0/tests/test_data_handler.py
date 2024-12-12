"""This module contains the tests for the data_handler module."""
import pytest
import pandas as pd
from src.where2charge.logic.data_handler import get_supplementary_data

adr_pre = 'src/where2charge/logic'
# Smoke tests 1. Check if we get any output
def test_smoke():
    output = get_supplementary_data(address_prefix=adr_pre, generate=True)
    assert output is not None

# Smoke Test 2 (or One-shot tests). the output type
def test_output_type():
    output = get_supplementary_data(address_prefix=adr_pre)
    assert type(output) == pd.DataFrame

# Smoke tests 3. Check if we get any error
def test_smoke_error():
    with pytest.raises(Exception):
        get_supplementary_data(address_prefix=adr_pre)


# Edge tests 1. Check if it works with invalid data
def test_invalid_input():
    invalid_input = []
    with pytest.raises(Exception):
        get_supplementary_data._get_geo_data(invalid_input)

# Edge tests 2. Check if it works with invalid data columns
def test_invalid_input_columns():
    invalid_geo_df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    invalid_df_EV = pd.DataFrame({'C': [1, 2, 3], 'D': [4, 5, 6]})
    with pytest.raises(Exception):
        get_supplementary_data._merge_data(invalid_geo_df, invalid_df_EV)


# We need to add other tests, such as checking the columns in _merge_data



