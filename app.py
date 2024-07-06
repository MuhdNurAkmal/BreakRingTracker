import pandas as pd
import streamlit as st
import base64
import time
import plotly.express as px

from process.dataViz import Dashboard
from process.dataProcess import DataProcessing
from process.dataFilter import DataFiltering

# ------------------- PAGE SETUP ---------------------------
st.set_page_config(page_title="Break Ring Dashboard", layout='wide')

with open("assets/logoHuawei.png", "rb") as img_file:
    huawei_logo = base64.b64encode(img_file.read()).decode()

with open("assets/CDBLogo.png", "rb") as img_file:
    cd_logo = base64.b64encode(img_file.read()).decode()

st.markdown(f"""
    <style>
    .header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .title h1 {{
        font-size: 3rem;
    }}
    .logo {{
        display: flex;
    }}
    .logo img {{
        height: 6rem;
        margin-right: 1rem;
    }}
    </style>
    
    <div class="header">
        <div class="title">
            <h1>Break Ring Tracker
        </div>
        <div class="logo">
            <img src="data:image/png;base64,{huawei_logo}">
            <img src="data:image/png;base64,{cd_logo}">
        </div>
    </div>
    <hr>
    """, unsafe_allow_html=True)

if 'dataframes' not in st.session_state:
    st.session_state.dataframes = None
if 'new_df' not in st.session_state:
    st.session_state.new_df = pd.DataFrame()

################################ FILE UPLOADER ################################
uploaded_files = st.file_uploader("", type=['xlsx', 'csv'], accept_multiple_files=True)

if uploaded_files:
    if st.button('Upload'):
        dataframes = []
        for file in uploaded_files:
            excel_file = pd.ExcelFile(file)
            if 'Master Data' in excel_file.sheet_names:
                df = pd.read_excel(file, sheet_name='Master Data', skiprows=[0])
            else:
                df = pd.read_excel(file, skiprows=[0])
            dataframes.append({file.name : df})
        
        st.session_state.dataframes = dataframes
        st.session_state.new_df = DataProcessing(dataframes)

    st.html("<hr>")
    # col1, col2 = st.columns([1, 3])
    
    if st.session_state.new_df is not None and not st.session_state.new_df.empty:
        df = DataFiltering(st.session_state.new_df)
        st.dataframe(df, hide_index=True)
        st.success(f"{df.shape[0]} rows of data have been shown.")
                        
        st.html("<hr>")
                
################################ DASHBOARD ################################
        dashboard = Dashboard(st.session_state.new_df) 

        dashboard.PieChart()
        dashboard.HorizontalBarGraph()
        dashboard.BarGraph()  
   