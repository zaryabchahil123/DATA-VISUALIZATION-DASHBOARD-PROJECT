import re

import pandas as pd


NUMERIC_COLUMNS = ["mcg", "gvh", "alm", "mit", "erl", "pox", "vac", "nuc"]
COLUMN_ALIASES = {"mxg": "mcg"}
SUGGESTED_QUESTIONS = [
    "How many records are shown?",
    "Which class is dominant?",
    "Show class distribution",
    "What is the average mcg?",
    "Which class has the highest average alm?",
    "What is the correlation between mcg and gvh?",
    "Interpret this filtered data",
]


def answer_data_question(question, df, total_records=None):
    question_text = normalize_question(question)
    total_records = total_records if total_records is not None else len(df)

    if df.empty:
        return "No rows match the current filters, so there is not enough data to interpret yet."

    if asks_for_class_distribution(question_text):
        return class_distribution_answer(df)

    if asks_for_dominant_class(question_text):
        return dominant_class_answer(df)

    if asks_for_highest_class_average(question_text):
        column = first_numeric_column(question_text) or "mcg"
        return highest_class_average_answer(df, column)

    if asks_for_correlation(question_text):
        columns = mentioned_numeric_columns(question_text)
        if len(columns) >= 2:
            return correlation_answer(df, columns[0], columns[1])
        return strongest_correlation_answer(df)

    if asks_for_average(question_text):
        column = first_numeric_column(question_text) or "mcg"
        return average_answer(df, column)

    if asks_for_minimum_or_maximum(question_text):
        column = first_numeric_column(question_text) or "mcg"
        return range_answer(df, column)

    if asks_for_count(question_text):
        return count_answer(df, total_records)

    if asks_for_interpretation(question_text):
        return interpretation_answer(df, total_records)

    return (
        "I could not match that question to a supported data format. "
        "Please try one of the popup questions, such as: "
        f"{'; '.join(SUGGESTED_QUESTIONS)}."
    )


def normalize_question(question):
    return str(question or "").strip().lower()


def asks_for_count(question):
    return "how many" in question or has_any_word(question, ["records", "rows", "count"])


def asks_for_average(question):
    return has_any_word(question, ["average", "mean", "avg"])


def asks_for_highest_class_average(question):
    return asks_for_average(question) and "class" in question and any(
        has_word(question, term) for term in ["highest", "top", "largest", "best", "maximum", "max"]
    )


def asks_for_correlation(question):
    return has_any_word(question, ["correlation", "relationship", "related", "relate"])


def asks_for_class_distribution(question):
    return "class" in question and any(
        has_word(question, term) for term in ["distribution", "breakdown", "share", "percentage", "percent"]
    )


def asks_for_minimum_or_maximum(question):
    return has_any_word(question, ["minimum", "min", "maximum", "max", "range"])


def asks_for_interpretation(question):
    return has_any_word(question, ["interpret", "insight", "summary", "explain", "overview"])


def asks_for_dominant_class(question):
    return "class" in question and has_any_word(question, ["dominant", "largest", "common", "most"])


def has_any_word(question, words):
    return any(has_word(question, word) for word in words)


def has_word(question, word):
    return re.search(rf"\b{re.escape(word)}\b", question) is not None


def mentioned_numeric_columns(question):
    columns = []
    for alias, column in COLUMN_ALIASES.items():
        if re.search(rf"\b{re.escape(alias)}\b", question) and column not in columns:
            columns.append(column)
    for column in NUMERIC_COLUMNS:
        if re.search(rf"\b{re.escape(column)}\b", question) and column not in columns:
            columns.append(column)
    return columns


def first_numeric_column(question):
    columns = mentioned_numeric_columns(question)
    return columns[0] if columns else None


def count_answer(df, total_records):
    coverage = len(df) / total_records * 100 if total_records else 0
    return f"The current filters show {len(df)} records, which is {coverage:.1f}% of the full dataset."


def average_answer(df, column):
    if column not in df.columns:
        return f"I could not find a numeric column named {column} in this dataset."
    return f"The average {column} score in the current filtered data is {df[column].mean():.3f}."


