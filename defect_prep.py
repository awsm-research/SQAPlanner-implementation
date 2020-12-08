#!/usr/bin/env python3
# coding: utf-8

# In[1]:


import pickle
import pandas as pd

from util_lomika import *
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


# In[4]:


def prepare_defect_dataset_fin(filename, path_data):
    # '/home/dilini/lomika/adult/adult.csv'
    # Read dataset

    # Numerical variables
    numerical_vars=['CountDeclMethodPrivate', 'AvgLineCode', 'CountLine', 'MaxCyclomatic', 'CountDeclMethodDefault',
     'AvgEssential','CountDeclClassVariable', 'SumCyclomaticStrict', 'AvgCyclomatic', 'AvgLine','CountDeclClassMethod','AvgLineComment', 'AvgCyclomaticModified', 'CountDeclFunction', 'CountLineComment', 'CountDeclClass',
     'CountDeclMethod', 'SumCyclomaticModified', 'CountLineCodeDecl', 'CountDeclMethodProtected',
     'CountDeclInstanceVariable', 'MaxCyclomaticStrict', 'CountDeclMethodPublic', 'CountLineCodeExe',
     'SumCyclomatic', 'SumEssential', 'CountStmtDecl', 'CountLineCode', 'CountStmtExe', 'RatioCommentToCode',
     'CountLineBlank', 'CountStmt', 'MaxCyclomaticModified', 'CountSemicolon', 'AvgLineBlank',
     'CountDeclInstanceMethod', 'AvgCyclomaticStrict', 'PercentLackOfCohesion', 'MaxInheritanceTree',
     'CountClassDerived', 'CountClassCoupled', 'CountClassBase', 'CountInput_Max', 'CountInput_Mean',
     'CountInput_Min', 'CountOutput_Max', 'CountOutput_Mean', 'CountOutput_Min', 'CountPath_Max', 'CountPath_Mean',
     'CountPath_Min', 'MaxNesting_Max', 'MaxNesting_Mean', 'MaxNesting_Min', 'COMM', 'ADEV', 'DDEV', 'Added_lines',
     'Del_lines', 'OWN_LINE', 'OWN_COMMIT', 'MINOR_COMMIT', 'MINOR_LINE', 'MAJOR_COMMIT', 'MAJOR_LINE', 'HeuBugCount']
    categorical_vars = []
    
   # path_data='/home/dilini/defects/jira_n/'+file
    #file_name = file

    dataset_trn = pd.read_csv(path_data+'/'+filename+'-R1.csv', skipinitialspace=True)
    dataset_tst = pd.read_csv(path_data+'/datasets/'+filename+'-R2.csv', skipinitialspace=True)
    dataset_val = pd.read_csv(path_data+'/datasets/'+filename+'-R3.csv', skipinitialspace=True)

    remove_variables(dataset_trn,['Unnamed: 0'])
    remove_variables(dataset_tst,['Unnamed: 0'])
    remove_variables(dataset_val,['Unnamed: 0'])
    
    vars_to_remove = ['File', 'HeuBug','RealBugCount','file_id']
    remove_variables(dataset_trn,vars_to_remove)
    remove_variables(dataset_tst,vars_to_remove)
    remove_variables(dataset_val,vars_to_remove)

    dataset_trn=dataset_trn.rename(columns={'RealBug': 'target'})
    dataset_tst=dataset_tst.rename(columns={'RealBug': 'target'})
    dataset_val=dataset_val.rename(columns={'RealBug': 'target'})

    df_bl_trn_fin = dataset_trn.copy()
    df_bl_tst_fin = dataset_tst.copy()
    df_bl_val_fin = dataset_val.copy()

    dataset_trn['train'] = 1
    dataset_tst['train'] = 0
    dataset_val['train'] = 2

    combined = pd.concat([dataset_trn,dataset_tst,dataset_val])

    label_le = LabelEncoder()
    combined['target'] = label_le.fit_transform(combined['target'].values)
    df_le_com, label_encoder = label_encode(combined, categorical_vars, label_encoder=None)

    train_fin = df_le_com[df_le_com["train"]==1]
    test_fin = df_le_com[df_le_com["train"]==0]
    validation_fin = df_le_com[df_le_com["train"]==2]

    train_fin.drop(["train"],axis=1,inplace=True)
    test_fin.drop(["train"],axis=1,inplace=True)
    validation_fin.drop(["train"],axis=1,inplace=True)


#     train_fin.to_csv(path_data+'/data_MO/'+file+'.csv', sep=',', encoding='utf-8')
#     test_fin.to_csv(path_data+'/data_MO/'+file+'test.csv', sep=',', encoding='utf-8')

    dataset = {
       # 'name': filename.replace('.csv', ''),
        'name':filename,
        'df_bl_trn_fin': df_bl_trn_fin,
        'df_bl_tst_fin': df_bl_tst_fin,
        'df_bl_val_fin': df_bl_val_fin,
        'categorical_vars': categorical_vars,
        'numerical_vars': numerical_vars,
        'label_encoder': label_encoder,
        'train': train_fin,
        'test': test_fin,
        'validation': validation_fin,
        
       # 'df_le': df_le
    }
    return dataset

