from ultis import json_to_dict

def test_json_to_dic1():
    out = json_to_dict('data_owner1.json')
    check_output_type(out)

def test_json_to_dic2():
    out = json_to_dict('data_owner2.json')
    check_output_type(out)

def check_output_type(out):
    # to test if the output is a dictionary
    assert type(out) is dict
