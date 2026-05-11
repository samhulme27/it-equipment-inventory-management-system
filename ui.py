import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from datetime import datetime

from main import add_new_device, run, load_data, device_exists, manually_add_device, save_data
from system_info import get_serial_number


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


# ----------------------------
# UI setup
# ----------------------------

root = tk.Tk()
root.title("IT Asset Manager")
root.geometry("1600x1200")

print("UI module loaded")

# ----------------------------
# Actions
# ----------------------------

def scan_device():
    serial_number = get_serial_number()
    try:
        if device_exists(serial_number):  # Example serial number check
            messagebox.showinfo("Device Check", "Device already exists in inventory, data has been updated.")
        else:
            run()
            messagebox.showinfo("Device Check", "Device scanned and added to inventory.")
    except Exception as e:
        messagebox.showerror("Error", str(e))




def view_inventory():

    inventory_window = tk.Toplevel(root)
    inventory_window.title("Inventory")
    inventory_window.geometry("1600x800")

    frame = tk.Frame(inventory_window)
    frame.pack(fill=tk.BOTH, expand=True)

    # ----------------------------
    # SEARCH BAR
    # ----------------------------
    search_var = tk.StringVar()

    search_entry = tk.Entry(frame, textvariable=search_var)
    search_entry.pack(fill="x", padx=5, pady=5)
    search_entry.insert(0, "Search...")

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    tree = ttk.Treeview(frame, yscrollcommand=scrollbar.set, selectmode="browse")
    scrollbar.config(command=tree.yview)

    try:
        df = load_data()

        if df.empty:
            messagebox.showinfo("Inventory", "No devices found")
            return

        df.columns = df.columns.str.strip()

        tree["columns"] = list(df.columns)
        tree.column("#0", width=0, stretch=False)

        for col in df.columns:
            tree.column(col, anchor="w", width=160)
            tree.heading(col, text=col)

        # ----------------------------
        # LOAD DATA FUNCTION
        # ----------------------------
        def load_table(dataframe):
            tree.delete(*tree.get_children())

            for _, row in dataframe.iterrows():
                tree.insert("", "end", values=[row[col] for col in dataframe.columns])

        load_table(df)

        # ----------------------------
        # SEARCH FUNCTION
        # ----------------------------
        def update_search(*args):
            query = search_var.get().lower().strip()

            if not query or query == "search...":
                load_table(df)
                return

            filtered = df[df.apply(
                lambda row: row.astype(str).str.lower().str.contains(query).any(),
                axis=1
            )]

            load_table(filtered)

        search_var.trace_add("write", update_search)

        # ----------------------------
        # EDIT FUNCTION
        # ----------------------------
        def on_row_double_click(event):
            selected = tree.selection()
            if not selected:
                return

            item = tree.item(selected[0])
            values = item["values"]

            edit_window = tk.Toplevel(inventory_window)
            edit_window.title("Edit Device")
            edit_window.geometry("400x500")

            entries = {}

            for i, col in enumerate(df.columns):
                tk.Label(edit_window, text=col).pack()

                entry = tk.Entry(edit_window)
                entry.insert(0, values[i])
                entry.pack()

                entries[col] = entry

            def save_changes():
                nonlocal df

                updated = {col: entries[col].get() for col in df.columns}

                # find row by first column (assumed unique like asset tag or serial)
                key_col = df.columns[0]
                key_value = values[0]

                idx = df.index[df[key_col] == key_value]

                if len(idx) > 0:
                    for col in df.columns:
                        df.at[idx[0], col] = updated[col]

                    save_data(df)

                edit_window.destroy()
                load_table(df)

            tk.Button(edit_window, text="Save", command=save_changes).pack(pady=10)

        tree.bind("<Double-1>", on_row_double_click)

        tree.pack(fill="both", expand=True)

    except Exception as e:
        messagebox.showerror("Error", str(e))



def open_manually_add_device_window():
    add_window = tk.Toplevel(root)
    add_window.title("Manually Add Device")
    add_window.geometry("1000x800")

    # Device Name
    label_device_name = tk.Label(add_window, text="Device Name:")
    label_device_name.pack()
    entry_device_name = tk.Entry(add_window)
    entry_device_name.pack()

    # Serial Number
    label_serial_number = tk.Label(add_window, text="Serial Number:")
    label_serial_number.pack()
    entry_serial_number = tk.Entry(add_window)
    entry_serial_number.pack()

    # Device Type
    label_device_type = tk.Label(add_window, text="Device Type:")
    label_device_type.pack()
    entry_device_type = tk.Entry(add_window)
    entry_device_type.pack()

    # Model Number
    label_model_number = tk.Label(add_window, text="Model Number:")
    label_model_number.pack()
    entry_model_number = tk.Entry(add_window)
    entry_model_number.pack()

    # MAC Address
    label_mac_address = tk.Label(add_window, text="MAC Address:")
    label_mac_address.pack()
    entry_mac_address = tk.Entry(add_window)
    entry_mac_address.pack()

    # User
    label_user = tk.Label(add_window, text="User:")
    label_user.pack()
    entry_user = tk.Entry(add_window)
    entry_user.pack()

    # Location
    label_location = tk.Label(add_window, text="Location:")
    label_location.pack()
    entry_location = tk.Entry(add_window)
    entry_location.pack()

    # Notes
    label_notes = tk.Label(add_window, text="Notes:")
    label_notes.pack()
    entry_notes = tk.Entry(add_window)
    entry_notes.pack()

    # Status
    label_status = tk.Label(add_window, text="Status:")
    label_status.pack()
    entry_status = tk.Entry(add_window)
    entry_status.pack()

    def submit_device():
        device_dict = {
            COL_DEVICE_NAME: entry_device_name.get(),
            COL_SERIAL_NUMBER: entry_serial_number.get(),
            COL_DEVICE_TYPE: entry_device_type.get(),
            COL_MODEL_NUMBER: entry_model_number.get(),
            COL_MAC_ADDRESS: entry_mac_address.get(),
            COL_USER: entry_user.get(),
            COL_LOCATION: entry_location.get(),
            COL_DATE: datetime.now().strftime("%m-%d-%Y"),
            COL_NOTES: entry_notes.get(),
            COL_STATUS: entry_status.get()
        }

        add_new_device(device_dict)
        add_window.destroy()

    tk.Button(add_window, text="Add Device", command=submit_device).pack(pady=10)


# ----------------------------
# Buttons
# ----------------------------

btn_scan = tk.Button(root, text="Scan Device", command=scan_device)
btn_scan.pack(pady=10)

btn_view = tk.Button(root, text="View Inventory", command=view_inventory)
btn_view.pack(pady=10)

add_new_device_button = tk.Button(root, text="Manually Add Device", command=open_manually_add_device_window)
add_new_device_button.pack(pady=10)


btn_exit = tk.Button(root, text="Exit", command=root.quit)
btn_exit.pack(pady=10)
# ----------------------------
# Run UI
# ----------------------------

root.mainloop()
