import numpy as np
import pandas as pd


def summarize_dataframe(df):
    summary_data = []

    for col in df.columns:
        data_type = df[col].dtype
        # Simplify data type display
        if data_type == "int64":
            display_data_type = "int"
        elif data_type == "float64":
            display_data_type = "float"
        elif data_type == "object":
            display_data_type = "string"
        else:
            display_data_type = str(data_type)

        non_null_count = df[col].notnull().sum()
        null_count = df[col].isnull().sum()
        most_repeated_value = (
            df[col].value_counts().idxmax() if not df[col].isnull().all() else None
        )

        # Initialize lowest and highest values as "-"
        lowest_value = "-"
        highest_value = "-"

        # Check if the column data type is numeric to calculate min and max
        if pd.api.types.is_numeric_dtype(data_type):
            lowest_value = df[col].min()
            highest_value = df[col].max()
            # Adjust for non-numeric highest and lowest values
            lowest_value = lowest_value if pd.notnull(lowest_value) else "-"
            highest_value = highest_value if pd.notnull(highest_value) else "-"

        summary_data.append(
            {
                "Columna": col,
                "Tipo de dato": display_data_type,
                "Valores válidos": non_null_count,
                "Valores nulos": null_count,
                "Moda": most_repeated_value if pd.notnull(most_repeated_value) else "-",
                "Valor mínimo": lowest_value,
                "Valor máximo": highest_value,
            }
        )

    summary_df = pd.DataFrame(summary_data)
    return summary_df


def format_numbers(x):
    if isinstance(x, (int, float)):
        if float(x).is_integer():
            return "{:,.0f}".format(x)
        else:
            return "{:,.2f}".format(x)
    return x


def extended_describe(df):
    desc = df.describe()
    desc = desc.rename(
        index={
            "count": "Total de valores",
            "mean": "Media",
            "std": "Desviación estándar",
            "min": "Mínimo",
            "25%": "Q1",
            "50%": "Q2",
            "75%": "Q3",
            "max": "Máximo",
        }
    )
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    desc.loc["RIC"] = desc.loc["Q3"] - desc.loc["Q1"]
    desc.loc["Asimetría"] = df[numeric_cols].skew()
    desc.loc["Curtosis"] = df[numeric_cols].kurtosis()

    # Apply the format_numbers function
    desc = desc.map(format_numbers)

    return desc
