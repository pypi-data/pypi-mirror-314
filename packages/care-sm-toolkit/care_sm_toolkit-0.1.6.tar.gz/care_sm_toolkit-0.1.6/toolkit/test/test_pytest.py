import pytest
import pandas as pd
from toolkit.main import Toolkit as Tool

@pytest.mark.parametrize("input_data", [
    ("exemplar_data/fiab_input_data.csv")
])
def test_import_data_works(input_data):
    toolkit = Tool()
    result = toolkit.import_your_data_from_csv(input_data)
    assert result is not False

@pytest.mark.parametrize("input_data", [
    (pd.DataFrame({'model': [1, 2], 'pid': [1, 2], 'event_id': [1, 2], 'value': [1, 2], 'age': [1, 2], 'value_datatype': [1, 2], 'valueIRI': [1, 2], 'activity': [1, 2], 'protocol_id':[1, 2],'unit': [1, 2], 'input': [1, 2], 'target': [1, 2], 'intensity': [1, 2],'frequency_type': [1, 2], 'frequency_value': [1, 2], 'agent_id': [1, 2], 'route': [1, 2], 'startdate': [1, 2], 'enddate': [1, 2], 'comments': [1, 2]})),
    (pd.DataFrame({'model': [1, 2], 'pid': [1, 2],'pid2': [1, 2], 'event_id': [1, 2], 'value': [1, 2], 'age': [1, 2], 'value_datatype': [1, 2], 'valueIRI': [1, 2], 'activity': [1, 2],'protocol_id':[1, 2], 'unit': [1, 2], 'input': [1, 2], 'target': [1, 2],'intensity': [1, 2], 'frequency_type': [1, 2], 'frequency_value': [1, 2], 'agent_id': [1, 2], 'route': [1, 2], 'startdate': [1, 2], 'enddate': [1, 2], 'comments': [1, 2]})),
])
def test_column_names_are_present(input_data):
    toolkit = Tool()
    result = toolkit.check_status_column_names(input_data)
    assert result is not False

@pytest.mark.parametrize("input_data", [
    (pd.DataFrame({'model': [1, 2], 'event_id': [1, 2], 'value': [1, 2], 'age': [1, 2], 'value_datatype': [1, 2], 'valueIRI': [1, 2], 'activity': [1, 2],'protocol_id':[1, 2], 'unit': [1, 2], 'input': [1, 2], 'target': [1, 2], 'intensity': [1, 2],'frequency_type': [1, 2], 'frequency_value': [1, 2], 'agent_id': [1, 2], 'route': [1, 2], 'startdate': [1, 2], 'enddate': [1, 2], 'comments': [1, 2]})),
    (pd.DataFrame({'model': [1, 2], 'pid': [1, 2],'pid2': [3, 4], 'value': [1, 2], 'age': [1, 2], 'value_datatype': [1, 2], 'valueIRI': [1, 2], 'activity': [1, 2], 'protocol_id':[1, 2],'unit': [1, 2], 'input': [1, 2], 'target': [1, 2], 'intensity': [1, 2],'frequency_type': [1, 2], 'frequency_value': [1, 2], 'agent_id': [1, 2], 'route': [1, 2], 'startdate': [1, 2], 'enddate': [1, 2], 'comments': [1, 2]})),
])
def test_column_names_are_not_present(input_data):
    toolkit = Tool()
    result = toolkit.check_status_column_names(input_data)
    assert result == False

@pytest.mark.parametrize("data_with_duplicates", [
    (pd.DataFrame({'model': ["model", 2], 'pid': [1, 2],'event_id': [1, 2], 'value': [1, 2], 'age': [1, 2], 'value_datatype': [1, 2], 'valueIRI': [1, 2], 'activity': [1, 2], 'protocol_id':[1, 2], 'unit': [1, 2], 'input': [1, 2], 'target': [1, 2], 'intensity': [1, 2],'frequency_type': [1, 2], 'frequency_value': [1, 2], 'agent_id': [1, 2], 'route': [1, 2], 'startdate': [1, 2], 'enddate': [1, 2], 'comments': [1, 2]})),
    (pd.DataFrame({'model': ["model", "model"], 'pid': [1, 2], 'event_id': [1, 2], 'value': [1, 2], 'age': [1, 2], 'value_datatype': [1, 2], 'valueIRI': [1, 2], 'activity': [1, 2], 'protocol_id':[1, 2], 'unit': [1, 2], 'input': [1, 2], 'target': [1, 2], 'intensity': [1, 2],'frequency_type': [1, 2], 'frequency_value': [1, 2], 'agent_id': [1, 2], 'route': [1, 2], 'startdate': [1, 2], 'enddate': [1, 2], 'comments': [1, 2]})),
])
def test_duplicated_titles_amog_row(data_with_duplicates):
    toolkit = Tool()
    result_with_duplicates = toolkit.check_for_duplicated_titles_among_row(data_with_duplicates)
    assert result_with_duplicates == True

