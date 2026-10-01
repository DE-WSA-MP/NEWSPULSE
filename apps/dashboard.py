import json
import streamlit as st
import pandas as pd


NEWS_DATA_FILE = "data/processed/news_data.json"
TREND_DATA_FILE = "data/processed/trend_analysis.json"


# -------------------------------------------------
# Load data
# -------------------------------------------------

@st.cache_data
def load_news_data():
    with open(NEWS_DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


@st.cache_data
def load_trend_data():
    with open(TREND_DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# -------------------------------------------------
# Page configuration
# -------------------------------------------------

st.set_page_config(
    page_title="NewsPulse",
    page_icon="📰",
    layout="wide"
)


# -------------------------------------------------
# Load datasets
# -------------------------------------------------

records = load_news_data()
trend_data = load_trend_data()

df = pd.DataFrame(records)


# -------------------------------------------------
# Header
# -------------------------------------------------

st.title("📰 NewsPulse")
st.subheader(
    "Multi-Source News Intelligence & Trend Analysis Platform"
)

st.write(
    "NewsPulse collects news and current-event data from "
    "multiple sources, processes the data, and identifies "
    "basic trends and patterns."
)


# -------------------------------------------------
# Summary metrics
# -------------------------------------------------

total_records = len(records)

source_counts = trend_data["records_by_source"]

nasa_count = source_counts.get("NASA", 0)
wikipedia_count = source_counts.get("Wikipedia", 0)
hackernews_count = source_counts.get("Hacker News", 0)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Records", total_records)

with col2:
    st.metric("NASA", nasa_count)

with col3:
    st.metric("Wikipedia", wikipedia_count)

with col4:
    st.metric("Hacker News", hackernews_count)


st.divider()


# -------------------------------------------------
# Source analysis
# -------------------------------------------------

st.header("Source Distribution")

source_df = pd.DataFrame(
    list(source_counts.items()),
    columns=["Source", "Records"]
)

st.bar_chart(
    source_df.set_index("Source")
)


# -------------------------------------------------
# Category analysis
# -------------------------------------------------

st.header("Category Distribution")

category_counts = trend_data["records_by_category"]

category_df = pd.DataFrame(
    list(category_counts.items()),
    columns=["Category", "Records"]
)

st.bar_chart(
    category_df.set_index("Category")
)


# -------------------------------------------------
# Date analysis
# -------------------------------------------------

st.header("Records by Date")

date_counts = trend_data["records_by_date"]

date_df = pd.DataFrame(
    list(date_counts.items()),
    columns=["Date", "Records"]
)

date_df["Date"] = pd.to_datetime(date_df["Date"])

date_df = date_df.sort_values("Date")

st.line_chart(
    date_df.set_index("Date")
)


# -------------------------------------------------
# Keyword analysis
# -------------------------------------------------

st.header("Top Keywords")

keyword_data = trend_data["top_keywords"]

keyword_df = pd.DataFrame(
    keyword_data,
    columns=["Keyword", "Frequency"]
)

st.bar_chart(
    keyword_df.set_index("Keyword")
)


# -------------------------------------------------
# Source filter
# -------------------------------------------------

st.header("News Explorer")

available_sources = ["All"] + sorted(
    df["source"].dropna().unique().tolist()
)

selected_source = st.selectbox(
    "Filter by source",
    available_sources
)

if selected_source != "All":
    filtered_df = df[
        df["source"] == selected_source
    ].copy()
else:
    filtered_df = df.copy()


# -------------------------------------------------
# News table
# -------------------------------------------------

display_columns = [
    "title",
    "source",
    "category",
    "published_at",
    "url"
]

display_df = filtered_df[
    display_columns
].copy()

display_df.columns = [
    "Title",
    "Source",
    "Category",
    "Published At",
    "URL"
]

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# -------------------------------------------------
# Source-wise trends
# -------------------------------------------------

st.header("Source-wise Trends")

source_keyword_data = trend_data[
    "top_keywords_by_source"
]

if selected_source == "All":

    for source, keywords in source_keyword_data.items():

        st.subheader(source)

        keyword_source_df = pd.DataFrame(
            keywords,
            columns=["Keyword", "Frequency"]
        )

        st.bar_chart(
            keyword_source_df.set_index("Keyword")
        )

else:

    keywords = source_keyword_data.get(
        selected_source,
        []
    )

    if keywords:

        keyword_source_df = pd.DataFrame(
            keywords,
            columns=["Keyword", "Frequency"]
        )

        st.bar_chart(
            keyword_source_df.set_index("Keyword")
        )

    else:
        st.info(
            "No keyword data available for this source."
        )