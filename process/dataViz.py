import plotly.express as px
import streamlit as st
import pandas as pd

class Dashboard:
    def __init__(self, df):
        self.df = df
        self.categories = {
            'Survey': ['Plan Survey', 'Actual Survey'],
            'MOS': ['Plan MOS', 'Actual MOS'],
            'Power Up': ['Plan Power Up', 'Actual Power Up'],
            'Integration': ['Plan Integration', 'Actual Integration'],
            'Migration': ['Plan Migration', 'Actual Migration']
        }
        
    def PieChart(self):
        status_counts = self.df['Break Ring Status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']

        fig = px.pie(
            status_counts,
            names='Status',
            values='Count',
            title='Break Ring Status',
            hole=0.3
        )
        
        st.plotly_chart(fig)

    def BarGraphGenerator(self, category, plan_col, actual_col):      
        self.df[plan_col] = pd.to_datetime(self.df[plan_col], errors='coerce')
        self.df[actual_col] = pd.to_datetime(self.df[actual_col], errors='coerce')
        
        self.df[plan_col] = self.df[plan_col].dt.to_period('M').astype(str)
        self.df[actual_col] = self.df[actual_col].dt.to_period('M').astype(str)
        
        plan_counts = self.df[plan_col].value_counts().sort_index().reset_index()
        plan_counts.columns = ['Month', 'Count']
        plan_counts['Type'] = 'Plan'

        actual_counts = self.df[actual_col].value_counts().sort_index().reset_index()
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
    
    def BarGraph(self):
        col1, col2 = st.columns(2)
        col_index = 0
        for category, (plan_col, actual_col) in self.categories.items():
            fig = self.BarGraphGenerator(category, plan_col, actual_col)
            if col_index % 2 == 0:
                col1.plotly_chart(fig)
            else:
                col2.plotly_chart(fig)
            col_index += 1