def range_answer(df, column):
    if column not in df.columns:
        return f"I could not find a numeric column named {column} in this dataset."
    return (
        f"For {column}, the current filtered data ranges from {df[column].min():.3f} "
        f"to {df[column].max():.3f}, with a median of {df[column].median():.3f}."
    )


def class_distribution_answer(df):
    counts = df["Class"].value_counts()
    total = len(df)
    parts = [
        f"{class_name}: {count} ({count / total * 100:.1f}%)"
        for class_name, count in counts.head(6).items()
    ]
    return "Class distribution in the current filtered data: " + "; ".join(parts) + "."


def dominant_class_answer(df):
    counts = df["Class"].value_counts()
    class_name = counts.index[0]
    count = counts.iloc[0]
    share = count / len(df) * 100
    return f"The dominant class is {class_name} with {count} rows ({share:.1f}% of the current filtered data)."


def highest_class_average_answer(df, column):
    if column not in df.columns:
        return f"I could not find a numeric column named {column} in this dataset."
    grouped = df.groupby("Class")[column].mean().sort_values(ascending=False)
    class_name = grouped.index[0]
    class_rows = len(df[df["Class"] == class_name])
    return (
        f"{class_name} has the highest average {column} at {grouped.iloc[0]:.3f} "
        f"across {class_rows} rows."
    )


def correlation_answer(df, first_column, second_column):
    if first_column not in df.columns or second_column not in df.columns:
        return "I could not find both numeric columns in this dataset."
    correlation = df[first_column].corr(df[second_column])
    if pd.isna(correlation):
        return f"There is not enough variation to calculate correlation between {first_column} and {second_column}."
    return (
        f"The correlation between {first_column} and {second_column} is {correlation:.3f}, "
        f"which is a {correlation_label(correlation)} relationship."
    )


def strongest_correlation_answer(df):
    strongest = strongest_numeric_correlation(df)
    if strongest is None:
        return "There is not enough numeric variation to calculate a meaningful correlation."
    first_column, second_column, correlation = strongest
    return (
        f"The strongest numeric relationship is {first_column} vs {second_column} "
        f"with a correlation of {correlation:.3f}, a {correlation_label(correlation)} relationship."
    )


def interpretation_answer(df, total_records):
    coverage = len(df) / total_records * 100 if total_records else 0
    class_counts = df["Class"].value_counts()
    dominant_class = class_counts.index[0]
    dominant_count = class_counts.iloc[0]
    dominant_share = dominant_count / len(df) * 100
    strongest = strongest_numeric_correlation(df)
    relationship_sentence = "The strongest numeric relationship could not be calculated from this filtered slice."

    if strongest is not None:
        first_column, second_column, correlation = strongest
        relationship_sentence = (
            f"The strongest numeric relationship is {first_column} vs {second_column} "
            f"at {correlation:.3f}, a {correlation_label(correlation)} relationship."
        )

    return (
        f"The current filters show {len(df)} rows ({coverage:.1f}% of the full dataset). "
        f"The dominant class is {dominant_class} with {dominant_count} rows ({dominant_share:.1f}%). "
        f"Average mcg is {df['mcg'].mean():.3f} and average gvh is {df['gvh'].mean():.3f}. "
        f"{relationship_sentence}"
    )


def strongest_numeric_correlation(df):
    numeric_df = df[[column for column in NUMERIC_COLUMNS if column in df.columns]]
    if len(numeric_df) < 2 or numeric_df.shape[1] < 2:
        return None

    corr = numeric_df.corr()
    best_pair = None
    best_abs_value = -1

    for index, first_column in enumerate(corr.columns):
        for second_column in corr.columns[index + 1:]:
            value = corr.loc[first_column, second_column]
            if pd.isna(value):
                continue
            if abs(value) > best_abs_value:
                best_abs_value = abs(value)
                best_pair = (first_column, second_column, value)

    return best_pair


def correlation_label(value):
    magnitude = abs(value)
    direction = "positive" if value >= 0 else "negative"
    if magnitude >= 0.7:
        strength = "strong"
    elif magnitude >= 0.4:
        strength = "moderate"
    elif magnitude >= 0.2:
        strength = "weak"
    else:
        strength = "very weak"
    return f"{strength} {direction}"
