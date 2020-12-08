#!/usr/bin/env python3
import numpy as np
import pandas as pd
import _pickle as cPickle
import random

from sklearn.preprocessing import LabelEncoder


def label_encode(df, columns, label_encoder=None):
    df_le = df.copy(deep=True)
    new_le = label_encoder is None
    label_encoder = dict() if new_le else label_encoder
    for col in columns:
        if new_le:
            le = LabelEncoder()
            df_le[col] = le.fit_transform(df_le[col])
            label_encoder[col] = le
        else:
            le = label_encoder[col]
            df_le[col] = le.transform(df_le[col])
    return df_le, label_encoder


def label_decode(df, columns, label_encoder):
    df_de = df.copy(deep=True)
    for col in columns:
        le = label_encoder[col]
        df_de[col] = le.inverse_transform(df_de[col])
    return df_de


def get_test_sample(model, test, poor=True, correct=True, seed=42, count=1):
    '''
    Return one random sample from test set based on the selection criteria.
    
    parameters:
      model - the model which is tested for
      survived - select survived sample
      correct - select the sample which the model prediected correctly
    '''
    test_sample = test.ix[:, :-1]
    prediction = model.predict_proba(test_sample)

    if (poor and correct):
        ids_1 = np.argwhere((prediction[:, 0] > prediction[:, 1]))
        ids_2 = np.argwhere(test.target == 0)
        ids = np.intersect1d(ids_1, ids_2)
    elif (poor and not correct):
        ids_1 = np.argwhere((prediction[:, 0] > prediction[:, 1]))
        ids_2 = np.argwhere(test.target == 1)
        ids = np.intersect1d(ids_1, ids_2)
    elif (not poor and correct):
        ids_1 = np.argwhere((prediction[:, 0] < prediction[:, 1]))
        ids_2 = np.argwhere(test.target == 1)
        ids = np.intersect1d(ids_1, ids_2)
    elif (not poor and not correct):
        ids_1 = np.argwhere((prediction[:, 0] < prediction[:, 1]))
        ids_2 = np.argwhere(test.target == 0)
        ids = np.intersect1d(ids_1, ids_2)
    if count == 1:
        idx = random.Random(seed).choice(ids)
        print(idx)
        d_index = idx
    else:
        ids = ids.reshape(len(ids)).tolist()
        idx = random.Random(seed).sample(ids, count)
        d_index = idx

    return test_sample.iloc[idx, :], d_index



def score_compare(x, y, threshold=0.5):
    if x < threshold and y < threshold:
        return 'True Negative'
    elif x < threshold and y > threshold:
        return 'False Negative'
    elif x > threshold and y > threshold:
        return 'True Positive'
    elif x > threshold and y < threshold:
        return 'False Positive'


# prediction
def get_multiple_scores(result):
    sco = []
    for i in range(result.shape[0]):
        sco.append(round(result[i, 0], 2))
    return sco


def remove_variables(df, vars_to_remove):
    df.drop(vars_to_remove, axis=1, inplace=True, errors='ignore')
