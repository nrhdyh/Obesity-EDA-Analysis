import streamlit as st

st.set_page_config(
    page_title="Obesity Analysis App",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Obesity Level Analysis Application")

st.write(
    """
    Welcome to the Obesity Level Analysis Application.

    This application is developed to explore obesity-related data and provide
    interactive visual insights based on demographic, lifestyle, and health-related factors.
    """
)

st.subheader("Available Pages")

st.markdown(
    """
    - **Insights Dashboard**: Interactive dashboard with Plotly charts and filters.
    """
)

st.info("Use the sidebar menu to open the Insights Dashboard.")
