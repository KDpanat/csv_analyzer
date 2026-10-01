def remove_duplicates(df):

    return df.drop_duplicates()


def remove_missing_rows(df):

    return df.dropna()


def fill_missing_mean(df, numeric_columns):

    new_df = df.copy()

    for column in numeric_columns:

        new_df[column] = (
            new_df[column]
            .fillna(
                new_df[column].mean()
            )
        )

    return new_df


def fill_missing_median(df, numeric_columns):

    new_df = df.copy()

    for column in numeric_columns:

        new_df[column] = (
            new_df[column]
            .fillna(
                new_df[column].median()
            )
        )

    return new_df


def find_outliers(df, column):

    Q1 = df[column].quantile(0.25)

    Q3 = df[column].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR

    upper = Q3 + 1.5 * IQR

    outliers = df[
        (df[column] < lower)
        |
        (df[column] > upper)
    ]

    return outliers, lower, upper


def remove_outliers(df, column):

    Q1 = df[column].quantile(0.25)

    Q3 = df[column].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR

    upper = Q3 + 1.5 * IQR

    return df[
        (df[column] >= lower)
        &
        (df[column] <= upper)
    ]