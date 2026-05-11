import subprocess
import pandas as pd
import re


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


def run_ps(command):
    result = subprocess.run(
        ["powershell", "-Command", command],
        capture_output=True,
        text=True
    )
    # keep only non-empty lines
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return lines[-1] if lines else ""


def get_serial_number():
    return run_ps("(Get-WmiObject Win32_BIOS).SerialNumber")


def get_mac_address():
    return run_ps("(Get-WmiObject Win32_NetworkAdapterConfiguration | Where-Object {$_.IPEnabled -eq $true}).MACAddress")


def get_device_name():
    return run_ps("(Get-WmiObject Win32_ComputerSystem).Name")


def get_device_type():
    return run_ps("(Get-WmiObject Win32_ComputerSystem).SystemType")


def get_model_number():
    return run_ps("(Get-WmiObject Win32_ComputerSystem).Model")


def get_user():
    return run_ps("(Get-WmiObject Win32_ComputerSystem).UserName")


def get_date():
    return run_ps("Get-Date -Format MM-dd-yyyy")


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
    df.columns = df.columns.str.strip()

    if COL_ASSET_TAG not in df.columns:
        return generate_asset_tag("ASSET", 1)

    tags = df[COL_ASSET_TAG].dropna().astype(str)

    numbers = []

    for tag in tags:
        tag = tag.strip()

        if "-" not in tag:
            continue

        parts = tag.split("-")

        if len(parts) != 2:
            continue

        if not parts[1].isdigit():
            continue

        numbers.append(int(parts[1]))

    next_number = max(numbers, default=0) + 1

    return generate_asset_tag("ASSET", next_number)
