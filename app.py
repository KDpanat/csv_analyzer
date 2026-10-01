import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


st.title("CSV Analyzer")

st.write("Upload a CSV file to analyze your data.")


# -------------------------
# Upload CSV
# -------------------------

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"]
)


if uploaded_file is not None:

    # Read CSV
    df = pd.read_csv(uploaded_file)

    st.success("CSV uploaded successfully!")

    # -------------------------
    # Dataset Preview
    # -------------------------

    st.subheader("Dataset Preview")

    st.dataframe(df.head(10))


    # -------------------------
    # Dataset Overview
    # -------------------------

    st.subheader("Dataset Overview")

    rows = df.shape[0]
    columns = df.shape[1]

    missing_values = df.isnull().sum().sum()

    duplicate_rows = df.duplicated().sum()


    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", rows)

    col2.metric("Columns", columns)

    col3.metric("Missing Values", missing_values)

    col4.metric("Duplicate Rows", duplicate_rows)


    # -------------------------
    # Column Information
    # -------------------------

    st.subheader("Column Information")

    column_info = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Missing Values": df.isnull().sum().values,
        "Unique Values": df.nunique().values
    })

    st.dataframe(column_info)

    # -------------------------
# Column Type Analysis
# -------------------------

st.subheader("Column Type Analysis")

numeric_columns = df.select_dtypes(include="number").columns.tolist()

categorical_columns = df.select_dtypes(include="object").columns.tolist()


col1, col2 = st.columns(2)

with col1:
    st.write("### Numerical Columns")
    st.write(numeric_columns)

with col2:
    st.write("### Categorical Columns")
    st.write(categorical_columns)

# -------------------------
# Missing Value Analysis
# -------------------------

st.subheader("Missing Value Analysis")

missing_data = pd.DataFrame({
    "Column": df.columns,
    "Missing Values": df.isnull().sum().values,
    "Missing %": (df.isnull().sum().values / len(df) * 100).round(2)
})

st.dataframe(missing_data)


# -------------------------
# Duplicate Analysis
# -------------------------

st.subheader("Duplicate Analysis")

duplicate_count = df.duplicated().sum()

if duplicate_count == 0:
    st.success("No duplicate rows found!")
else:
    st.warning(f"{duplicate_count} duplicate rows found.")

    st.write("Duplicate Rows:")
    st.dataframe(df[df.duplicated()])

# -------------------------
# Statistical Summary
# -------------------------

st.subheader("Statistical Summary")

st.dataframe(df.describe())

# -------------------------
# Histogram
# -------------------------



st.subheader("Histogram")

if len(numeric_columns) > 0:

    selected_column = st.selectbox(
        "Select a numerical column",
        numeric_columns,
        key="histogram_column"
    )

    fig, ax = plt.subplots()

    ax.hist(df[selected_column].dropna(), bins=20)

    ax.set_xlabel(selected_column)
    ax.set_ylabel("Frequency")
    ax.set_title(f"Distribution of {selected_column}")

    st.pyplot(fig)

else:
    st.info("No numerical columns available.")

# -------------------------
# Box Plot
# -------------------------

st.subheader("Box Plot")

if len(numeric_columns) > 0:

    selected_box_column = st.selectbox(
        "Select a numerical column",
        numeric_columns,
        key="boxplot_column"
    )

    fig, ax = plt.subplots()

    ax.boxplot(df[selected_box_column].dropna())

    ax.set_ylabel(selected_box_column)
    ax.set_title(f"Box Plot of {selected_box_column}")

    st.pyplot(fig)

else:
    st.info("No numerical columns available.")

# -------------------------
# Categorical Analysis
# -------------------------

st.subheader("Categorical Analysis")

if len(categorical_columns) > 0:

    selected_category = st.selectbox(
        "Select a categorical column",
        categorical_columns,
        key="categorical_column"
    )

    value_counts = df[selected_category].value_counts()

    st.write(f"Value Counts for **{selected_category}**")

    st.dataframe(
        value_counts.reset_index().rename(
            columns={
                "index": selected_category,
                "count": "Count"
            }
        )
    )

    # -------------------------
    # Bar Chart
    # -------------------------

    st.write(f"Distribution of **{selected_category}**")

    fig, ax = plt.subplots()

    ax.bar(
        value_counts.index.astype(str),
        value_counts.values
    )

    ax.set_xlabel(selected_category)
    ax.set_ylabel("Count")
    ax.set_title(f"{selected_category} Distribution")

    plt.xticks(rotation=45)

    st.pyplot(fig)

