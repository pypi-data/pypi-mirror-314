import pytest
import pandas as pd
from toolkit.main import Toolkit
from unittest.mock import patch, MagicMock
import os

@pytest.fixture
def toolkit():
    return Toolkit()

@patch('pandas.read_csv')
def test_import_your_data_from_csv(self):
    self.match = "Diagnosis"

    mock_data = pd.DataFrame({'model': ['Diagnosis'], 'pid': [12356845]})
    
    result = self.toolkit.import_your_data_from_csv(self, input_data="CARE-SM-Toolkit/toolkit/new_exampler_data")
    assert result.equals(mock_data)
    

def test_check_status_column_names(toolkit):
    # Create a DataFrame with the correct columns
    data = pd.DataFrame(columns=toolkit.columns)
    result = toolkit.check_status_column_names(data)
    assert result is not None

    # Create a DataFrame with an incorrect column
    wrong_columns = toolkit.columns + ['extra_column']
    data = pd.DataFrame(columns=wrong_columns)
    with pytest.raises(SystemExit):
        toolkit.check_status_column_names(data)

    
def test_value_edition(toolkit):
    data = pd.DataFrame({
        'model': ['model1'],
        'value': ['test_value'],
        'value_datatype': ['xsd:string'],
        'valueIRI': [None],
        'target': [None],
        'input': [None],
        'agent': [None],
        'activity': [None],
        'unit': [None]
    })
    
    result = toolkit.value_edition(data)
    
    assert 'value_string' in result.columns
    assert result['value_string'][0] == 'test_value'

def test_time_edition(toolkit):
    data = pd.DataFrame({
        'model': ['model1'],
        'startdate': ['2024-01-01'],
        'enddate': [None]
    })
    
    result = toolkit.time_edition(data)
    assert result['enddate'][0] == '2024-01-01'
