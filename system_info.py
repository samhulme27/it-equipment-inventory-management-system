import subprocess
import pandas as pd


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


def get_serial_number():
    command = "Get-WmiObject win32_bios | select SerialNumber"
    results = subprocess.run(["powershell", "-command", command], capture_output=True, text=True)
    print(results.stdout)
    return results.stdout.strip()


def get_mac_address():
    command = "Get-WmiObject win32_networkadapterconfiguration | where {$_.IPEnabled -eq $true} | select MACAddress"
    results = subprocess.run(["powershell", "-command", command], capture_output=True, text=True)
    print(results.stdout)
    return results.stdout.strip()


def get_device_name():
    command = "Get-WmiObject win32_computersystem | select Name"
    results = subprocess.run(["powershell", "-command", command], capture_output=True, text=True)
    print(results.stdout)
    return results.stdout.strip()


def get_device_type():
    command = "Get-WmiObject win32_computersystem | select SystemType"
    results = subprocess.run(["powershell", "-command", command], capture_output=True, text=True)
    print(results.stdout)
    return results.stdout.strip()


def get_model_number():
    command = "Get-WmiObject win32_computersystem | select Model"
    results = subprocess.run(["powershell", "-command", command], capture_output=True, text=True)
    print(results.stdout)
    return results.stdout.strip()


def get_user():
    command = "Get-WmiObject win32_computersystem | select UserName"
    results = subprocess.run(["powershell", "-command", command], capture_output=True, text=True)
    print(results.stdout)
    return results.stdout.strip()


def get_date():
    command = "Get-Date -Format MM-dd-yyyy"
    results = subprocess.run(["powershell", "-command", command], capture_output=True, text=True)
    print(results.stdout)
    return results.stdout.strip()


def generate_device_info(asset_tag, device_name, device_type, serial_number, model_number, mac_address, user, location, date, notes, status):
    return {
        COL_ASSET_TAG: asset_tag,
        COL_DEVICE_NAME: device_name,
        COL_DEVICE_TYPE: device_type,
        COL_SERIAL_NUMBER: serial_number,
        COL_MODEL_NUMBER: model_number,
        COL_MAC_ADDRESS: mac_address,
        COL_USER: user,
        COL_LOCATION: location,
        COL_DATE: date,
        COL_NOTES: notes,
        COL_STATUS: status
    }


def generate_asset_tag(prefix,number):
    return f"{prefix}-{number:04d}"


def generate_next_asset_tag(file_path):

    df = pd.read_excel(file_path)

    tags = df[COL_ASSET_TAG].dropna().astype(str)

    if tags.empty:
        next_number = 1
    else:
        last_asset_tag = tags.iloc[-1]

        try:
            last_number = int(last_asset_tag.split("-")[1])
        except (IndexError, ValueError):
            last_number = 0

        next_number = last_number + 1

    return generate_asset_tag("ASSET", next_number)