else:
    st.info("No categorical columns available.")

# -------------------------
# Scatter Plot
# -------------------------

st.subheader("Scatter Plot")

if len(numeric_columns) >= 2:

    col1, col2 = st.columns(2)

    with col1:
        x_column = st.selectbox(
            "Select X-axis",
            numeric_columns,
            key="scatter_x"
        )

    with col2:
        y_column = st.selectbox(
            "Select Y-axis",
            numeric_columns,
            key="scatter_y"
        )

    fig, ax = plt.subplots()

    ax.scatter(
        df[x_column],
        df[y_column]
    )

    ax.set_xlabel(x_column)
    ax.set_ylabel(y_column)
    ax.set_title(f"{x_column} vs {y_column}")

    st.pyplot(fig)

else:
    st.info("At least two numerical columns are required.")

# -------------------------
# Correlation Analysis
# -------------------------

st.subheader("Correlation Analysis")

if len(numeric_columns) >= 2:

    correlation_matrix = df[numeric_columns].corr()

    st.write("Correlation Matrix")

    st.dataframe(correlation_matrix.round(2))

else:
    st.info("At least two numerical columns are required.")

# -------------------------
# Correlation Heatmap
# -------------------------

st.write("Correlation Heatmap")

fig, ax = plt.subplots()

im = ax.imshow(correlation_matrix, cmap="coolwarm")

ax.set_xticks(range(len(correlation_matrix.columns)))
ax.set_yticks(range(len(correlation_matrix.columns)))

ax.set_xticklabels(correlation_matrix.columns, rotation=45, ha="right")
ax.set_yticklabels(correlation_matrix.columns)

for i in range(len(correlation_matrix)):
    for j in range(len(correlation_matrix)):
        ax.text(
            j,
            i,
            f"{correlation_matrix.iloc[i, j]:.2f}",
            ha="center",
            va="center"
        )

fig.colorbar(im)

ax.set_title("Correlation Heatmap")

st.pyplot(fig)

# -------------------------
# Correlation Heatmap
# -------------------------

st.write("Correlation Heatmap")

fig, ax = plt.subplots()

im = ax.imshow(correlation_matrix, cmap="coolwarm")

ax.set_xticks(range(len(correlation_matrix.columns)))
ax.set_yticks(range(len(correlation_matrix.columns)))

ax.set_xticklabels(correlation_matrix.columns, rotation=45, ha="right")
ax.set_yticklabels(correlation_matrix.columns)

for i in range(len(correlation_matrix)):
    for j in range(len(correlation_matrix)):
        ax.text(
            j,
            i,
            f"{correlation_matrix.iloc[i, j]:.2f}",
            ha="center",
            va="center"
        )

fig.colorbar(im)

ax.set_title("Correlation Heatmap")

st.pyplot(fig)

# -------------------------
# Missing Value Handling
# -------------------------

st.write("### Handle Missing Values")

missing_count = df.isnull().sum().sum()

st.write(f"Total missing values: **{missing_count}**")

if missing_count > 0:

    missing_action = st.selectbox(
        "Choose an action",
        [
            "Do Nothing",
            "Remove Rows with Missing Values",
            "Fill Numerical Values with Mean",
            "Fill Numerical Values with Median"
        ]
    )

    if missing_action == "Remove Rows with Missing Values":

        df = df.dropna()

        st.success("Rows containing missing values were removed.")

    elif missing_action == "Fill Numerical Values with Mean":

        for column in numeric_columns:
            df[column] = df[column].fillna(df[column].mean())

        st.success(
            "Missing numerical values were filled with the mean."
        )

    elif missing_action == "Fill Numerical Values with Median":

        for column in numeric_columns:
            df[column] = df[column].fillna(df[column].median())

        st.success(
            "Missing numerical values were filled with the median."
        )

else:

    st.success("No missing values found!")

# =========================================================
# DATA CLEANING
# =========================================================

st.header("13️⃣ Data Cleaning")


# =========================================================
# REMOVE DUPLICATE ROWS
# =========================================================

st.subheader("Remove Duplicate Rows")

duplicate_count = df.duplicated().sum()

