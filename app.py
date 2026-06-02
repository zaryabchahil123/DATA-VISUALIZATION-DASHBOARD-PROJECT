import streamlit as st
from filters import load_and_clean_data, apply_filters
from charts import (plot_pie_chart, plot_histogram, plot_line_chart, 
                    plot_bar_chart, plot_scatter_plot, plot_box_plot, 
                    plot_heatmap, plot_area_chart, plot_count_plot, 
                    plot_violin_plot, plot_bubble_chart)

st.set_page_config(page_title="Yeast Data Dashboard", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

html, body, p, div, label, span {
    font-family: 'Inter', sans-serif;
}

.title-container {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    padding: 35px;
    border-radius: 15px;
    text-align: center;
    color: white;
    box-shadow: 0 10px 25px rgba(30, 60, 114, 0.15);
    margin-bottom: 30px;
}

.title-container h1 {
    font-size: 2.8rem;
    font-weight: 800;
    margin: 0;
    color: white;
}

.title-container p {
    font-size: 1.1rem;
    font-weight: 300;
    margin: 10px 0 0 0;
    color: #e0e6ed;
}

.kpi-card {
    background-color: var(--secondary-background-color);
    color: var(--text-color);
    border-radius: 12px;
    border: 1px solid rgba(128, 128, 128, 0.15);
    padding: 20px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    transition: transform 0.3s ease;
}

.kpi-card:hover {
    transform: translateY(-5px);
}

.kpi-label {
    font-size: 0.9rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    opacity: 0.8;
}

.kpi-value {
    font-size: 2.2rem;
    font-weight: 700;
    margin-top: 5px;
    color: var(--primary-color);
}

.tab-content {
    padding: 20px 0;
}

.chart-caption {
    text-align: center;
    margin-top: -10px;
    margin-bottom: 25px;
}

.chart-caption strong {
    font-size: 1.1rem;
    display: block;
    margin-bottom: 3px;
}

.chart-caption span {
    font-size: 0.9rem;
    opacity: 0.85;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="title-container">
    <h1>🧬 Yeast Data Visualization Dashboard</h1>
    <p>A Professional Exploratory Analysis of Yeast Protein Localization Sites</p>
</div>
""", unsafe_allow_html=True)

df_raw = load_and_clean_data("data/yeast.data")
df_filtered = apply_filters(df_raw)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Records</div>
        <div class="kpi-value">{len(df_filtered)}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    val = f"{df_filtered['mcg'].mean():.3f}" if not df_filtered.empty else "0.000"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Average mcg Score</div>
        <div class="kpi-value">{val}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    val = f"{df_filtered['gvh'].mean():.3f}" if not df_filtered.empty else "0.000"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Average gvh Score</div>
        <div class="kpi-value">{val}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if df_filtered.empty:
    st.warning("No data matches the current filters. Please adjust the filters in the sidebar.")
else:
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Overview", "Distributions", "Trends", "Relationships (Bonus)", "Correlations", "Raw Data Table"
    ])
    
    with tab1:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.pyplot(plot_pie_chart(df_filtered))
            st.markdown("""
            <div class="chart-caption">
                <strong>Pie Chart</strong>
                <span>Proportional distribution of localization classes</span>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.pyplot(plot_count_plot(df_filtered))
            st.markdown("""
            <div class="chart-caption">
                <strong>Count Plot</strong>
                <span>Frequency count of erl categories</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
            
    with tab2:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.pyplot(plot_histogram(df_filtered))
            st.markdown("""
            <div class="chart-caption">
                <strong>Histogram</strong>
                <span>Display frequency distribution of mcg scores</span>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.pyplot(plot_box_plot(df_filtered))
            st.markdown("""
            <div class="chart-caption">
                <strong>Box Plot</strong>
                <span>Data spread, median, and outliers of nuc scores</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.pyplot(plot_violin_plot(df_filtered))
        st.markdown("""
        <div class="chart-caption">
            <strong>Violin Plot</strong>
            <span>Distribution and probability density of vac scores by class</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
            
    with tab3:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.pyplot(plot_line_chart(df_filtered))
            st.markdown("""
            <div class="chart-caption">
                <strong>Line Chart</strong>
                <span>Trends of gvh scores over sequence</span>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.pyplot(plot_area_chart(df_filtered))
            st.markdown("""
            <div class="chart-caption">
                <strong>Area Chart</strong>
                <span>Cumulative trends of mit scores over sequence</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab4:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.pyplot(plot_scatter_plot(df_filtered))
            st.markdown("""
            <div class="chart-caption">
                <strong>Scatter Plot</strong>
                <span>Relationship between mcg and gvh scores</span>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.pyplot(plot_bubble_chart(df_filtered))
            st.markdown("""
            <div class="chart-caption">
                <strong>Bubble Chart (Bonus)</strong>
                <span>Three-dimensional relationship between mcg, gvh, and vac</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
            
    with tab5:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.pyplot(plot_heatmap(df_filtered))
            st.markdown("""
            <div class="chart-caption">
                <strong>Heatmap</strong>
                <span>Correlation matrix of all numerical features</span>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.pyplot(plot_bar_chart(df_filtered))
            st.markdown("""
            <div class="chart-caption">
                <strong>Bar Chart</strong>
                <span>Average alm score across protein localization classes</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab6:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        st.dataframe(df_filtered, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)
