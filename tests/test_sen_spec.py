from ultis import sen_spec, json_to_dict

def test_sen_spec1():
    out1 = json_to_dict('data_owner1.json')
    performance = sen_spec(out1)
    check_output_type(performance)
    check_output_keys(performance)
    check_output_values_type(performance)

def test_sen_spec2():
    out2 = json_to_dict('data_owner2.json')
    performance = sen_spec(out2)
    check_output_type(performance)
    check_output_keys(performance)
    check_output_values_type(performance)

def check_output_type(performance):
    # to test if the output is a dictionary
    assert type(performance) is dict

def check_output_keys(performance):
    # to test if keys of the dictionary output include None, Mild, Moderate, Severe, Proliferative
    keys = set(performance.keys())
    test_keys = {'None','Mild','Moderate','Severe','Proliferative'}
    assert keys == test_keys

def check_output_values_type(performance):
    # to test if values of the dictionary output are dictionaries 
    check = [type(i) is dict for i in performance.values()]
    assert all(check) is True