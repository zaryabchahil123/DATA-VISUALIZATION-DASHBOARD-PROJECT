import pandas as pd
import streamlit as st

def load_and_clean_data(filepath):
    column_names = ['Sequence_Name', 'mcg', 'gvh', 'alm', 'mit', 'erl', 'pox', 'vac', 'nuc', 'Class']
    df = pd.read_csv(filepath, sep=r'\s+', names=column_names)
    return df

def apply_filters(df):
    st.sidebar.header("Dashboard Filters")
    
    if st.sidebar.button("Reset Filters"):
        st.session_state.clear()
        st.rerun()

    orig_df = df.copy()

    search_query = st.sidebar.text_input("Search by Sequence Name", key="search_query")
    if search_query:
        df = df[df['Sequence_Name'].str.contains(search_query, case=False, na=False)]

    classes = sorted(orig_df['Class'].unique())
    selected_classes = st.sidebar.multiselect("Select Protein Class", options=classes, default=classes, key="selected_classes")
    if selected_classes:
        df = df[df['Class'].isin(selected_classes)]

    mcg_min = float(orig_df['mcg'].min())
    mcg_max = float(orig_df['mcg'].max())
    if mcg_min == mcg_max:
        mcg_max += 0.01
    mcg_range = st.sidebar.slider("mcg Range", min_value=mcg_min, max_value=mcg_max, value=(mcg_min, mcg_max), key="mcg_range")
    df = df[(df['mcg'] >= mcg_range[0]) & (df['mcg'] <= mcg_range[1])]

    gvh_min = float(orig_df['gvh'].min())
    gvh_max = float(orig_df['gvh'].max())
    if gvh_min == gvh_max:
        gvh_max += 0.01
    gvh_range = st.sidebar.slider("gvh Range", min_value=gvh_min, max_value=gvh_max, value=(gvh_min, gvh_max), key="gvh_range")
    df = df[(df['gvh'] >= gvh_range[0]) & (df['gvh'] <= gvh_range[1])]

    return df
