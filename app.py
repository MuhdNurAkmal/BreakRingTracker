import pandas as pd
import streamlit as st
import base64
from process.dataViz import DataVisualization
from process.dataProcess import DataProcessing

# ------------------- PAGE SETUP ---------------------------
st.set_page_config(page_title="Break Ring Dashboard", layout='wide')

with open("assets/logoHuawei.png", "rb") as img_file:
    huawei_logo = base64.b64encode(img_file.read()).decode()

with open("assets/CDBLogo.png", "rb") as img_file:
    cd_logo = base64.b64encode(img_file.read()).decode()

st.markdown(
    f"""
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

# ------------------- UPLOAD FILE --------------------------
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

    st.markdown(f"""<hr>""", unsafe_allow_html=True)
# ------------------- DATA FILTER --------------------------
col1, col2 = st.columns([1, 3])

if st.session_state.new_df is not None and not st.session_state.new_df.empty:
    with col1:
        st.write("Filter")        
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
        
    with col2:
        st.dataframe(df_selection, hide_index=True)
        
    
    st.markdown(f"""<hr>""", unsafe_allow_html=True)
    DataVisualization(st.session_state.new_df)
