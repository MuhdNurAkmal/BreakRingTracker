import streamlit as st
import pandas as pd
import numpy as np

def DataProcessing(dataframes):
    st.title("DataFrame", anchor=False)
    
    processed_df = []
    print(dataframes)
    for df in dataframes:
        if 'DUID2' in df.columns:
            df = df.rename(columns = {'DUID2':'DUID / Activity Name'})
        if 'ACTIVITY NAME' in df.columns:
            df = df.rename(columns = {'ACTIVITY NAME':'DUID / Activity Name'})
        
        processed_df.append(df)
        
    merged_df = pd.concat(processed_df, ignore_index=True)
    
    selected_column = ['Batch', 'Break Ring Status', 'CD EQ PO Date', 'CD ES PO Date',
                       'CME Type', 'DUID / Activity Name',
                       'Integrated Date (30days + install)', 'Integration',
                       'Material On Site (MOS)', 'Plan Integration', 'Plan MOS',
                       'Plan Power Up', 'Plan Survey Date', 'Power Up ',
                       'Priority Rollout (colour)', 'Region', 'Ring ID',
                       'SWAP/MIGRATION \nCOMPLETION DATE', 'SWAP/MIGRATION PLAN DATE',
                       'Site ID', 'Site Name', 'State', 'Status', 'Subcon',
                       'Survey Completed', 'Survey Date', 'Survey Plan'
                       ]
    
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
                           'PO ES Date', 'PO EQ Date'
                           ]]
    
    # Data Tranformation
    merged_df = merged_df.fillna('N/A')
    merged_df['Break Ring Status'] = merged_df['Break Ring Status'].replace('completed', 'Completed')
    columns_to_capitalize = ['Subcon', 'Region', 'State']
    for col in columns_to_capitalize:
        merged_df[col] = merged_df[col].str.capitalize()
    
    return merged_df