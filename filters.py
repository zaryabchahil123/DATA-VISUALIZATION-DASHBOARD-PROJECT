import pandas as pd
import streamlit as st

YEAST_COLUMNS = ['Sequence_Name', 'mcg', 'gvh', 'alm', 'mit', 'erl', 'pox', 'vac', 'nuc', 'Class']
DISCRETE_MULTI_SELECT_COLUMNS = ["erl", "pox"]
FILTER_KEY_PREFIXES = ("filter_search", "filter_category_", "filter_values_", "filter_range_", "filter_date_")


def load_and_clean_data(filepath):
    df = pd.read_csv(filepath, sep=r'\s+', names=YEAST_COLUMNS)
    return df


def get_filterable_columns(df):
    numeric_columns = df.select_dtypes(include="number").columns.tolist()
    date_columns = df.select_dtypes(include=["datetime64[ns]", "datetimetz"]).columns.tolist()
    text_columns = [
        column for column in df.select_dtypes(include=["object", "string"]).columns
        if column != "Class"
    ]
    category_columns = [column for column in ["Class"] if column in df.columns]
    multi_select_columns = [
        column for column in DISCRETE_MULTI_SELECT_COLUMNS
        if column in numeric_columns and df[column].nunique(dropna=True) > 1
    ]

    return {
        "text": text_columns,
        "category": category_columns,
        "multi_select": multi_select_columns,
        "numeric": numeric_columns,
        "date": date_columns,
    }


def filter_dataframe(
    df,
    search_query="",
    selected_categories=None,
    selected_values=None,
    numeric_ranges=None,
    date_ranges=None,
):
    filtered_df = df.copy()
    selected_categories = selected_categories or {}
    selected_values = selected_values or {}
    numeric_ranges = numeric_ranges or {}
    date_ranges = date_ranges or {}

    if search_query:
        text_columns = get_filterable_columns(filtered_df)["text"]
        if text_columns:
            search_mask = pd.Series(False, index=filtered_df.index)
            for column in text_columns:
                search_mask = search_mask | filtered_df[column].str.contains(search_query, case=False, na=False)
            filtered_df = filtered_df[search_mask]

    for column, values in selected_categories.items():
        if column in filtered_df.columns and values:
            filtered_df = filtered_df[filtered_df[column].isin(values)]

    for column, values in selected_values.items():
        if column in filtered_df.columns and values:
            filtered_df = filtered_df[filtered_df[column].isin(values)]

    for column, value_range in numeric_ranges.items():
        if column in filtered_df.columns and value_range:
            lower_bound, upper_bound = value_range
            filtered_df = filtered_df[
                (filtered_df[column] >= lower_bound) &
                (filtered_df[column] <= upper_bound)
            ]

    for column, date_range in date_ranges.items():
        if column in filtered_df.columns and date_range and len(date_range) == 2:
            start_date, end_date = date_range
            filtered_df = filtered_df[
                (filtered_df[column] >= pd.Timestamp(start_date)) &
                (filtered_df[column] <= pd.Timestamp(end_date))
            ]

    return filtered_df


def reset_filter_state():
    for key in list(st.session_state.keys()):
        if key.startswith(FILTER_KEY_PREFIXES):
            del st.session_state[key]


def numeric_slider_bounds(series):
    min_value = float(series.min())
    max_value = float(series.max())
    if min_value == max_value:
        max_value = min_value + 0.01
    return min_value, max_value


def apply_filters(df):
    st.sidebar.header("Dashboard Filters")

    if st.sidebar.button("Reset Filters", use_container_width=True):
        reset_filter_state()
        st.rerun()

    orig_df = df.copy()
    filterable_columns = get_filterable_columns(orig_df)

    search_query = ""
    selected_categories = {}
    selected_values = {}
    numeric_ranges = {}
    date_ranges = {}

    if filterable_columns["text"]:
        search_query = st.sidebar.text_input(
            "Search Sequence Name",
            key="filter_search",
        )

    for column in filterable_columns["category"]:
        options = sorted(orig_df[column].dropna().unique().tolist())
        selected_categories[column] = st.sidebar.multiselect(
            "Protein Class",
            options=options,
            default=options,
            key=f"filter_category_{column}",
        )

    with st.sidebar.expander("Multi-Select Filters", expanded=True):
        for column in filterable_columns["multi_select"]:
            options = sorted(orig_df[column].dropna().unique().tolist())
            selected_values[column] = st.multiselect(
                f"{column} Values",
                options=options,
                default=options,
                key=f"filter_values_{column}",
            )

    with st.sidebar.expander("Numerical Range Filters", expanded=True):
        for column in filterable_columns["numeric"]:
            min_value, max_value = numeric_slider_bounds(orig_df[column])
            numeric_ranges[column] = st.slider(
                f"{column} Range",
                min_value=min_value,
                max_value=max_value,
                value=(min_value, max_value),
                step=0.01,
                format="%.2f",
                key=f"filter_range_{column}",
            )

    for column in filterable_columns["date"]:
        min_date = orig_df[column].min().date()
        max_date = orig_df[column].max().date()
        date_ranges[column] = st.sidebar.date_input(
            f"{column} Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key=f"filter_date_{column}",
        )

    return filter_dataframe(
        orig_df,
        search_query=search_query,
        selected_categories=selected_categories,
        selected_values=selected_values,
        numeric_ranges=numeric_ranges,
        date_ranges=date_ranges,
    )
