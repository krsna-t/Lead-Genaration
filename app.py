import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Lead Generator", layout="wide")

# ======= GLOBAL STYLING =======
st.markdown("""
    <style>
    .css-1d391kg, .css-1cypcdb {
        background-color: #111827 !important;
        color: white !important;
    }
    .st-c5 {
        color: #E5E7EB !important;
    }
    .st-emotion-cache-10trblm {
        font-size: 3rem;
        color: #38bdf8;
        text-shadow: 0 0 10px rgba(56, 189, 248, 0.6);
    }
    .stDownloadButton {
        background-color: #0ea5e9;
        color: white;
        border-radius: 10px;
        padding: 0.6em 1.2em;
        font-weight: bold;
    }
    .stDownloadButton:hover {
        background-color: #0369a1;
    }
    </style>
""", unsafe_allow_html=True)

# ======= TITLE =======
st.title("Lead Generation Engine")

# ======= LOAD DATA =======
@st.cache_data
def load_data():
    df = pd.read_csv("leads.csv", parse_dates=["ImportDate"])
    df["LeadScore"] = df["Frequency"].rank(ascending=False).astype(int) * 10
    return df.sort_values(by="LeadScore", ascending=False)

df = load_data()

# ======= SIDEBAR FILTERS =======
with st.sidebar:
    st.markdown("### \U0001F50D Filter Leads")

    with st.expander("Country Filter"):
        selected_countries = st.multiselect(
            "Choose Country(s)",
            options=sorted(df["Country"].unique()),
            default=sorted(df["Country"].unique())
        )

    with st.expander("Product Filter"):
        selected_products = st.multiselect(
            "Choose Motor Type",
            options=sorted(df["Product"].unique()),
            default=sorted(df["Product"].unique())
        )

    with st.expander("Competitor Filter"):
        selected_competitors = st.multiselect(
            "Choose Competitor(s)",
            options=sorted(df["Competitor"].unique()),
            default=[]
        )

    st.markdown("---")

# ======= FILTERING =======
filtered = df[
    df["Country"].isin(selected_countries) &
    df["Product"].isin(selected_products)
]
if selected_competitors:
    filtered = filtered[filtered["Competitor"].isin(selected_competitors)]

# ======= METRICS =======
st.markdown("###Summary Metrics")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Leads", len(filtered))
k2.metric("Avg Frequency", round(filtered["Frequency"].mean(), 2))
k3.metric("Top Product", filtered["Product"].mode()[0] if not filtered.empty else "N/A")
k4.metric("Top Supplier", filtered["Supplier"].mode()[0] if not filtered.empty else "N/A")

st.markdown("###Visualizations")

# ======= CHARTS =======
col1, col2 = st.columns(2)
with col1:
    st.subheader("Leads by Country")
    country_counts = filtered["Country"].value_counts()
    fig1 = px.bar(country_counts, title="Top Countries", labels={"index": "Country", "value": "Count"})
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    st.subheader("Product Distribution")
    product_counts = filtered["Product"].value_counts()
    fig2 = px.pie(names=product_counts.index, values=product_counts.values, title="Product Share")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
col3, col4 = st.columns(2)
with col3:
    st.subheader("Top Competitors")
    comp_counts = filtered["Competitor"].value_counts()
    fig3 = px.bar(comp_counts, title="Competitor Presence", labels={"index": "Competitor", "value": "Leads"})
    st.plotly_chart(fig3, use_container_width=True)
with col4:
    st.subheader("Top Industries")
    ind_counts = filtered["Industry"].value_counts()
    fig4 = px.bar(ind_counts, title="Industry Focus", labels={"index": "Industry", "value": "Leads"})
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
col5, col6 = st.columns(2)
with col5:
    st.subheader("\Top Suppliers")
    sup_counts = filtered["Supplier"].value_counts()
    fig5 = px.bar(sup_counts, title="Suppliers", labels={"index": "Supplier", "value": "Shipments"})
    st.plotly_chart(fig5, use_container_width=True)
with col6:
    st.subheader("Avg Frequency per Product")
    freq_product = filtered.groupby("Product")["Frequency"].mean().sort_values()
    fig6 = px.bar(freq_product, title="Frequency by Product", labels={"value": "Avg Frequency"})
    st.plotly_chart(fig6, use_container_width=True)

# ======= TABLE & DOWNLOAD =======
st.subheader("Filtered Lead Table")
st.dataframe(filtered, use_container_width=True)

csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button("Download Filtered CSV", csv, "filtered_leads.csv", "text/csv")
