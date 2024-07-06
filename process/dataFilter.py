import streamlit as st

def DataFiltering(df):
    filter_options = {
        "File Source": "Source",
        "Batch": "Batch",
        "Break Ring Status": "Break Ring Status",
        "Priority": "Priority",
        "State": "State",
        "Region": "Region",
        "Subcon": "Subcon",
        "CME Status": "CME Status"
    }

    selections = {}
    cols = st.columns(4)
    
    for idx, (label, column) in enumerate(filter_options.items()):
        with cols[idx % 4]:
            selections[column] = st.multiselect(label, options=df[column].unique())
    
    filtered_df = df.copy()
    for column, selected_values in selections.items():
        if selected_values:
            filtered_df = filtered_df[filtered_df[column].isin(selected_values)]
    
    return filtered_df
