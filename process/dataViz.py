import plotly.express as px
import plotly.graph_objects as go
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
        self.config = {'staticPlot': False}
        
    def PieChart(self):
        status_counts = self.df['Break Ring Status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        
        color_sequence = px.colors.qualitative.G10
        
        fig = px.pie(
            status_counts,
            names='Status',
            values='Count',
            title='Break Ring Status',
            hole=0.3,
            color_discrete_sequence=color_sequence,
        )
        
        st.plotly_chart(fig, config=self.config)

    def BarGraphGenerator(self, category, plan_col, actual_col):
        dff = self.df.copy()
        dff[plan_col] = pd.to_datetime(dff[plan_col], errors='coerce')
        dff[actual_col] = pd.to_datetime(dff[actual_col], errors='coerce')
              
        dff[plan_col] = dff[plan_col].dt.to_period('M').astype(str)
        dff[actual_col] = dff[actual_col].dt.to_period('M').astype(str)
        
        plan_counts = dff[plan_col].value_counts().sort_index().reset_index()
        plan_counts.columns = ['Month', 'Count']
        plan_counts['Type'] = 'Plan'

        actual_counts = dff[actual_col].value_counts().sort_index().reset_index()
        actual_counts.columns = ['Month', 'Count']
        actual_counts['Type'] = 'Actual'

        combined_counts = pd.concat([plan_counts, actual_counts])
        color_sequence = px.colors.qualitative.T10
        
        fig = px.bar(
            combined_counts,
            x='Month',
            y='Count',
            color='Type',
            barmode='group',
            title=f'Plan vs Actual : {category}',
            color_discrete_sequence=color_sequence
        )
        
        fig.update_xaxes(type='category', title_text='Month')
        fig.update_yaxes(title_text='Number of Activities')
        
        return fig
    
    def BarGraph(self):
        col1, col2 = st.columns(2)
        col_index = 0
        
        for category, (plan_col, actual_col) in self.categories.items():
            fig = self.BarGraphGenerator(category, plan_col, actual_col)
            if col_index % 2 == 0:
                col1.plotly_chart(fig, config=self.config)
            else:
                col2.plotly_chart(fig, config=self.config)
            col_index += 1
    
    def HorizontalBarGraph(self):
        geography = ['State', 'Region']
        colors = {
            'State': 'rgba(0, 128, 128, 0.6)',
            'Region': 'rgba(255, 127, 80, 0.6)'
        }
        line_colors = {
            'State': 'rgba(0, 128, 128, 1.0)',
            'Region': 'rgba(255, 127, 80, 1.0)'
        }

        for geo_level in geography:
            if geo_level in self.df.columns:
                filtered_df = self.df[~self.df[geo_level].isin(["N/A", "TBA"])]
                count = filtered_df[geo_level].value_counts().sort_values(ascending=True)
                geo = count.index

                na_count = self.df[self.df[geo_level] == "N/A"].shape[0]
                tba_count = self.df[self.df[geo_level] == "TBA"].shape[0]

                fig = go.Figure()

                fig.add_trace(go.Bar(
                    x=count,
                    y=geo,
                    text=count,
                    textposition='outside',
                    textfont=dict(size=14, color='black', family='Arial'),
                    marker=dict(
                        color=colors[geo_level],
                        line=dict(
                            color=line_colors[geo_level],
                            width=1
                        )
                    ),
                    orientation='h',
                ))

                fig.update_layout(
                    title=f'Number of Activities Across {geo_level}',
                    xaxis_title='Number of Activities',
                    yaxis_title=geo_level,
                    template='simple_white',
                    bargap=0.2
                )

                col1, col2, col3 = st.columns([9, 1, 2])
                
                col1.plotly_chart(fig, config=self.config)

                with col3:
                    st.html("<div style='padding-top: 10em;'>")
                    st.metric(f"Not Available", na_count)
                    st.metric(f"To Be Announced", tba_count)
                    st.html("</div>")