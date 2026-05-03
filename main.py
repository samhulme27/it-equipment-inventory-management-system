import pandas as pd 


EXL_FILE = "inventory.xlsx"

COL_DEVICE_NAME = "Device Name"
COL_DEVICE_TYPE = "Device Type"
COL_USER = "User"
COL_LOCATION = "location"
COL_DATE = "Date"
COL_NOTES = "Notes"
COL_STATUS = "Status"

# Mapping for the excel file and excel table colums, will need to change later when I've made the proper excel document 


def load_data():
    return pd.read_excel(EXL_FILE)


# Function to get the excel file, which loads into a table in python, now mapped to EXL_FILE


def save_data(df):
    df.to_excel(EXL_FILE, index=False)

# Function save data, takes updated python table data and writes it back into excel
