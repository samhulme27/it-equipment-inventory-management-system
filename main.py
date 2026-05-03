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


df = pd.read_excel("inventory.xlsx") 
# load excel file into a table in python and call it df
print(df)