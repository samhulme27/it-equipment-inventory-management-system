import pandas as pd 
import datetime

# excel file
EXL_FILE = "inventory.xlsx"

COL_DEVICE_NAME = "Device Name"
COL_DEVICE_TYPE = "Device Type"
COL_SERIAL_NUMBER = "Serial Number"
COL_MODEL_NUMBER = "Model Number"
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
    df = df.reindex(columns=[
        COL_DEVICE_NAME,
        COL_DEVICE_TYPE,
        COL_SERIAL_NUMBER,
        COL_MODEL_NUMBER,
        COL_USER,
        COL_LOCATION,
        COL_DATE,
        COL_NOTES,
        COL_STATUS
    ])
    df.to_excel(EXL_FILE, index=False)

# Function save data, takes updated python table data and writes it back into excel


def add_new_device(device_name, device_type, serial_number, model_number, user, location, date, notes, status):

    df = load_data()
    #Load the data
    date = datetime.datetime.now()
    # get the date and time now
    
    new_row = {
        COL_DEVICE_NAME: device_name,
        COL_DEVICE_TYPE: device_type,
        COL_SERIAL_NUMBER: serial_number,
        COL_MODEL_NUMBER: model_number,
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

def retire_device(device_name):
    df = load_data()

    df[df[COL_DEVICE_NAME] != device_name]

    save_data(df)


def edit_device(device_name, column, new_value):
    
    df = load_data()
    #load the df

    filter = df[COL_DEVICE_NAME] == device_name

    #find the correct device name and row(create the filter)

    df.loc[filter, column] = new_value

    #loc - select specific rows and columns, change the value 
    
    save_data() 


#search function, takes the device name and searches through the excel file for it, then prints the row with the device name, if not found prints no devices found

def search_device_name(device_name):
    df = load_data()

    result = df[df[COL_DEVICE_NAME].astype(str).str.contains(device_name, case=False, na=False)]
    if result.empty:
        print("No devices found with that name.")
    else:
        print(result)
        return result

#serch function, takes the device type and searches through the excel file for it, then prints the row with the device type, if not found prints no devices found

def search_device_type(device_type):
    df = load_data()
    result = df[df[COL_DEVICE_TYPE].astype(str).str.contains(device_type, case=False, na=False)]
    if result.empty:
        print("No devices found with that type.")
    else:
        print("The following devices were found with that type:")
        print(result)
        return result

#search function, takes the user and searches through the excel file for it, then prints the row with the user, if not found prints no devices found

def search_user(user):
    df = load_data()
    result = df[df[COL_USER].astype(str).str.contains(user, case=False, na=False)]
    if result.empty:
        print("No devices found for that user.")
    else:
        print("The following devices were found for that user:")
        print(result)
        return result

#search function, takes the location and searches through the excel file for it, then prints the row with the location, if not found prints no devices found
def search_location(location):
    df = load_data()
    result = df[df[COL_LOCATION].astype(str).str.contains(location, case=False, na=False)]
    if result.empty:
        print("No devices found for that location.")
    else:
        print("The following devices were found for that location:")
        print(result)
        return result

search_device_type("desktop")