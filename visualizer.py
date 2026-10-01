import matplotlib.pyplot as plt


def create_histogram(df, column):

    fig, ax = plt.subplots()

    ax.hist(
        df[column].dropna(),
        bins=20
    )

    ax.set_xlabel(column)

    ax.set_ylabel("Frequency")

    ax.set_title(
        f"Distribution of {column}"
    )

    return fig


def create_boxplot(df, column):

    fig, ax = plt.subplots()

    ax.boxplot(
        df[column].dropna()
    )

    ax.set_ylabel(column)

    ax.set_title(
        f"Box Plot of {column}"
    )

    return fig


def create_scatterplot(
    df,
    x_column,
    y_column
):

    fig, ax = plt.subplots()

    ax.scatter(
        df[x_column],
        df[y_column]
    )

    ax.set_xlabel(x_column)

    ax.set_ylabel(y_column)

    ax.set_title(
        f"{x_column} vs {y_column}"
    )

    return fig


def create_bar_chart(
    df,
    column
):

    value_counts = (
        df[column]
        .value_counts()
    )

    fig, ax = plt.subplots()

    ax.bar(
        value_counts.index.astype(str),
        value_counts.values
    )

    ax.set_xlabel(column)

    ax.set_ylabel("Count")

    ax.set_title(
        f"{column} Distribution"
    )

    plt.xticks(
        rotation=45
    )

    return fig