st.write(
    f"Duplicate rows found: **{duplicate_count}**"
)

if duplicate_count > 0:

    if st.button("Remove Duplicate Rows"):

        df = df.drop_duplicates()

        st.success(
            f"{duplicate_count} duplicate rows removed!"
        )

else:

    st.success("No duplicate rows to remove.")


# =========================================================
# MISSING VALUE HANDLING
# =========================================================

st.subheader("Handle Missing Values")

missing_count = df.isnull().sum().sum()

st.write(
    f"Total missing values: **{missing_count}**"
)

if missing_count > 0:

    missing_action = st.selectbox(
        "Choose an action",
        [
            "Do Nothing",
            "Remove Rows with Missing Values",
            "Fill Numerical Values with Mean",
            "Fill Numerical Values with Median"
        ],
        key="missing_action"
    )

    if missing_action == "Remove Rows with Missing Values":

        if st.button(
            "Remove Rows with Missing Values"
        ):

            df = df.dropna()

            st.success(
                "Rows containing missing values were removed."
            )

    elif missing_action == "Fill Numerical Values with Mean":

        if st.button(
            "Fill Missing Values with Mean"
        ):

            for column in numeric_columns:

                df[column] = df[column].fillna(
                    df[column].mean()
                )

            st.success(
                "Missing numerical values were filled with the mean."
            )

    elif missing_action == "Fill Numerical Values with Median":

        if st.button(
            "Fill Missing Values with Median"
        ):

            for column in numeric_columns:

                df[column] = df[column].fillna(
                    df[column].median()
                )

            st.success(
                "Missing numerical values were filled with the median."
            )

else:

    st.success("No missing values to handle.")


# =========================================================
# OUTLIER DETECTION
# =========================================================

st.subheader("Outlier Detection")

if len(numeric_columns) > 0:

    outlier_column = st.selectbox(
        "Select a numerical column",
        numeric_columns,
        key="outlier_column"
    )

    # First quartile
    Q1 = df[outlier_column].quantile(0.25)

    # Third quartile
    Q3 = df[outlier_column].quantile(0.75)

    # Interquartile Range
    IQR = Q3 - Q1

    # Lower and upper limits
    lower_limit = Q1 - 1.5 * IQR

    upper_limit = Q3 + 1.5 * IQR

    # Find outliers
    outliers = df[
        (df[outlier_column] < lower_limit)
        |
        (df[outlier_column] > upper_limit)
    ]

    st.write(
        f"Lower limit: **{lower_limit:.2f}**"
    )

    st.write(
        f"Upper limit: **{upper_limit:.2f}**"
    )

    st.write(
        f"Outliers found: **{len(outliers)}**"
    )

    if len(outliers) > 0:

        with st.expander("View Outliers"):

            st.dataframe(
                outliers,
                use_container_width=True
            )

        if st.button("Remove Outliers"):

            df = df[
                (df[outlier_column] >= lower_limit)
                &
                (df[outlier_column] <= upper_limit)
            ]

            st.success(
                f"{len(outliers)} outliers removed!"
            )

    else:

        st.success(
            "No outliers found in this column."
        )

else:

    st.info(
        "No numerical columns available for outlier detection."
    )


# =========================================================
# DATA FILTERING
# =========================================================

st.header("14️⃣ Data Filtering")

filter_column = st.selectbox(
    "Select a column to filter",
    df.columns,
    key="filter_column"
)


# ---------------------------------------------------------
# Categorical Column Filtering
# ---------------------------------------------------------

if df[filter_column].dtype == "object":

    filter_values = st.multiselect(
        "Select values",
        df[filter_column]
        .dropna()
        .unique()
        .tolist(),
        key="filter_values"
    )

    if filter_values:

        filtered_df = df[
            df[filter_column].isin(filter_values)
        ]

    else:

        filtered_df = df


# ---------------------------------------------------------
# Numerical Column Filtering
# ---------------------------------------------------------

else:

    min_value = float(
        df[filter_column].min()
    )

    max_value = float(
        df[filter_column].max()
    )

    selected_range = st.slider(
        "Select range",
        min_value,
        max_value,
        (min_value, max_value),
        key="filter_range"
    )

    filtered_df = df[
        df[filter_column].between(
            selected_range[0],
            selected_range[1]
        )
    ]


st.write(
    f"Showing **{len(filtered_df)}** rows."
)

