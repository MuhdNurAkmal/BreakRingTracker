import streamlit as st

def CreateMultiselect(df):
    ringID = st.multiselect("Break Ring Status",
                            options=df["Break Ring Status"].unique())
    
    subcon = st.multiselect("Subcon",
                            options=df["Subcon"].unique())
    
    state = st.multiselect("State",
                            options=df["State"].unique())
    
    region = st.multiselect("Region",
                             options=df["Region"].unique())
    
    return ringID, subcon, state, region
    
def DataFiltering(df, ringID, subcon, state, region):
    
    df_filter = df.copy()
    
    if ringID:
        df_filter = df_filter[df_filter['Break Ring Status'].isin(ringID)]
    if subcon:
        df_filter = df_filter[df_filter['Subcon'].isin(subcon)]
    if state:
        df_filter = df_filter[df_filter['State'].isin(state)]
    if region:
        df_filter = df_filter[df_filter['Region'].isin(region)]
    
    return df_filter