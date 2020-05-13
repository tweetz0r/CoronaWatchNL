from pathlib import Path
import itertools

import pandas as pd
import numpy as np

from utils import convert_to_int

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

DATA_FOLDER = Path("data-desc")

VARIABLES = [
    "Totaal",
    "Ziekenhuisopname",
    "Overleden"
]


def get_timeline():

    df = pd.read_csv(Path("data", "rivm_NL_covid19_sex.csv"))
    dates = sorted(df["Datum"].unique())

    return dates


def export_date(df, data_folder, prefix, data_date=None, label=None):

    if data_date:
        df_date = df.loc[df["Datum"] == data_date, :]
    else:
        df_date = df

    # export with data date
    if label is not None:
        export_path = Path(DATA_FOLDER, data_folder, f"{prefix}_{label}.csv")
    else:
        export_path = Path(DATA_FOLDER, data_folder, f"{prefix}.csv")

    print(f"Export {export_path}")
    df_date.to_csv(export_path, index=False)


def main_sex():

    df_reported = pd.read_csv(Path("data", "rivm_NL_covid19_sex.csv"))
    df_reported = df_reported.rename(columns={"Aantal": "AantalCumulatief"})
    
    df_reported["Aantal"] = df_reported \
    .groupby(['Type', 'Geslacht'], sort=True)['AantalCumulatief'] \
    .transform(pd.Series.diff)
    
    df_reported.loc[df_reported["Datum"] == sorted(df_reported["Datum"].unique())[0], "Aantal"] = \
    df_reported.loc[df_reported["Datum"] == sorted(df_reported["Datum"].unique())[0], "AantalCumulatief"]

    df_reported['Aantal'] = df_reported["Aantal"].astype(pd.Int64Dtype())
    df_reported['AantalCumulatief'] = df_reported["AantalCumulatief"].astype(pd.Int64Dtype())

    # format the columns
    df_reported = df_reported[[
        "Datum",
        "Geslacht",
        "Type",
        "Aantal",
        "AantalCumulatief"
    ]]

    Path(DATA_FOLDER, "data-sex").mkdir(exist_ok=True)

    dates = sorted(df_reported["Datum"].unique())

    # export by date
    for data_date in dates:

        export_date(df_reported, "data-sex", "RIVM_NL_sex", data_date, str(data_date).replace("-", ""))

    # export latest
    export_date(df_reported, "data-sex", "RIVM_NL_sex", data_date=dates[-1], label="latest")

    # export all
    export_date(df_reported, "data-sex", "RIVM_NL_sex", data_date=None, label=None)


def main_age():

    df_reported = pd.read_csv(Path("data", "rivm_NL_covid19_age.csv"))
    df_reported = df_reported.rename(columns={"Aantal": "AantalCumulatief"})

    df_reported["Aantal"] = df_reported \
    .groupby(['Type', 'LeeftijdGroep'], sort=True)['AantalCumulatief'] \
    .transform(pd.Series.diff)
    
    df_reported.loc[df_reported["Datum"] == sorted(df_reported["Datum"].unique())[0], "Aantal"] = \
    df_reported.loc[df_reported["Datum"] == sorted(df_reported["Datum"].unique())[0], "AantalCumulatief"]

    df_reported['Aantal'] = df_reported["Aantal"].astype(pd.Int64Dtype())
    df_reported['AantalCumulatief'] = df_reported["AantalCumulatief"].astype(pd.Int64Dtype())

    # format the columns
    df_reported = df_reported[[
        "Datum",
        "LeeftijdGroep",
        "Type",
        "Aantal",
        "AantalCumulatief"
    ]]

    Path(DATA_FOLDER, "data-age").mkdir(exist_ok=True)

    dates = sorted(df_reported["Datum"].unique())

    # export by date
    for data_date in dates:

        export_date(df_reported, "data-age", "RIVM_NL_age", data_date, str(data_date).replace("-", ""))

    # export latest
    export_date(df_reported, "data-age", "RIVM_NL_age", data_date=dates[-1], label="latest")

    # export all
    export_date(df_reported, "data-age", "RIVM_NL_age", data_date=None, label=None)
    
    
if __name__ == '__main__':

    DATA_FOLDER.mkdir(exist_ok=True)

    main_sex()
     
    main_age()

