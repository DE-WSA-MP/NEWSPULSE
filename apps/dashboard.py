import json
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st


# -------------------------------------------------
# Add project root to Python path
# -------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from apps.pipeline import main as run_pipeline
from apps.analysis.trend_analysis import (
    main as run_trend_analysis
)


NEWS_DATA_FILE = (
    "data/processed/news_data.json"
)

TREND_DATA_FILE = (
    "data/processed/trend_analysis.json"
)


# -------------------------------------------------
# Page configuration
# -------------------------------------------------

st.set_page_config(
    page_title="NewsPulse",
    page_icon="📰",
    layout="wide"
)


# -------------------------------------------------
# Run live data acquisition
# -------------------------------------------------

def refresh_data():
    """Fetch fresh data and regenerate analysis."""

    run_pipeline()
    run_trend_analysis()

    st.cache_data.clear()


# -------------------------------------------------
# Load data
# -------------------------------------------------

@st.cache_data
def load_news_data():

    with open(
        NEWS_DATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


@st.cache_data
def load_trend_data():

    with open(
        TREND_DATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# -------------------------------------------------
# Initial live data fetch
# -------------------------------------------------

if "data_initialized" not in st.session_state:

    with st.spinner(
        "Fetching latest data from NASA, "
        "Wikipedia and Hacker News..."
    ):

        refresh_data()

    st.session_state.data_initialized = True

    st.session_state.last_refresh = (
        datetime.now()
    )


# -------------------------------------------------
# Refresh button
# -------------------------------------------------

refresh_col1, refresh_col2 = st.columns(
    [1, 5]
)

with refresh_col1:

    if st.button(
        "🔄 Refresh Data",
        use_container_width=True
    ):

        with st.spinner(
            "Fetching latest data..."
        ):

            refresh_data()

        st.session_state.last_refresh = (
            datetime.now()
        )

        st.rerun()


with refresh_col2:

    if "last_refresh" in st.session_state:

        st.caption(
            "Last refreshed: "
            + st.session_state.last_refresh.strftime(
                "%d %b %Y, %H:%M:%S"
            )
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
    "Multi-Source News Intelligence "
    "& Trend Analysis Platform"
)

st.write(
    "NewsPulse collects news and current-event "
    "data from multiple sources, processes the "
    "data, and identifies basic trends and patterns."
)


# -------------------------------------------------
# Summary metrics
# -------------------------------------------------

total_records = len(records)

source_counts = trend_data[
    "records_by_source"
]

nasa_count = source_counts.get(
    "NASA",
    0
)

wikipedia_count = source_counts.get(
    "Wikipedia",
    0
)

hackernews_count = source_counts.get(
    "Hacker News",
    0
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Records",
        total_records
    )


with col2:

    st.metric(
        "NASA",
        nasa_count
    )


with col3:

    st.metric(
        "Wikipedia",
        wikipedia_count
    )


with col4:

    st.metric(
        "Hacker News",
        hackernews_count
    )


st.divider()


# -------------------------------------------------
# Content type distribution
# -------------------------------------------------

st.header(
    "Content Type Distribution"
)

content_type_counts = trend_data[
    "records_by_content_type"
]

content_type_df = pd.DataFrame(
    list(
        content_type_counts.items()
    ),
    columns=[
        "Content Type",
        "Records"
    ]
)

content_type_df = (
    content_type_df.sort_values(
        "Records",
        ascending=False
    )
)

st.dataframe(
    content_type_df,
    use_container_width=True,
    hide_index=True
)


# -------------------------------------------------
# Topic distribution
# -------------------------------------------------

st.header(
    "Topic Distribution"
)

topic_counts = trend_data[
    "records_by_topic"
]

topic_df = pd.DataFrame(
    list(
        topic_counts.items()
    ),
    columns=[
        "Topic",
        "Records"
    ]
)

topic_df = topic_df.sort_values(
    "Records",
    ascending=False
)

st.dataframe(
    topic_df,
    use_container_width=True,
    hide_index=True
)


# -------------------------------------------------
# Records by date
# -------------------------------------------------

st.header(
    "Records by Date"
)

date_counts = trend_data[
    "records_by_date"
]

date_df = pd.DataFrame(
    list(
        date_counts.items()
    ),
    columns=[
        "Date",
        "Records"
    ]
)

date_df["Date"] = pd.to_datetime(
    date_df["Date"]
)

date_df = date_df.sort_values(
    "Date"
)

st.line_chart(
    date_df.set_index("Date")
)


# -------------------------------------------------
# Top keywords
# -------------------------------------------------

st.header(
    "Top Keywords"
)

keyword_data = trend_data[
    "top_keywords"
]

keyword_df = pd.DataFrame(
    keyword_data,
    columns=[
        "Keyword",
        "Frequency"
    ]
)

st.bar_chart(
    keyword_df.set_index(
        "Keyword"
    )
)


# -------------------------------------------------
# News Explorer
# -------------------------------------------------

st.header(
    "News Explorer"
)

available_sources = [
    "All"
] + sorted(
    df["source"]
    .dropna()
    .unique()
    .tolist()
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
    "content_type",
    "topic",
    "published_at",
    "url"
]

display_df = filtered_df[
    display_columns
].copy()

display_df.columns = [
    "Title",
    "Source",
    "Content Type",
    "Topic",
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

st.header(
    "Source-wise Trends"
)

source_keyword_data = trend_data[
    "top_keywords_by_source"
]


if selected_source == "All":

    for source, keywords in (
        source_keyword_data.items()
    ):

        st.subheader(source)

        keyword_source_df = pd.DataFrame(
            keywords,
            columns=[
                "Keyword",
                "Frequency"
            ]
        )

        st.bar_chart(
            keyword_source_df.set_index(
                "Keyword"
            )
        )

else:

    keywords = source_keyword_data.get(
        selected_source,
        []
    )

    if keywords:

        keyword_source_df = pd.DataFrame(
            keywords,
            columns=[
                "Keyword",
                "Frequency"
            ]
        )

        st.bar_chart(
            keyword_source_df.set_index(
                "Keyword"
            )
        )

    else:

        st.info(
            "No keyword data available "
            "for this source."
        )