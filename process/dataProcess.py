import streamlit as st
import pandas as pd
import numpy as np

def DataProcessing(dataframes):    
    processed_df = []
    for file_dict in dataframes:
        for filename, df in file_dict.items():
            if 'DUID2' in df.columns:
                df = df.rename(columns = {'DUID2':'DUID / Activity Name'})
            if 'ACTIVITY NAME' in df.columns:
                df = df.rename(columns = {'ACTIVITY NAME':'DUID / Activity Name'})

            df['Source'] = filename.split('.')[0]
            processed_df.append(df)
        
    merged_df = pd.concat(processed_df, ignore_index=True)
    
    merged_df.rename(columns = {'Priority Rollout (colour)' : 'Priority',
                                'Status' : 'CME Status',
                                'Plan Survey Date' : 'Plan Survey',
                                'Survey Date' : 'Actual Survey',
                                'Material On Site (MOS)' : 'Actual MOS',
                                'Power Up ' : 'Actual Power Up',
                                'Integration' : 'Actual Integration',
                                'SWAP/MIGRATION PLAN DATE' : 'Plan Migration',
                                'SWAP/MIGRATION \nCOMPLETION DATE' : 'Actual Migration',
                                'CD ES PO Date' : 'PO ES Date', 
                                'CD EQ PO Date' : 'PO EQ Date'
                                }, inplace = True)
    
    merged_df = merged_df[['Ring ID','DUID / Activity Name',
                           'Source',
                           'Batch', 'Priority',
                           'Site ID', 'Site Name',
                           'Region', 'State',
                           'Subcon',
                           'CME Type', 'CME Status',
                           'Plan Survey', 'Actual Survey',
                           'Plan MOS', 'Actual MOS',
                        #    'Plan Installation', 'Actual Installation',
                        #    'QCTE',
                           'Plan Power Up', 'Actual Power Up',
                           'Plan Integration', 'Actual Integration',
                           'Plan Migration', 'Actual Migration',
                           'Break Ring Status',
                           'PO ES Date', 'PO EQ Date',
                           ]]
    
    merged_df = merged_df.fillna('N/A')
    merged_df['Break Ring Status'] = merged_df['Break Ring Status'].replace('completed', 'Completed')
    merged_df['Subcon'] = merged_df['Subcon'].str.upper()
    columns_to_capitalize = ['Region', 'State']
    for col in columns_to_capitalize:
        merged_df[col] = merged_df[col].str.title()
    merged_df[['Region', 'State']] = merged_df[['Region', 'State']].replace('Tba', 'TBA')
    
    merged_df.sort_values(by=['Ring ID'], inplace=True)
    
    return merged_df