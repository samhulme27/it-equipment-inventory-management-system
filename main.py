import pandas as pd 
import shutil, os
from datetime import datetime
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



def validate_data(device):

    asset_tag = str(device.get(COL_ASSET_TAG, "")).strip()
    serial = str(device.get(COL_SERIAL_NUMBER, "")).strip()

    if not asset_tag:
        return False, "Empty asset tag"

    if not serial:
        return False, "Empty serial number"

    return True, "Valid"



def device_exists(serial_number):
    df = load_data()
    serials = df[COL_SERIAL_NUMBER].astype(str)
    return serial_number in serials.values


def load_data():
    return pd.read_excel(EXL_FILE)


# Function to get the excel file, which loads into a table in python, now mapped to EXL_FILE


def save_data(df):

    if os.path.exists(EXL_FILE):
        data_backup(EXL_FILE) # backup data before saving, creates a backup folder and saves the old file with a timestamp, prevents data loss from accidental overwrites, last state before action is saved 

    # enforce correct column order only
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

    # FORCE asset tag FIRST (guaranteed not empty)
    if not device_dict.get(COL_ASSET_TAG):
        device_dict[COL_ASSET_TAG] = generate_next_asset_tag(EXL_FILE)

    valid, message = validate_data(device_dict)

    if not valid:
        print(f"Validation failed: {message}")
        return

    df = load_data()

    new_df = pd.DataFrame([device_dict])

    df = pd.concat([df, new_df], ignore_index=True)

    save_data(df)


def manually_add_device():

    device_dict = {
        COL_ASSET_TAG: generate_next_asset_tag(EXL_FILE),
        COL_DEVICE_NAME: input("Enter device name: "),
        COL_DEVICE_TYPE: input("Enter device type: "),
        COL_SERIAL_NUMBER: input("Enter serial number: "),
        COL_MODEL_NUMBER: input("Enter model number: "),
        COL_MAC_ADDRESS: input("Enter MAC address: "),
        COL_USER: input("Enter user: "),
        COL_LOCATION: input("Enter location: "),
        COL_DATE: datetime.now(),
        COL_NOTES: input("Enter any notes: "),
        COL_STATUS: input("Enter status (In Use, Available, Retired, Repair): ")
    }

    add_new_device(device_dict)


def retire_device(device_name):
    df = load_data()

    df[df[COL_DEVICE_NAME] != device_name]

    save_data(df)


def edit_device(serial_number, column, new_value):
    
    df = load_data()
    #load the df

    filter = df[COL_SERIAL_NUMBER].astype(str) == str(serial_number)

    #find the correct device serial and row(create the filter)

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
    

def data_backup(file_path):

    if not os.path.exists(file_path):
        return
    
    back_up_folder = "backups"
    os.makedirs(back_up_folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    back_up_file = os.path.join(back_up_folder, f"inventory_backup_{timestamp}.xlsx")

    shutil.copy(file_path, back_up_file)

    #keep 10 most recent backups, delete older ones
    backups = sorted([
        os.path.join(back_up_folder, f)
        for f in os.listdir(back_up_folder)
        if f.endswith(".xlsx")
    ], key=os.path.getmtime
    )

    while len(backups) > 10:
        os.remove(backups[0])
        backups.pop(0)


def update_existing_device(device_dict):
    df = load_data()

    serial = str(device_dict[COL_SERIAL_NUMBER])

    mask = df[COL_SERIAL_NUMBER].astype(str) == serial

    auto_updated_fields = [
        COL_DEVICE_NAME, 
        COL_DEVICE_TYPE, 
        COL_MODEL_NUMBER, 
        COL_MAC_ADDRESS,
        COL_USER, 
        COL_DATE]
    
    for field in auto_updated_fields:
        df.loc[mask, field] = device_dict[field]
    save_data(df)

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

    valid, message = validate_data(device)

    if not valid:
        print(f"Device data validation failed: {message}")
        return

    if device_exists(device[COL_SERIAL_NUMBER]):
        update_existing_device(device)
        print("Device with this serial number already exists. Cannot add duplicate.")
    else:
        add_new_device(device)
        print("Device added successfully.")
