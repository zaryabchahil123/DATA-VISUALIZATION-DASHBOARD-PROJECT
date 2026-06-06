NUMERIC_KPI_COLUMNS = ["mcg", "gvh", "alm", "mit", "vac", "nuc"]


def format_decimal(value):
    if value is None:
        return "0.000"
    return f"{value:.3f}"


def build_kpi_metrics(df, total_records=None):
    total_records = total_records if total_records is not None else len(df)
    filtered_count = len(df)
    coverage = (filtered_count / total_records * 100) if total_records else 0
    class_count = df["Class"].nunique() if "Class" in df.columns and not df.empty else 0
    dominant_class = "None"

    if "Class" in df.columns and not df.empty:
        dominant_class = df["Class"].value_counts().idxmax()

    metrics = [
        {"label": "Total Records", "value": f"{filtered_count}"},
        {"label": "Filtered Coverage", "value": f"{coverage:.1f}%"},
        {"label": "Classes Shown", "value": f"{class_count}"},
        {"label": "Dominant Class", "value": dominant_class},
    ]

    for column in NUMERIC_KPI_COLUMNS:
        average = df[column].mean() if column in df.columns and not df.empty else None
        metrics.append({"label": f"Average {column}", "value": format_decimal(average)})

    return metrics
