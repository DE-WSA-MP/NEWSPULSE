import json
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from apps.pipeline import main as run_pipeline
from apps.analysis.trend_analysis import (
    main as run_trend_analysis
)


# ============================================================
# DATA FILES
# ============================================================

NEWS_DATA_FILE = (
    "data/processed/news_data.json"
)

TREND_DATA_FILE = (
    "data/processed/trend_analysis.json"
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="NewsPulse",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# DARK MODE FRIENDLY CSS
# ============================================================

st.markdown(
    """
    <style>

    /* --------------------------------------------------------
       Main page
    -------------------------------------------------------- */

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* --------------------------------------------------------
       Headings
    -------------------------------------------------------- */

    h1 {
        color: #F5F7FA !important;
        font-weight: 750 !important;
        letter-spacing: -0.5px;
    }

    h2 {
        color: #F5F7FA !important;
        font-weight: 700 !important;
    }

    h3 {
        color: #F5F7FA !important;
        font-weight: 650 !important;
    }


    /* --------------------------------------------------------
       Paragraph text
    -------------------------------------------------------- */

    p {
        color: #D1D5DB;
    }


    /* --------------------------------------------------------
       Metric cards
    -------------------------------------------------------- */

    div[data-testid="stMetric"] {
        background-color: #171A21;
        border: 1px solid #2B303B;
        border-radius: 14px;
        padding: 1rem 1.1rem;
    }

    div[data-testid="stMetricLabel"] {
        color: #D1D5DB !important;
    }

    div[data-testid="stMetricValue"] {
        color: #F8FAFC !important;
        font-weight: 700 !important;
    }


    /* --------------------------------------------------------
       Buttons
    -------------------------------------------------------- */

    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }


    /* --------------------------------------------------------
       Article containers
    -------------------------------------------------------- */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px;
        border-color: #2B303B;
    }


    /* --------------------------------------------------------
       Sidebar
    -------------------------------------------------------- */

    section[data-testid="stSidebar"] {
        border-right: 1px solid #2B303B;
    }


    /* --------------------------------------------------------
       Captions
    -------------------------------------------------------- */

    div[data-testid="stCaptionContainer"] {
        color: #9CA3AF;
    }


    /* --------------------------------------------------------
       Links
    -------------------------------------------------------- */

    a {
        font-weight: 600;
    }


    /* --------------------------------------------------------
       Horizontal rule
    -------------------------------------------------------- */

    hr {
        border-color: #2B303B;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATA FUNCTIONS
# ============================================================

def refresh_data():
    """
    Fetch fresh data from NASA, Wikipedia and Hacker News,
    then regenerate trend analysis.
    """

    run_pipeline()
    run_trend_analysis()

    st.cache_data.clear()


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


# ============================================================
# INITIAL DATA FETCH
# ============================================================

if "data_initialized" not in st.session_state:

    # Use st.status instead of st.spinner.
    # This gives a much clearer loading experience.

    with st.status(
        "Fetching latest news...",
        expanded=True
    ) as status:

        st.write(
            "Collecting data from NASA, Wikipedia "
            "Current Events and Hacker News."
        )

        refresh_data()

        status.update(
            label="Latest news loaded successfully",
            state="complete",
            expanded=False
        )

    st.session_state.data_initialized = True

    st.session_state.last_refresh = datetime.now()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("📰 NewsPulse")

    st.caption(
        "Multi-source news intelligence dashboard"
    )

    st.divider()

    st.subheader("🔄 Data")

    if st.button(
        "Refresh Latest Data",
        use_container_width=True
    ):

        with st.status(
            "Refreshing NewsPulse...",
            expanded=True
        ) as status:

            st.write(
                "Fetching the latest records "
                "from all three sources."
            )

            refresh_data()

            status.update(
                label="Data refreshed successfully",
                state="complete",
                expanded=False
            )

        st.session_state.last_refresh = datetime.now()

        st.rerun()

    if "last_refresh" in st.session_state:

        st.caption(
            "Last refreshed: "
            + st.session_state.last_refresh.strftime(
                "%d %b %Y, %H:%M:%S"
            )
        )

    st.divider()

    st.subheader("🔎 Explorer Filters")

    st.caption(
        "Use the filters in News Explorer "
        "to find specific records."
    )


# ============================================================
# LOAD DATA
# ============================================================

records = load_news_data()

trend_data = load_trend_data()

df = pd.DataFrame(records)


# ============================================================
# ENSURE REQUIRED COLUMNS EXIST
# ============================================================

required_columns = [
    "id",
    "title",
    "description",
    "source",
    "published_at",
    "url",
    "content_type",
    "topic"
]

for column in required_columns:

    if column not in df.columns:

        df[column] = ""


# ============================================================
# HEADER
# ============================================================

st.title("📰 NewsPulse")

st.subheader(
    "Multi-Source News Intelligence & Trend Analysis"
)

st.write(
    "Collecting, processing and analyzing news from "
    "NASA, Wikipedia Current Events and Hacker News."
)


# ============================================================
# SUMMARY METRICS
# ============================================================

st.divider()

total_records = len(records)

source_counts = trend_data.get(
    "records_by_source",
    {}
)

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


# ONLY FOUR CARDS
# Topics card has been removed.

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


# ============================================================
# CONTENT OVERVIEW
# ============================================================

st.divider()

st.header("📊 Content Overview")

st.caption(
    "Distribution of content types and detected topics "
    "in the current dataset."
)


overview_col1, overview_col2 = st.columns(2)


# ------------------------------------------------------------
# CONTENT TYPES
# ------------------------------------------------------------

with overview_col1:

    st.subheader("Content Types")

    content_type_counts = trend_data.get(
        "records_by_content_type",
        {}
    )

    content_type_df = pd.DataFrame(
        list(content_type_counts.items()),
        columns=[
            "Content Type",
            "Records"
        ]
    )

    if not content_type_df.empty:

        content_type_df = (
            content_type_df
            .sort_values(
                "Records",
                ascending=True
            )
            .set_index("Content Type")
        )

        st.bar_chart(
            content_type_df,
            horizontal=True,
            use_container_width=True
        )

    else:

        st.info(
            "No content type data available."
        )


# ------------------------------------------------------------
# TOPICS TABLE
# ------------------------------------------------------------

with overview_col2:

    st.subheader("Topics")

    topic_counts = trend_data.get(
        "records_by_topic",
        {}
    )

    topic_df = pd.DataFrame(
        list(topic_counts.items()),
        columns=[
            "Topic",
            "Records"
        ]
    )

    if not topic_df.empty:

        topic_df = (
            topic_df
            .sort_values(
                "Records",
                ascending=False
            )
            .reset_index(drop=True)
        )

        # Add ranking
        topic_df.insert(
            0,
            "Rank",
            range(1, len(topic_df) + 1)
        )

        st.dataframe(
            topic_df,
            use_container_width=True,
            hide_index=True,
            height=420
        )

    else:

        st.info(
            "No topic data available."
        )
# ============================================================
# NEWS ACTIVITY OVER TIME
# ============================================================

st.divider()

st.header("📅 News Activity Over Time")

st.caption(
    "Number of records acquired for each publication date."
)

date_counts = trend_data.get(
    "records_by_date",
    {}
)

date_df = pd.DataFrame(
    list(date_counts.items()),
    columns=[
        "Date",
        "Records"
    ]
)

if not date_df.empty:

    date_df["Date"] = pd.to_datetime(
        date_df["Date"],
        errors="coerce"
    )

    date_df = date_df.dropna(
        subset=["Date"]
    )

    date_df = date_df.sort_values(
        "Date"
    )

    st.line_chart(
        date_df.set_index("Date"),
        use_container_width=True
    )

else:

    st.info(
        "No date information available."
    )


# ============================================================
# TRENDING KEYWORDS
# ============================================================

st.divider()

st.header("🔥 Trending Keywords")

st.caption(
    "Most frequently occurring keywords across "
    "the integrated dataset."
)

keyword_data = trend_data.get(
    "top_keywords",
    []
)

keyword_df = pd.DataFrame(
    keyword_data,
    columns=[
        "Keyword",
        "Frequency"
    ]
)

if not keyword_df.empty:

    keyword_df = keyword_df.head(15)

    keyword_chart_df = (
        keyword_df
        .sort_values(
            "Frequency",
            ascending=True
        )
        .set_index("Keyword")
    )

    st.bar_chart(
        keyword_chart_df,
        horizontal=True,
        use_container_width=True
    )

else:

    st.info(
        "No keyword data available."
    )


# ============================================================
# SOURCE-WISE TRENDS
#
# IMPORTANT:
# This section is intentionally BEFORE News Explorer.
# ============================================================

st.divider()

st.header("📈 Source-wise Trends")

st.caption(
    "Most frequent keywords identified for each news source."
)


source_keyword_data = trend_data.get(
    "top_keywords_by_source",
    {}
)


if source_keyword_data:

    source_names = list(
        source_keyword_data.keys()
    )

    source_tabs = st.tabs(
        source_names
    )

    for tab, (source, keywords) in zip(
        source_tabs,
        source_keyword_data.items()
    ):

        with tab:

            keyword_source_df = pd.DataFrame(
                keywords,
                columns=[
                    "Keyword",
                    "Frequency"
                ]
            )

            if not keyword_source_df.empty:

                keyword_source_df = (
                    keyword_source_df
                    .head(10)
                    .sort_values(
                        "Frequency",
                        ascending=True
                    )
                    .set_index("Keyword")
                )

                st.bar_chart(
                    keyword_source_df,
                    horizontal=True,
                    use_container_width=True
                )

            else:

                st.info(
                    f"No keyword data available for {source}."
                )

else:

    st.info(
        "No source-wise trend data available."
    )


# ============================================================
# NEWS EXPLORER
#
# This now comes AFTER Source-wise Trends.
# ============================================================

st.divider()

st.header("🔎 News Explorer")

st.caption(
    "Search and filter the latest records collected by NewsPulse."
)


# ============================================================
# FILTERS
# ============================================================

filter_col1, filter_col2, filter_col3, filter_col4 = (
    st.columns(4)
)


# ------------------------------------------------------------
# SOURCE
# ------------------------------------------------------------

available_sources = [
    "All"
] + sorted(
    [
        source
        for source in (
            df["source"]
            .fillna("")
            .astype(str)
            .str.strip()
            .unique()
        )
        if source
    ]
)

with filter_col1:

    selected_source = st.selectbox(
        "Source",
        available_sources
    )


# ------------------------------------------------------------
# TOPIC
# ------------------------------------------------------------

topic_values = sorted(
    [
        topic
        for topic in (
            df["topic"]
            .fillna("")
            .astype(str)
            .str.strip()
            .unique()
        )
        if topic
    ]
)

available_topics = [
    "All"
] + topic_values

with filter_col2:

    selected_topic = st.selectbox(
        "Topic",
        available_topics
    )


# ------------------------------------------------------------
# CONTENT TYPE
# ------------------------------------------------------------

content_type_values = sorted(
    [
        content_type
        for content_type in (
            df["content_type"]
            .fillna("")
            .astype(str)
            .str.strip()
            .unique()
        )
        if content_type
    ]
)

available_content_types = [
    "All"
] + content_type_values

with filter_col3:

    selected_content_type = st.selectbox(
        "Content Type",
        available_content_types
    )


# ------------------------------------------------------------
# SEARCH
# ------------------------------------------------------------

with filter_col4:

    search_text = st.text_input(
        "Search",
        placeholder="Search news..."
    )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()


if selected_source != "All":

    filtered_df = filtered_df[
        filtered_df["source"]
        == selected_source
    ]


if selected_topic != "All":

    filtered_df = filtered_df[
        filtered_df["topic"]
        .fillna("")
        .astype(str)
        .str.strip()
        == selected_topic
    ]


if selected_content_type != "All":

    filtered_df = filtered_df[
        filtered_df["content_type"]
        .fillna("")
        .astype(str)
        .str.strip()
        == selected_content_type
    ]


if search_text.strip():

    search_lower = search_text.lower()

    title_mask = (
        filtered_df["title"]
        .fillna("")
        .astype(str)
        .str.lower()
        .str.contains(
            search_lower,
            na=False
        )
    )

    description_mask = (
        filtered_df["description"]
        .fillna("")
        .astype(str)
        .str.lower()
        .str.contains(
            search_lower,
            na=False
        )
    )

    topic_mask = (
        filtered_df["topic"]
        .fillna("")
        .astype(str)
        .str.lower()
        .str.contains(
            search_lower,
            na=False
        )
    )

    filtered_df = filtered_df[
        title_mask
        | description_mask
        | topic_mask
    ]


# ============================================================
# RESULT COUNT
# ============================================================

st.caption(
    f"Showing {len(filtered_df)} of "
    f"{len(df)} records"
)


# ============================================================
# NEWS ARTICLES
# ============================================================

if filtered_df.empty:

    st.info(
        "No news records match the selected filters."
    )

else:

    for _, row in filtered_df.iterrows():

        title = str(
            row.get(
                "title",
                "Untitled"
            )
        )

        source = str(
            row.get(
                "source",
                ""
            )
        )

        topic = str(
            row.get(
                "topic",
                ""
            )
        ).strip()

        content_type = str(
            row.get(
                "content_type",
                ""
            )
        ).strip()

        published_at = str(
            row.get(
                "published_at",
                ""
            )
        )

        description = str(
            row.get(
                "description",
                ""
            )
        )

        url = str(
            row.get(
                "url",
                ""
            )
        )


        # ----------------------------------------------------
        # ARTICLE CARD
        # ----------------------------------------------------

        with st.container(
            border=True
        ):

            st.subheader(
                title
            )

            st.caption(
                f"{source}  •  {published_at}"
            )


            # ------------------------------------------------
            # TOPIC + CONTENT TYPE
            # ------------------------------------------------

            badge_col1, badge_col2, badge_col3 = (
                st.columns([2, 2, 6])
            )


            with badge_col1:

                if topic:

                    st.info(
                        f"🏷️ {topic}"
                    )

                else:

                    st.caption(
                        "🏷️ No topic"
                    )


            with badge_col2:

                if content_type:

                    st.success(
                        f"📄 {content_type}"
                    )

                else:

                    st.caption(
                        "📄 Unknown type"
                    )


            # ------------------------------------------------
            # DESCRIPTION
            # ------------------------------------------------

            if description:

                if len(description) > 350:

                    display_description = (
                        description[:350]
                        + "..."
                    )

                else:

                    display_description = description

                st.write(
                    display_description
                )

            else:

                st.caption(
                    "No description available."
                )


            # ------------------------------------------------
            # ARTICLE LINK
            # ------------------------------------------------

            if url:

                st.link_button(
                    "Read Article →",
                    url
                )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "NewsPulse · Multi-Source News Intelligence "
    "& Trend Analysis Platform"
)

st.caption(
    "NASA · Wikipedia Current Events · Hacker News"
)