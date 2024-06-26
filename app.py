import pandas as pd
import streamlit as st
import base64

from process.dataViz import DataVisualization
from process.dataProcess import DataProcessing

# ------------------- PAGE SETUP ---------------------------
st.set_page_config(page_title="Break Ring Dashboard",
                   layout='wide',
                   initial_sidebar_state='collapsed'
                   )

# ---- HEADER WITH LOGOS ----
with open("assets/logoHuawei.jpg", "rb") as img_file:
    image_1 = base64.b64encode(img_file.read()).decode()

with open("assets/CDBLogo.png", "rb") as img_file:
    image_2 = base64.b64encode(img_file.read()).decode()

st.markdown(
    f"""
    <style>
    .header {{
        display: flex;
        align-items: center;
    }}
    .header img {{
        height: 7rem;
        margin-right: 2rem;
    }}
    </style>
    <div class="header">
        <img src="data:image/png;base64,{image_1}" height="20rem" alt="Logo 1">
        <img src="data:image/png;base64,{image_2}" height="20rem" alt="Logo 2">
    </div>
    """,
    unsafe_allow_html=True
)

# Initialize session state
if 'dataframes' not in st.session_state:
    st.session_state.dataframes = None
if 'new_df' not in st.session_state:
    st.session_state.new_df = pd.DataFrame()

# ------------------- UPLOAD FILE --------------------------
# uploaded_files = st.file_uploader("", type=["xlsx"], accept_multiple_files=True)

if uploaded_files:
    if st.button('Upload'):
        dataframes = []
        for file in uploaded_files:
            excel_file = pd.ExcelFile(file)
            if 'Master Data' in excel_file.sheet_names:
                df = pd.read_excel(file, sheet_name='Master Data', skiprows=[0])
            else:
                df = pd.read_excel(file, skiprows=[0])
            dataframes.append(df)
        
        st.session_state.dataframes = dataframes
        st.session_state.new_df = DataProcessing(dataframes)

# This is for filtering
col1, col2 = st.columns([3, 1])

if st.session_state.new_df is not None and not st.session_state.new_df.empty:
    with col2:
        st.header("Please Filter Here:", anchor=False)
        
        ring_id = st.multiselect(
            "Break Ring Status",
            options=st.session_state.new_df['Break Ring Status'].unique(),
        )
        
        subcon = st.multiselect(
            "Subcon",
            options=st.session_state.new_df['Subcon'].unique(),
        )
        state = st.multiselect(
            "State Name",
            options=st.session_state.new_df['State'].unique(),
        )
        region = st.multiselect(
            "Region",
            options=st.session_state.new_df['Region'].unique(),
        )

    # ---------- DATA FILTERING -------------
    df_selection = st.session_state.new_df.copy()
    
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
    
    DataVisualization(df_selection)