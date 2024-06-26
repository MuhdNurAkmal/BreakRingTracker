import streamlit as st

def DataFiltering(df):
    
    col1, col2 = st.columns([3, 1])

    with col2:
        st.header("Please Filter Here:", anchor=False)
        
        ring_id = st.multiselect(
            "Break Ring Status",
            options=df['Break Ring Status'].unique(),
        )
        
        subcon = st.multiselect(
            "Subcon",
            options=df['Subcon'].unique(),
        )
        state = st.multiselect(
            "State Name",
            options=df['State'].unique(),
        )
        region = st.multiselect(
            "Region",
            options=df['Region'].unique(),
        )

    # ---------- DATA FILTERING -------------
    df_selection = df.copy()
    
    if ring_id:
        df_selection = df_selection[df_selection['Break Ring Status'].isin(ring_id)]
    if subcon:
        df_selection = df_selection[df_selection['Subcon'].isin(subcon)]
    if state:
        df_selection = df_selection[df_selection['State'].isin(state)]
    if region:
        df_selection = df_selection[df_selection['Region'].isin(region)]
        
    with col1:
        st.dataframe(df_selection)
        
    return df_selection