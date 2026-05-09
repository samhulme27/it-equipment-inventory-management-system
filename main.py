import pandas as pd 
import datetime
from system_info import get_serial_number, get_mac_address, get_device_name, get_device_type, get_model_number, get_user, generate_device_info, get_date, generate_next_asset_tag, generate_asset_tag

# excel fileS
EXL_FILE = "inventory.xlsx"

COL_ASSET_TAG = "Asset Tag"
COL_DEVICE_NAME = "Device Name"
COL_DEVICE_TYPE = "Device Type"
COL_SERIAL_NUMBER = "Serial Number"
COL_MODEL_NUMBER = "Model Number"
COL_MAC_ADDRESS = "MAC Address"
COL_USER = "User"
COL_LOCATION = "location"
COL_DATE = "Date"
COL_NOTES = "Notes"
COL_STATUS = "Status"

# Mapping for the excel file and excel table colums, will need to change later when I've made the proper excel document 

VALID_STATUS = ["In Use", "Available", "Retired", "repair"]



def validate_data(df):
    if df[COL_ASSET_TAG].duplicated().any():
        # check for duplicate asset tags, if any are found return false and error message
        return False, "Duplicate asset tags found"
    if df[COL_ASSET_TAG].astype(str).str.strip().eq("").any():
        # check for empty asset tags, if any are found return false and error message
        return False, "Empty asset tags found"
    
    if df[COL_DEVICE_NAME].duplicated().any():
        # check for duplicate device names, if any are found return false and error message
        return False, "Duplicate device names found"
    return True, "Data is valid"


def load_data():
    return pd.read_excel(EXL_FILE)


# Function to get the excel file, which loads into a table in python, now mapped to EXL_FILE


def save_data(df):
    valid, message = validate_data(df)

    if not valid:
        print(f"Data validation failed: {message}")
        return

    df = df.reindex(columns=[
        COL_ASSET_TAG,
        COL_DEVICE_NAME,
        COL_DEVICE_TYPE,
        COL_SERIAL_NUMBER,
        COL_MODEL_NUMBER,
        COL_MAC_ADDRESS,
        COL_USER,
        COL_LOCATION,
        COL_DATE,
        COL_NOTES,
        COL_STATUS
    ])

    df.to_excel(EXL_FILE, index=False)
    print("Data saved successfully.")

# Function save data, validates data and takes updated python table data and writes it back into excel


def add_new_device(device_dict):

    df = load_data()

    # ensure date is set here OR earlier in pipeline
    if COL_DATE not in device_dict:
        device_dict[COL_DATE] = datetime.datetime.now()

    new_df = pd.DataFrame([device_dict])

    df = pd.concat([df, new_df], ignore_index=True)

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

#search function, takes the device type and searches through the excel file for it, then prints the row with the device type, if not found prints no devices found

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


def run():
    device = generate_device_info(
        asset_tag=generate_next_asset_tag(EXL_FILE),
        device_name=get_device_name(),
        device_type=get_device_type(),
        serial_number=get_serial_number(),
        model_number=get_model_number(),
        mac_address=get_mac_address(),
        user=get_user(),
        location="Unknown",
        date=get_date(),
        notes="No notes",
        status="Active"
    )
    add_new_device(device)

run()