st.dataframe(
    filtered_df,
    use_container_width=True
)


# =========================================================
# AUTOMATIC INSIGHTS
# =========================================================

st.header("15️⃣ Automatic Insights")


# ---------------------------------------------------------
# Numerical Insights
# ---------------------------------------------------------

if len(numeric_columns) > 0:

    st.subheader("Numerical Insights")

    for column in numeric_columns:

        mean_value = df[column].mean()

        max_value = df[column].max()

        min_value = df[column].min()

        st.write(
            f"**{column}** → "
            f"Mean: `{mean_value:.2f}`, "
            f"Minimum: `{min_value:.2f}`, "
            f"Maximum: `{max_value:.2f}`"
        )


# ---------------------------------------------------------
# Categorical Insights
# ---------------------------------------------------------

if len(categorical_columns) > 0:

    st.subheader("Categorical Insights")

    for column in categorical_columns:

        if df[column].notna().any():

            most_common = (
                df[column]
                .mode()
                .iloc[0]
            )

            st.write(
                f"**{column}** → "
                f"Most common value: `{most_common}`"
            )


# =========================================================
# DOWNLOAD DATASET
# =========================================================

st.header("16️⃣ Download Dataset")

csv_data = df.to_csv(
    index=False
)

st.download_button(
    label="⬇️ Download Current Dataset",
    data=csv_data,
    file_name="cleaned_dataset.csv",
    mime="text/csv"
)

# =========================================================
# DATA CLEANING
# =========================================================

st.header("13️⃣ Data Cleaning")


# =========================================================
# REMOVE DUPLICATE ROWS
# =========================================================

st.subheader("Remove Duplicate Rows")

duplicate_count = df.duplicated().sum()

st.write(
    f"Duplicate rows found: **{duplicate_count}**"
)

if duplicate_count > 0:

    if st.button("Remove Duplicate Rows", key="remove_duplicate_rows"):

        df = df.drop_duplicates()

        st.success(
            f"{duplicate_count} duplicate rows removed!"
        )

else:

    st.success("No duplicate rows to remove.")


# =========================================================
# MISSING VALUE HANDLING
# =========================================================

st.subheader("Handle Missing Values")

missing_count = df.isnull().sum().sum()

st.write(
    f"Total missing values: **{missing_count}**"
)

if missing_count > 0:

    missing_action = st.selectbox(
        "Choose an action",
        [
            "Do Nothing",
            "Remove Rows with Missing Values",
            "Fill Numerical Values with Mean",
            "Fill Numerical Values with Median"
        ],
        key="missing_action"
    )

    if missing_action == "Remove Rows with Missing Values":

        if st.button(
            "Remove Rows with Missing Values"
        ):

            df = df.dropna()

            st.success(
                "Rows containing missing values were removed."
            )

    elif missing_action == "Fill Numerical Values with Mean":

        if st.button(
            "Fill Missing Values with Mean"
        ):

            for column in numeric_columns:

                df[column] = df[column].fillna(
                    df[column].mean()
                )

            st.success(
                "Missing numerical values were filled with the mean."
            )

    elif missing_action == "Fill Numerical Values with Median":

        if st.button(
            "Fill Missing Values with Median"
        ):

            for column in numeric_columns:

                df[column] = df[column].fillna(
                    df[column].median()
                )

            st.success(
                "Missing numerical values were filled with the median."
            )

else:

    st.success("No missing values to handle.")


# =========================================================
# OUTLIER DETECTION
# =========================================================

st.subheader("Outlier Detection")

if len(numeric_columns) > 0:

    outlier_column = st.selectbox(
        "Select a numerical column",
        numeric_columns,
        key="outlier_column"
    )

    # First quartile
    Q1 = df[outlier_column].quantile(0.25)

    # Third quartile
    Q3 = df[outlier_column].quantile(0.75)

    # Interquartile Range
    IQR = Q3 - Q1

    # Lower and upper limits
    lower_limit = Q1 - 1.5 * IQR

    upper_limit = Q3 + 1.5 * IQR

    # Find outliers
    outliers = df[
        (df[outlier_column] < lower_limit)
        |
        (df[outlier_column] > upper_limit)
    ]

    st.write(
        f"Lower limit: **{lower_limit:.2f}**"
    )

    st.write(
        f"Upper limit: **{upper_limit:.2f}**"
    )

    st.write(
        f"Outliers found: **{len(outliers)}**"
    )

    if len(outliers) > 0:

        with st.expander("View Outliers"):

            st.dataframe(
                outliers,
                use_container_width=True
            )

        if st.button("Remove Outliers"):

            df = df[
                (df[outlier_column] >= lower_limit)
                &
                (df[outlier_column] <= upper_limit)
            ]

            st.success(
                f"{len(outliers)} outliers removed!"
            )

    else:

        st.success(
            "No outliers found in this column."
        )

