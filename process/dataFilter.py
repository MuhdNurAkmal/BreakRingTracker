import streamlit as st

def DataFiltering(df):
    ringID = st.multiselect("Break Ring Status", options=df["Break Ring Status"].unique())
    subcon = st.multiselect("Subcon", options=df["Subcon"].unique())
    state = st.multiselect("State", options=df["State"].unique())
    region = st.multiselect("Region", options=df["Region"].unique())
    
    filtered_df = df.copy()
    
    if ringID:
        filtered_df = filtered_df[filtered_df['Break Ring Status'].isin(ringID)]
    if subcon:
        filtered_df = filtered_df[filtered_df['Subcon'].isin(subcon)]
    if state:
        filtered_df = filtered_df[filtered_df['State'].isin(state)]
    if region:
        filtered_df = filtered_df[filtered_df['Region'].isin(region)]
    
    return filtered_df
