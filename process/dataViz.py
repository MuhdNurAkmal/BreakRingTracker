import plotly.express as px
import streamlit as st
import pandas as pd
from datetime import datetime

def DataVisualization(df) :
    
    st.title("Dashboard", anchor=False)
    
    # ---- BREAK RING STATUS ----
    status_counts = df['Break Ring Status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']

    # Create a pie chart
    fig = px.pie(
        status_counts,
        names='Status',
        values='Count',
        title='Break Ring Status',
        hole=0.3
    )
    st.plotly_chart(fig)

    # ---- DATE COUNT ----    
    categories = {
        'Survey': ['Plan Survey', 'Actual Survey'],
        'MOS': ['Plan MOS', 'Actual MOS'],
        'PowerUp': ['Plan Power Up', 'Actual Power Up'],
        'Integration': ['Plan Integration', 'Actual Integration'],
        'Migration': ['Plan Migration', 'Actual Migration'],
    }

    def create_bar_graph(df, category, plan_col, actual_col):
        # Convert 'N/A' to NaN for proper handling
        df[plan_col] = pd.to_datetime(df[plan_col], errors='coerce')
        df[actual_col] = pd.to_datetime(df[actual_col], errors='coerce')
        
        # Convert Period objects to strings
        df[plan_col] = df[plan_col].dt.to_period('M').astype(str)
        df[actual_col] = df[actual_col].dt.to_period('M').astype(str)
        
        plan_counts = df[plan_col].value_counts().sort_index().reset_index()
        plan_counts.columns = ['Month', 'Count']
        plan_counts['Type'] = 'Plan'

        actual_counts = df[actual_col].value_counts().sort_index().reset_index()
        actual_counts.columns = ['Month', 'Count']
        actual_counts['Type'] = 'Actual'

        combined_counts = pd.concat([plan_counts, actual_counts])

        fig = px.bar(
            combined_counts,
            x='Month',
            y='Count',
            color='Type',
            barmode='group',
            title=f"{category} Plan vs Actual"
        )
        
        fig.update_xaxes(type='category') 
        
        return fig

    col1, col2 = st.columns(2)
    col_index = 0
    for category, (plan_col, actual_col) in categories.items():
        fig = create_bar_graph(df, category, plan_col, actual_col)
        if col_index % 2 == 0:
            col1.plotly_chart(fig)
        else:
            col2.plotly_chart(fig)
        col_index += 1