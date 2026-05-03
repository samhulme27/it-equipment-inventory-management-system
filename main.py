import pandas as pd 
import datetime


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


def add_new_device(device_name, device_type, user, location, date, notes, status):

    df = load_data()
    #Load the data
    date = datetime.datetime.now()
    # get the date and time now
    
    new_row = {
        COL_DEVICE_NAME: device_name,
        COL_DEVICE_TYPE: device_type,
        COL_USER: user,
        COL_LOCATION: location,
        COL_DATE: date,
        COL_NOTES: notes,
        COL_STATUS: status

        }

    new_df = pd.DataFrame([new_row])
    df = pd.concat([df, new_df], ignore_index=True)

    #get the data from the new row, merge the new row with the df
    save_data(df)

