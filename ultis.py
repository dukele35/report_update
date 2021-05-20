import json
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix

def json_to_dict(filename):
    '''
    Input:
        - filename: a .json filename
    Output:
        - a dictionary
    '''
    with open(filename) as json_file:
        string_format = json.load(json_file)
        dict_format = json.loads(string_format)
        return dict_format

def sen_spec(dic):
    '''
    Input:
        - a dictionary has values as file names and keys as sub-dictionaries as follows:
          e.g. {'image1.png':
                    {'prediction': {'None': 0.1, 'Mild':0.2, 'Moderate':0.3, 'Severe':0.2, 'Proliferative':0.2},
                     'true_class': 'Mild',
                     'pred_class': 'Moderate',
                     'SHA256': '4539ske2304202...'}, 
                'image2.png':
                    {'prediction': {'None': 0.05, 'Mild':0.15, 'Moderate':0.3, 'Severe':0.25, 'Proliferative':0.25},
                     'true_class': 'Moderate',
                     'pred_class': 'Moderate',
                     'SHA256': '567d4c23567891...'}}
    Output:
        - a dictionary has keys as classes, i.e. None, Mild, Moderate, Severe and Proliferative, 
          and values as sub-dictionaries of the sensitivity and specificity measurements for those classes
          e.g. {'None':{'sensivitity':0.6, 'specificity':0.7}, 
                'Mild':{'sensivitity':0.9, 'specificity':1}, 
                'Moderate':{'sensivitity':0.2, 'specificity':0.4},
                'Severe':{'sensivitity':0.6, 'specificity':0.5},
                'Proliferative':{'sensivitity':0.8, 'specificity':0.5}}
    '''
    df = pd.DataFrame(columns=['id', 'true_class', 'pred_class'])
    for filename in dic:
        row = pd.Series({'id':filename, 'true_class':dic[filename]['true_class'], 'pred_class':dic[filename]['pred_class']})
        df = df.append(row, ignore_index=True)
    cm = confusion_matrix(df['true_class'], df['pred_class'], labels=['None', 'Mild', 'Moderate', 'Severe', 'Proliferative'])
    index = {'None':0, 'Mild':1, 'Moderate':2, 'Severe':3, 'Proliferative':4}
    performance = {}
    for key in index.keys():
        tp = cm[index[key], index[key]]
        fn = sum(np.delete(cm[index[key],:], index[key]))
        fp = sum(np.delete(cm[:,index[key]], index[key]))
        tn = sum(sum(np.delete(np.delete(cm, index[key], 0), index[key], 1)))
        sensitivity = tp / (tp + fn)
        specificity = tn / (tn + fp)
        performance[key] = {'sensitivity':sensitivity, 'specificity':specificity}
    return performance