@pytest.mark.parametrize("input_data, expected_data", [

    (pd.DataFrame({'model':['Sex'],'valueIRI':['https://Female'],'value': ["Female"],'target': [None], 'value_datatype': ["xsd:string"], 'value_string': [None],'value_id':[None],'attribute_type':[None]}),
     pd.DataFrame({'model':['Sex'],'valueIRI':['https://Female'],'value': ["Female"],'target': [None], 'value_datatype': ["xsd:string"], 'value_string': ["Female"],'value_id':[None],'attribute_type':['https://Female']})),
    
    (pd.DataFrame({'model':['Birthdate'],'valueIRI':[None],'value': ["2021-12-05"],'target': [None], 'value_datatype': ["xsd:date"], 'value_date': [None],'value_id':[None]}),
     pd.DataFrame({'model':['Birthdate'],'valueIRI':[None],'value': ["2021-12-05"],'target': [None], 'value_datatype': ["xsd:date"], 'value_date': ["2021-12-05"],'value_id':[None]})),
    ])

def test_value_edition_works(input_data, expected_data):
    toolkit = Tool()
    result_value_edition = toolkit.value_edition(input_data)
    
    if "value_integer" in result_value_edition:
        result_value_edition["value_integer"] = result_value_edition["value_integer"].astype('int64')
    if "value_float" in result_value_edition:
        result_value_edition["value_float"] = result_value_edition["value_float"].astype('float')
    if ("value_string" in result_value_edition):
        result_value_edition["value_string"] = result_value_edition["value_string"].astype('object')
    if ("value_date" in result_value_edition):
        result_value_edition["value_date"] = result_value_edition["value_date"].astype('object')
        
    assert result_value_edition.equals(expected_data)

@pytest.mark.parametrize("input_data, expected_data", [
    (pd.DataFrame(
        { 'model': ['Birthdate','Deathdate','Deathdate'],
                  'startdate':[None,'2020-03-08',None],
                   'enddate':[None,None,None],
             }),
     
     pd.DataFrame({ 'model': ['Birthdate','Deathdate','Deathdate'],
                  'startdate':[None,'2020-03-08',None],
                   'enddate':[None,'2020-03-08',None],

             })),

])
def test_time_edition_works(input_data, expected_data):
    toolkit = Tool()
    result_value_edition = toolkit.time_edition(input_data)
    
    if "value_integer" in result_value_edition:
        result_value_edition["age"] = result_value_edition["age"].astype('float64')
        result_value_edition["value_integer"] = result_value_edition["value_integer"].astype('float64')

    # print("Actual DataFrame Data Types:")
    # print(result_value_edition)

    # print("Expected DataFrame Data Types:")
    # print(expected_data)
    assert result_value_edition.equals(expected_data)

@pytest.mark.parametrize("input_data, expected_data", [
    (pd.DataFrame(
        { 'model': ['Diagnosis',"Consent_used","Symptom_onset",'Clinical_trial','Biobank','Biobank'],
                'value':['valueX',None,'valueX',None,None,None],
                'valueIRI':['valueX',None,None,'valueX',None,None],
                'age':['valueX',None,None,None,None,None],
                'agent_id':[None,None,None,'valueX',None,None],
                'activity':[None,None,None,None,None,None],
                'target':[None,None,None,None,None,None],
             }),
     
    pd.DataFrame(
        { 'model': ['Diagnosis',"Consent_used","Symptom_onset",'Clinical_trial','Biobank','Biobank'],
                'value':['valueX',None,'valueX',None,None,None],
                'valueIRI':['valueX',None,None,'valueX',None,None],
                'age':['valueX',None,None,None,None,None],
                'agent_id':[None,None,None,'valueX',None,None],
                'activity':[None,None,None,None,None,None],
                'target':[None,None,None,None,None,None],

             })
    ),
])
def test_clean_empty_rows_works(input_data, expected_data):
    toolkit = Tool()
    result_value_edition = toolkit.clean_empty_rows(input_data)
    assert result_value_edition.equals(expected_data)

if __name__ == '__main__':
    pytest.main([__file__])