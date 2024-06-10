import numpy as np


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
