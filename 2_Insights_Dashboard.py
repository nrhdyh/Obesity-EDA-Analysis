import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Insights Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Load Dataset
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/nrhdyh/Obesity-EDA-Analysis/refs/heads/main/ObesityDataSet_raw_and_data_sinthetic.csv")
    return df

df = load_data()

# -----------------------------
# Page Title
# -----------------------------
st.title("📊 Insights Dashboard")
st.write(
    "This dashboard provides interactive visual insights from the obesity dataset. "
    "Users can filter the data and explore patterns related to obesity levels, "
    "physical characteristics, and lifestyle habits."
)

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔎 Filter Options")

gender_filter = st.sidebar.multiselect(
    "Select Gender",
    options=sorted(df["Gender"].unique()),
    default=sorted(df["Gender"].unique())
)

obesity_filter = st.sidebar.multiselect(
    "Select Obesity Level",
    options=sorted(df["NObeyesdad"].unique()),
    default=sorted(df["NObeyesdad"].unique())
)

transport_filter = st.sidebar.multiselect(
    "Select Transportation Mode",
    options=sorted(df["MTRANS"].unique()),
    default=sorted(df["MTRANS"].unique())
)

age_range = st.sidebar.slider(
    "Select Age Range",
    min_value=int(df["Age"].min()),
    max_value=int(df["Age"].max()),
    value=(int(df["Age"].min()), int(df["Age"].max()))
)

# -----------------------------
# Apply Filters
# -----------------------------
filtered_df = df[
    (df["Gender"].isin(gender_filter)) &
    (df["NObeyesdad"].isin(obesity_filter)) &
    (df["MTRANS"].isin(transport_filter)) &
    (df["Age"] >= age_range[0]) &
    (df["Age"] <= age_range[1])
]

# -----------------------------
# Key Metrics
# -----------------------------
st.subheader("📌 Dataset Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", filtered_df.shape[0])
col2.metric("Average Age", round(filtered_df["Age"].mean(), 2))
col3.metric("Average Weight", round(filtered_df["Weight"].mean(), 2))
col4.metric("Average Height", round(filtered_df["Height"].mean(), 2))

st.divider()

# -----------------------------
# Row 1 Charts
# -----------------------------
chart1, chart2 = st.columns(2)

with chart1:
    st.subheader("Obesity Level Distribution")

    obesity_count = filtered_df["NObeyesdad"].value_counts().reset_index()
    obesity_count.columns = ["Obesity Level", "Count"]

    fig1 = px.bar(
        obesity_count,
        x="Obesity Level",
        y="Count",
        text="Count",
        title="Distribution of Obesity Levels"
    )

    fig1.update_layout(
        xaxis_tickangle=-45,
        height=450
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.caption(
        "This chart shows the number of respondents in each obesity category."
    )

with chart2:
    st.subheader("Gender Distribution")

    gender_count = filtered_df["Gender"].value_counts().reset_index()
    gender_count.columns = ["Gender", "Count"]

    fig2 = px.pie(
        gender_count,
        names="Gender",
        values="Count",
        title="Gender Distribution",
        hole=0.4
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.caption(
        "This chart shows the proportion of male and female respondents."
    )

st.divider()

# -----------------------------
# Row 2 Charts
# -----------------------------
chart3, chart4 = st.columns(2)

with chart3:
    st.subheader("Weight by Obesity Level")

    fig3 = px.box(
        filtered_df,
        x="NObeyesdad",
        y="Weight",
        color="NObeyesdad",
        title="Weight Distribution by Obesity Level"
    )

    fig3.update_layout(
        xaxis_tickangle=-45,
        showlegend=False,
        height=450
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.caption(
        "Higher obesity categories generally show higher weight values."
    )

with chart4:
    st.subheader("Age vs Weight")

    fig4 = px.scatter(
        filtered_df,
        x="Age",
        y="Weight",
        color="NObeyesdad",
        hover_data=["Gender", "Height", "FAF", "TUE"],
        title="Age vs Weight by Obesity Level"
    )

    fig4.update_layout(height=450)

    st.plotly_chart(fig4, use_container_width=True)

    st.caption(
        "This scatter plot shows the relationship between age and weight."
    )

st.divider()

# -----------------------------
# Row 3 Charts
# -----------------------------
chart5, chart6 = st.columns(2)

with chart5:
    st.subheader("Physical Activity by Obesity Level")

    fig5 = px.box(
        filtered_df,
        x="NObeyesdad",
        y="FAF",
        color="NObeyesdad",
        title="Physical Activity Frequency by Obesity Level"
    )

    fig5.update_layout(
        xaxis_tickangle=-45,
        showlegend=False,
        height=450
    )

    st.plotly_chart(fig5, use_container_width=True)

    st.caption(
        "Physical activity varies across obesity levels, but the pattern is weaker compared to weight."
    )

with chart6:
    st.subheader("Technology Usage by Obesity Level")

    fig6 = px.box(
        filtered_df,
        x="NObeyesdad",
        y="TUE",
        color="NObeyesdad",
        title="Technology Usage Time by Obesity Level"
    )

    fig6.update_layout(
        xaxis_tickangle=-45,
        showlegend=False,
        height=450
    )

    st.plotly_chart(fig6, use_container_width=True)

    st.caption(
        "Technology usage time shows variation but does not clearly separate obesity levels."
    )

st.divider()

# -----------------------------
# Correlation Heatmap
# -----------------------------
st.subheader("Correlation Heatmap")

numeric_cols = filtered_df.select_dtypes(include=["float64", "int64"]).columns

if len(numeric_cols) > 1 and filtered_df.shape[0] > 1:
    corr = filtered_df[numeric_cols].corr()

    fig7 = px.imshow(
        corr,
        text_auto=True,
        title="Correlation Matrix of Numerical Features",
        color_continuous_scale="RdBu_r",
        aspect="auto"
    )

    fig7.update_layout(height=650)

    st.plotly_chart(fig7, use_container_width=True)

    st.caption(
        "The correlation heatmap shows relationships between numerical variables. "
        "Weight is one of the most important features related to obesity classification."
    )
else:
    st.warning("Not enough data to generate correlation heatmap.")

st.divider()

# -----------------------------
# Data Preview
# -----------------------------
with st.expander("View Filtered Data"):
    st.dataframe(filtered_df, use_container_width=True)

# -----------------------------
# Insights Summary
# -----------------------------
st.subheader("Key Insights")

st.write(
    """
    Based on the dashboard, weight shows the clearest difference across obesity levels.
    Higher obesity categories generally have higher weight values compared to normal and insufficient weight groups.
    Family history, eating habits, physical activity, and technology usage also provide useful lifestyle context,
    although their patterns are weaker compared to weight.
    """
)
