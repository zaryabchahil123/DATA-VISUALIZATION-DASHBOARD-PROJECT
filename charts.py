import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def style_chart(fig, ax):
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    ax.tick_params(colors='#8a95a5', which='both')
    ax.xaxis.label.set_color('#8a95a5')
    ax.yaxis.label.set_color('#8a95a5')
    ax.title.set_color('#8a95a5')
    for spine in ax.spines.values():
        spine.set_color('#8a95a5')
    ax.grid(True, color='#8a95a5', linestyle='--', linewidth=0.5, alpha=0.3)

def plot_pie_chart(df):
    class_counts = df['Class'].value_counts()
    total = class_counts.sum()
    threshold = 0.03 * total
    large_classes = class_counts[class_counts >= threshold]
    small_classes_sum = class_counts[class_counts < threshold].sum()
    if small_classes_sum > 0:
        if 'Other' in large_classes:
            large_classes['Other'] += small_classes_sum
        else:
            large_classes['Other'] = small_classes_sum
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    wedges, texts, autotexts = ax.pie(
        large_classes,
        labels=large_classes.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=sns.color_palette("muted"),
        pctdistance=0.75,
        wedgeprops=dict(width=0.35, edgecolor='#8a95a5', alpha=0.9)
    )
    for text in texts:
        text.set_fontsize(10)
        text.set_color('#8a95a5')
    for autotext in autotexts:
        autotext.set_fontsize(9)
        autotext.set_weight('bold')
        autotext.set_color('white')
    ax.set_title("Class Distribution", fontsize=14, pad=20, color='#8a95a5')
    return fig

def plot_histogram(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    style_chart(fig, ax)
    sns.histplot(df['mcg'], bins=30, kde=True, ax=ax, color='#3498db')
    ax.set_title("Distribution of mcg Feature", fontsize=14, pad=15)
    ax.set_xlabel("mcg Value", fontsize=12)
    ax.set_ylabel("Frequency", fontsize=12)
    sns.despine(ax=ax)
    return fig

def plot_line_chart(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    style_chart(fig, ax)
    df_sorted = df.sort_values(by='mcg').reset_index(drop=True)
    sns.lineplot(data=df_sorted, x=df_sorted.index, y='gvh', ax=ax, color='#e74c3c')
    ax.set_title("gvh Trend sorted by mcg", fontsize=14, pad=15)
    ax.set_xlabel("Sequence Index", fontsize=12)
    ax.set_ylabel("gvh Value", fontsize=12)
    sns.despine(ax=ax)
    return fig

def plot_bar_chart(df):
    class_avg = df.groupby('Class')['alm'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    style_chart(fig, ax)
    sns.barplot(data=class_avg, x='Class', y='alm', hue='Class', ax=ax, palette="viridis", legend=False)
    ax.set_title("Average alm Score per Class", fontsize=14, pad=15)
    ax.set_xlabel("Class", fontsize=12)
    ax.set_ylabel("Average alm Value", fontsize=12)
    plt.xticks(rotation=45)
    sns.despine(ax=ax)
    return fig

def plot_scatter_plot(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    style_chart(fig, ax)
    sns.scatterplot(data=df, x='mcg', y='gvh', hue='Class', ax=ax, palette="Set1")
    ax.set_title("mcg vs gvh Scatter Plot", fontsize=14, pad=15)
    ax.set_xlabel("mcg", fontsize=12)
    ax.set_ylabel("gvh", fontsize=12)
    ax.legend(title="Class", bbox_to_anchor=(1.05, 1), loc='upper left')
    sns.despine(ax=ax)
    return fig

def plot_box_plot(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    style_chart(fig, ax)
    sns.boxplot(data=df, x='Class', y='nuc', hue='Class', ax=ax, palette="deep", legend=False)
    ax.set_title("nuc Score Spread across Classes", fontsize=14, pad=15)
    ax.set_xlabel("Class", fontsize=12)
    ax.set_ylabel("nuc Value", fontsize=12)
    plt.xticks(rotation=45)
    sns.despine(ax=ax)
    return fig

def plot_heatmap(df):
    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    corr = numeric_df.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax, fmt=".2f", cbar=True, annot_kws={"color": "white"})
    ax.tick_params(colors='#8a95a5', which='both')
    ax.title.set_color('#8a95a5')
    cbar = ax.collections[0].colorbar
    cbar.ax.yaxis.set_tick_params(color='#8a95a5')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#8a95a5')
    ax.set_title("Correlation Matrix of Numerical Features", fontsize=14, pad=15)
    return fig

def plot_area_chart(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    style_chart(fig, ax)
    df_sorted = df.sort_values(by='mcg').reset_index(drop=True)
    df_sorted['mit'].plot(kind='area', ax=ax, alpha=0.4, color='#2ecc71')
    ax.set_title("Cumulative mit Values sorted by mcg", fontsize=14, pad=15)
    ax.set_xlabel("Sequence Index", fontsize=12)
    ax.set_ylabel("mit Value", fontsize=12)
    sns.despine(ax=ax)
    return fig

def plot_count_plot(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    style_chart(fig, ax)
    sns.countplot(data=df, x='erl', hue='erl', ax=ax, palette="Set2", legend=False)
    ax.set_title("Count of erl Categories", fontsize=14, pad=15)
    ax.set_xlabel("erl", fontsize=12)
    ax.set_ylabel("Count", fontsize=12)
    sns.despine(ax=ax)
    return fig

def plot_violin_plot(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    style_chart(fig, ax)
    sns.violinplot(data=df, x='Class', y='vac', hue='Class', ax=ax, palette="muted", legend=False)
    ax.set_title("vac Distribution and Probability Density by Class", fontsize=14, pad=15)
    ax.set_xlabel("Class", fontsize=12)
    ax.set_ylabel("vac Value", fontsize=12)
    plt.xticks(rotation=45)
    sns.despine(ax=ax)
    return fig

def plot_bubble_chart(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    style_chart(fig, ax)
    sizes = df['vac'] * 500 + 50
    sns.scatterplot(
        data=df,
        x='mcg',
        y='gvh',
        hue='Class',
        size=sizes,
        sizes=(20, 500),
        ax=ax,
        palette="Set1",
        alpha=0.7
    )
    ax.set_title("mcg vs gvh Bubble Chart (Size = vac)", fontsize=14, pad=15)
    ax.set_xlabel("mcg", fontsize=12)
    ax.set_ylabel("gvh", fontsize=12)
    ax.legend(title="Class", bbox_to_anchor=(1.05, 1), loc='upper left')
    sns.despine(ax=ax)
    return fig
