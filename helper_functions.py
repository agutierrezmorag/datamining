import numpy as np


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
    return desc
