import pandas as pd


def get_numeric_columns(df):

    return df.select_dtypes(
        include="number"
    ).columns.tolist()


def get_categorical_columns(df):

    return df.select_dtypes(
        include="object"
    ).columns.tolist()


def get_missing_values(df):

    return df.isnull().sum()


def get_duplicate_count(df):

    return df.duplicated().sum()


def get_column_information(df):

    return pd.DataFrame({

        "Column": df.columns,

        "Data Type":
        df.dtypes.astype(str).values,

        "Missing Values":
        df.isnull().sum().values,

        "Unique Values":
        df.nunique().values

    })


def get_correlation(df):

    numeric_columns = get_numeric_columns(df)

    if len(numeric_columns) < 2:

        return None

    return df[numeric_columns].corr()