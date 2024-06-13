import pandas as pd
import plotly.express as px
import streamlit as st
import base64

# ------------------- PAGE SETUP ---------------------------
st.set_page_config(page_title="Break Ring Dashboard",
                   layout='wide',
                   )

# ---- HEADER WITH LOGOS ----
# Read the images as binary
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

# ------------------- UPLOAD FILE --------------------------
uploaded_file = st.file_uploader("", type=["xlsx"])

if uploaded_file:
    
    # ----------------- DATASET --------------------
    df = pd.read_excel(io=uploaded_file,
                    engine='openpyxl')
    
    df['Plan MOS'] = df['Plan MOS'].replace('May Plan', 'May')

    # ---- SIDEBAR ----
    st.sidebar.header("Please Filter Here:")
    ring_id = st.sidebar.multiselect(
        "Break Ring Status:",
        options=df['Break Ring Status'].unique(),
    )

    # ---------- DATA FILTERING -------------
    if ring_id:
        df_selection = df[df['Break Ring Status'].isin(ring_id)]
    else:
        df_selection = df.copy()

    # Display the filtered DataFrame in the Streamlit app
    st.dataframe(df_selection)
    
    # ---------- DATA VISUALIZATION -------------
    st.title("Dashboard", anchor=False)

    # ---- BREAK RING STATUS ----
    status_counts = df['Break Ring Status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']

    # Create a pie chart
    fig = px.pie(
        status_counts,
        names='Status',
        values='Count',
        title='Break Ring Status'
    )

    # Display the pie chart in the Streamlit app
    st.plotly_chart(fig)
    
    # ---- DATE COUNT ----    
    categories = {
        'Survey': ['Plan Survey', 'Actual Survey'],
        'MOS': ['Plan MOS', 'Actual MOS'],
        'Installation': ['Plan Installation', 'Actual Installation'],
        'PowerUp': ['Plan Power Up', 'Actual Power Up'],
        'Integration': ['Plan Integration', 'Actual Integration'],
        'Migration': ['Plan Migration', 'Actual Migration'],
    }

    def create_bar_graph(df, category, plan_col, actual_col):
        plan_counts = df[plan_col].value_counts().reset_index()
        plan_counts.columns = ['Month', 'Count']
        plan_counts['Type'] = plan_col

        actual_counts = df[actual_col].value_counts().reset_index()
        actual_counts.columns = ['Month', 'Count']
        actual_counts['Type'] = actual_col

        combined_counts = pd.concat([plan_counts, actual_counts])

        fig = px.bar(
            combined_counts,
            x='Month',
            y='Count',
            color='Type',
            barmode='group',
            title=f"{category} Plan vs Actual"
        )
        
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