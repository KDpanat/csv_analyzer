def numerical_insights(
    df,
    numeric_columns
):

    results = []

    for column in numeric_columns:

        results.append({

            "Column": column,

            "Mean":
            df[column].mean(),

            "Median":
            df[column].median(),

            "Minimum":
            df[column].min(),

            "Maximum":
            df[column].max()

        })

    return results


def categorical_insights(
    df,
    categorical_columns
):

    results = []

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

            results.append({

                "Column": column,

                "Most Common":
                most_common,

                "Count": count

            })

    return results