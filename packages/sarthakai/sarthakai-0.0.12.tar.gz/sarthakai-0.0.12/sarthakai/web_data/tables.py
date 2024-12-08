import os
from pyairtable import Api

# Data management
import pandas as pd
from pandas import DataFrame


def get_airtable_data(base_id: str, table_id: str):
    airtable_api = Api(os.environ["AIRTABLE_API_KEY"])
    table = airtable_api.table(base_id, table_id)
    table = table.all()
    return table


def get_data_from_gsheet(sheet_id: str, gid: str) -> DataFrame:
    df = pd.read_csv(
        f"https://docs.google.com/spreadsheets/export?id={sheet_id}&gid={gid}&exportFormat=csv"
    )
    return df