else:

    st.info(
        "No numerical columns available for outlier detection."
    )


# =========================================================
# DATA FILTERING
# =========================================================

st.header("14️⃣ Data Filtering")

filter_column = st.selectbox(
    "Select a column to filter",
    df.columns,
    key="filter_column"
)


# ---------------------------------------------------------
# Categorical Column Filtering
# ---------------------------------------------------------

if df[filter_column].dtype == "object":

    filter_values = st.multiselect(
        "Select values",
        df[filter_column]
        .dropna()
        .unique()
        .tolist(),
        key="filter_values"
    )

    if filter_values:

        filtered_df = df[
            df[filter_column].isin(filter_values)
        ]

    else:

        filtered_df = df


# ---------------------------------------------------------
# Numerical Column Filtering
# ---------------------------------------------------------

else:

    min_value = float(
        df[filter_column].min()
    )

    max_value = float(
        df[filter_column].max()
    )

    selected_range = st.slider(
        "Select range",
        min_value,
        max_value,
        (min_value, max_value),
        key="filter_range"
    )

    filtered_df = df[
        df[filter_column].between(
            selected_range[0],
            selected_range[1]
        )
    ]


st.write(
    f"Showing **{len(filtered_df)}** rows."
)

st.dataframe(
    filtered_df,
    use_container_width=True
)


# =========================================================
# AUTOMATIC INSIGHTS
# =========================================================

st.header("15️⃣ Automatic Insights")


# ---------------------------------------------------------
# Numerical Insights
# ---------------------------------------------------------

if len(numeric_columns) > 0:

    st.subheader("Numerical Insights")

    for column in numeric_columns:

        mean_value = df[column].mean()

        max_value = df[column].max()

        min_value = df[column].min()

        st.write(
            f"**{column}** → "
            f"Mean: `{mean_value:.2f}`, "
            f"Minimum: `{min_value:.2f}`, "
            f"Maximum: `{max_value:.2f}`"
        )


# ---------------------------------------------------------
# Categorical Insights
# ---------------------------------------------------------

if len(categorical_columns) > 0:

    st.subheader("Categorical Insights")

    for column in categorical_columns:

        if df[column].notna().any():

            most_common = (
                df[column]
                .mode()
                .iloc[0]
            )

            st.write(
                f"**{column}** → "
                f"Most common value: `{most_common}`"
            )


# =========================================================
# DOWNLOAD DATASET
# =========================================================

st.header("16️⃣ Download Dataset")

csv_data = df.to_csv(
    index=False
)

st.download_button(
    label="⬇️ Download Current Dataset",
    data=csv_data,
    file_name="cleaned_dataset.csv",
    mime="text/csv"
)


# =========================================================
# 18. ADVANCED AUTOMATIC INSIGHTS
# =========================================================

st.header("18️⃣ Advanced Automatic Insights")


# ---------------------------------------------------------
# Dataset Size
# ---------------------------------------------------------

st.subheader("📊 Dataset Summary")

st.write(
    f"Your dataset contains **{len(df)} rows** "
    f"and **{len(df.columns)} columns**."
)


# ---------------------------------------------------------
# Missing Value Insight
# ---------------------------------------------------------

missing_counts = df.isnull().sum()

if missing_counts.sum() > 0:

    column_with_most_missing = (
        missing_counts.idxmax()
    )

    highest_missing_count = (
        missing_counts.max()
    )

    st.warning(
        f"⚠️ `{column_with_most_missing}` has the "
        f"highest number of missing values: "
        f"**{highest_missing_count}**."
    )

else:

    st.success(
        "✅ The dataset contains no missing values."
    )


# ---------------------------------------------------------
# Duplicate Insight
# ---------------------------------------------------------

duplicate_count = df.duplicated().sum()

if duplicate_count > 0:

    st.warning(
        f"⚠️ The dataset contains "
        f"**{duplicate_count} duplicate rows**."
    )

