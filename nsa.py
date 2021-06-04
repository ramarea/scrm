# Code Author: Tumisang Ramarea
# Project co-Author: Kyriakos Lotidis
# Spring 2021
# EE 384S: Performance Engineering of Computer Networks
# Final Project
# Analysis of Results

import numpy as np
import pandas as pd

agents = ["R1", "R2", "D1", "D2", "S1", "S2"]
networks = ["ES", "RS", "RH", "AS"]
scenarios = ["DLSL","DHSL","DLSH","DHSH"]
len_df = 0

def computeValueAdd(df):
    df['Value Add'] = df['Revenue'] - df['Costs']

def computeCSL(df):
    data = df['Filled Orders'] / (df['Filled Orders'] + df['Discarded Orders'])
    df.insert(4,'CSL', data)
    
def removeExcessColumns(df):
    return df.drop(['Unnamed: 0','Filled Orders','Discarded Orders','Revenue', 'Costs'], axis = 1)
    
def renameColumns(df,name):
    #newcsl = f"CSL ({name})"
    #print(newcsl)
    return df.rename({'CSL':f"CSL ({name})", 'Value Add': f"Value Add ({name})"}, axis = 1)

def preprocessSimData():
    my_dict = {}
    for scenario in scenarios:
        for network in networks:
            for agent in agents:
                name = f"{network}_{agent}_{scenario}"
                df = pd.read_csv(f"{name}.csv")
                computeValueAdd(df)
                computeCSL(df)
                df = removeExcessColumns(df)
                df = renameColumns(df,name)
                #print(df.columns)
                my_dict[name] = df
    return my_dict

def mergeData(data_dict):
    df = pd.DataFrame()
    df['Time'] = np.arange(len(data_dict["ES_R1_DLSL"]))
    for scenario in scenarios:
        for network in networks:
            for agent in agents:
                temp = data_dict[f"{network}_{agent}_{scenario}"]
                df = pd.merge(df,temp, how = "outer")
    return df
        

def analyzeByScenario(data):
    for scenario in scenarios:
        titles = ['Time', f"CSL (ES_R1_{scenario})", f"CSL (ES_R2_{scenario})", f"CSL (ES_D1_{scenario})",f"CSL (ES_D2_{scenario})",f"CSL (ES_S1_{scenario})",f"CSL (ES_S2_{scenario})",f"CSL (AS_R1_{scenario})", f"CSL (AS_R2_{scenario})", f"CSL (AS_D1_{scenario})",f"CSL (AS_D2_{scenario})",f"CSL (AS_S1_{scenario})",f"CSL (AS_S2_{scenario})",f"CSL (RS_R1_{scenario})", f"CSL (RS_R2_{scenario})", f"CSL (RS_D1_{scenario})",f"CSL (RS_D2_{scenario})",f"CSL (RS_S1_{scenario})",f"CSL (RS_S2_{scenario})",f"CSL (RH_R1_{scenario})", f"CSL (RH_R2_{scenario})", f"CSL (RH_D1_{scenario})",f"CSL (RH_D2_{scenario})",f"CSL (RH_S1_{scenario})",f"CSL (RH_S2_{scenario})", f"Value Add (ES_R1_{scenario})", f"Value Add (ES_R2_{scenario})", f"Value Add (ES_D1_{scenario})",f"Value Add (ES_D2_{scenario})",f"Value Add (ES_S1_{scenario})",f"Value Add (ES_S2_{scenario})",f"Value Add (AS_R1_{scenario})", f"Value Add (AS_R2_{scenario})", f"Value Add (AS_D1_{scenario})",f"Value Add (AS_D2_{scenario})",f"Value Add (AS_S1_{scenario})",f"Value Add (AS_S2_{scenario})",f"Value Add (RS_R1_{scenario})", f"Value Add (RS_R2_{scenario})", f"Value Add (RS_D1_{scenario})",f"Value Add (RS_D2_{scenario})",f"Value Add (RS_S1_{scenario})",f"Value Add (RS_S2_{scenario})",f"Value Add (RH_R1_{scenario})", f"Value Add (RH_R2_{scenario})", f"Value Add (RH_D1_{scenario})",f"Value Add (RH_D2_{scenario})",f"Value Add (RH_S1_{scenario})",f"Value Add (RH_S2_{scenario})"]
        df = data[titles]
        analyzeByNetwork(df)
        print(df)

def computeAgentMetric(data, metric):
    cols = [col for col in data.columns if metric in col]
    df = pd.DataFrame()
    metric_df = data[cols]
    #print(df)
    for column in metric_df:
        if metric == 'Value Add':
            col_sum = metric_df[column].sum()
        else:
            col_sum = metric_df[column].mean()
        df[column] = [col_sum]
    return df

def main():
    sim_data_dict = preprocessSimData()
    merged_data = mergeData(sim_data_dict)
    va_metrics = computeAgentMetric(merged_data, 'Value Add')
    csl_metrics = computeAgentMetric(merged_data, 'CSL')
    va_metrics.to_csv('va_metrics.csv')
    csl_metrics.to_csv('csl_metrics.csv')
    #analyzeByScenario(merged_data)
    #print(merged_data.columns)
    #print(sim_data_dict)
    
if __name__ == '__main__':
    main()