else:

    st.success(
        "✅ No duplicate rows detected."
    )


# ---------------------------------------------------------
# Numerical Insights
# ---------------------------------------------------------

if len(numeric_columns) > 0:

    st.subheader("📈 Numerical Insights")

    for column in numeric_columns:

        mean_value = df[column].mean()

        median_value = df[column].median()

        min_value = df[column].min()

        max_value = df[column].max()

        st.write(
            f"**{column}** → "
            f"Mean: `{mean_value:.2f}`, "
            f"Median: `{median_value:.2f}`, "
            f"Min: `{min_value:.2f}`, "
            f"Max: `{max_value:.2f}`"
        )


# ---------------------------------------------------------
# Categorical Insights
# ---------------------------------------------------------

if len(categorical_columns) > 0:

    st.subheader("🏷️ Categorical Insights")

    for column in categorical_columns:

        if df[column].notna().any():

            most_common = (
                df[column]
                .mode()
                .iloc[0]
            )

            count = (
                df[column]
                .value_counts()
                .iloc[0]
            )

            st.write(
                f"**{column}** → "
                f"Most common value: `{most_common}` "
                f"({count} occurrences)"
            )


# ---------------------------------------------------------
# Strongest Correlation
# ---------------------------------------------------------

if len(numeric_columns) >= 2:

    correlation_matrix = (
        df[numeric_columns]
        .corr()
        .abs()
    )

    # Remove diagonal values
    np.fill_diagonal(
        correlation_matrix.values,
        0
    )

    strongest_pair = (
        correlation_matrix
        .stack()
        .idxmax()
    )

    strongest_value = (
        correlation_matrix
        .loc[strongest_pair]
    )

    st.subheader("🔗 Strongest Numerical Relationship")

    st.write(
        f"`{strongest_pair[0]}` ↔ "
        f"`{strongest_pair[1]}`"
    )

    st.write(
        f"Correlation strength: "
        f"**{strongest_value:.2f}**"
    )
# =========================================================
# 19. DATE COLUMN DETECTION
# =========================================================

st.header("19️⃣ Date Column Detection")


date_columns = []


for column in df.columns:

    # Already datetime
    if pd.api.types.is_datetime64_any_dtype(
        df[column]
    ):

        date_columns.append(column)

    # Try converting object columns
    elif df[column].dtype == "object":

        converted = pd.to_datetime(
            df[column],
            errors="coerce"
        )

        valid_ratio = (
            converted.notna().mean()
        )

        if valid_ratio >= 0.8:

            date_columns.append(column)


if len(date_columns) > 0:

    st.success(
        f"Date columns detected: {date_columns}"
    )

else:

    st.info(
        "No date columns detected."
    )


# =========================================================
# DATE ANALYSIS
# =========================================================

if len(date_columns) > 0:

    st.subheader("📅 Date Analysis")

    selected_date_column = st.selectbox(
        "Select a date column",
        date_columns,
        key="date_column"
    )

    date_data = pd.to_datetime(
        df[selected_date_column],
        errors="coerce"
    )

    st.write(
        f"Earliest date: "
        f"**{date_data.min()}**"
    )

    st.write(
        f"Latest date: "
        f"**{date_data.max()}**"
    )

    # Extract date components

    date_info = pd.DataFrame({

        "Year":
        date_data.dt.year,

        "Month":
        date_data.dt.month,

        "Day":
        date_data.dt.day,

        "Day of Week":
        date_data.dt.day_name()

    })

    st.dataframe(
        date_info.head(10),
        use_container_width=True
    )

# =========================================================
# 21. GLOBAL SEARCH
# =========================================================

st.header("2️⃣0️⃣ Global Search")

search_text = st.text_input(
    "Search the entire dataset"
)


if search_text:

    search_mask = df.astype(str).apply(
        lambda column:
        column.str.contains(
            search_text,
            case=False,
            na=False
        )
    ).any(axis=1)


    search_results = df[
        search_mask
    ]


    st.write(
        f"Found **{len(search_results)} rows**."
    )


    st.dataframe(
        search_results,
        use_container_width=True
    )

else:

    st.info(
        "Enter text above to search the dataset."
    )

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "CSV Analyzer • Built with Python, Pandas, NumPy, "
    "Matplotlib and Streamlit"
)

          