import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from datetime import datetime

from main import add_new_device, run, load_data, device_exists, save_data
from system_info import get_serial_number


COL_ASSET_TAG = "Asset Tag"
COL_ASSET_NAME = "Asset Name"
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
root.geometry("1200x800")

print("UI module loaded")

# ----------------------------
# Actions
# ----------------------------

def scan_device():
    serial_number = get_serial_number()
    messagebox.showinfo("scanning", "Scanning device...")
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
    inventory_window.geometry("1200x800")
    inventory_window.configure(bg="#f5f5f5")

    frame = tk.Frame(inventory_window, bg="#f5f5f5")
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


    def load_table(dataframe):

        tree.delete(*tree.get_children())

        if dataframe.empty:
            return

        dataframe.columns = dataframe.columns.str.strip()

        dataframe[COL_DATE] = pd.to_datetime(
            dataframe[COL_DATE],
            errors="coerce"
        )

        dataframe = dataframe.sort_values(
            by=COL_DATE,
            ascending=False
        ).reset_index(drop=True)

        for _, row in dataframe.iterrows():

            display_values = []

            for value in row:

                if pd.isna(value):
                    value = ""

                elif isinstance(value, pd.Timestamp):
                    value = value.strftime("%m-%d-%Y")

                display_values.append(str(value))

            tree.insert(
                "",
                "end",
                values=display_values
            )


    # ----------------------------
    # SEARCH BAR
    # ----------------------------
    search_var = tk.StringVar()

    search_entry = tk.Entry(frame, textvariable=search_var)
    search_entry.pack(fill="x", pady=5)
    search_entry.insert(0, "Search devices...")

    # ----------------------------
    # TREE + SCROLLBAR
    # ----------------------------
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    tree = ttk.Treeview(
        frame,
        yscrollcommand=scrollbar.set,
        selectmode="browse"
    )

    scrollbar.config(command=tree.yview)

    # ----------------------------
    # LOAD DATA
    # ----------------------------
    df = load_data()

    if df.empty:
        messagebox.showinfo(
            "Inventory",
            "No devices found"
        )
        inventory_window.destroy()
        return

    df.columns = df.columns.str.strip()

    # ----------------------------
    # SORT BY MOST RECENT
    # ----------------------------
    df[COL_DATE] = pd.to_datetime(
        df[COL_DATE],
        errors="coerce"
    )

    df = df.sort_values(
        by=COL_DATE,
        ascending=False
    ).reset_index(drop=True)

    tree["columns"] = list(df.columns)

    tree.column("#0", width=0, stretch=False)

    for col in df.columns:
        tree.column(
            col,
            anchor="w",
            width=170,
            stretch=True
        )

        tree.heading(
            col,
            text=col,
            anchor="w"
        )

    # ----------------------------
    # LOAD TABLE
    # ----------------------------
    def load_table(dataframe):

        tree.delete(*tree.get_children())

        for _, row in dataframe.iterrows():
            tree.insert(
                "",
                "end",
                values=list(row)
            )

    load_table(df)

    # ----------------------------
    # SEARCH
    # ----------------------------
    def update_search(*args):

        query = search_var.get().lower().strip()

        if not query or query == "search devices...":
            load_table(df)
            return

        filtered = df[df.apply(
            lambda row:
            row.astype(str)
            .str.lower()
            .str.contains(query)
            .any(),
            axis=1
        )]

        load_table(filtered)

    search_var.trace_add("write", update_search)

    # ----------------------------
    # VIEW DEVICE
    # ----------------------------
    def view_selected():

        selected = tree.selection()

        if not selected:
            return

        item = tree.item(selected[0])
        values = item["values"]

        view_window = tk.Toplevel(inventory_window)
        view_window.title("Device Details")
        view_window.geometry("600x400")

        for i, col in enumerate(df.columns):

            tk.Label(
                view_window,
                text=f"{col}: {values[i]}",
                anchor="w",
                justify="left"
            ).pack(
                fill="x",
                padx=10,
                pady=3
            )

    # ----------------------------
    # EDIT DEVICE
    # ----------------------------
    def edit_selected():

        selected = tree.selection()

        if not selected:
            return

        item = tree.item(selected[0])
        values = item["values"]

        edit_window = tk.Toplevel(inventory_window)
        edit_window.title("Edit Device")
        edit_window.geometry("600x400")

        entries = {}

        for i, col in enumerate(df.columns):

            tk.Label(
                edit_window,
                text=col
            ).pack()

            entry = tk.Entry(edit_window)

            entry.insert(0, values[i])

            entry.pack(
                fill="x",
                padx=10,
                pady=3
            )

            entries[col] = entry

        def save_changes():

            key_col = df.columns[0]
            key_value = values[0]

            idx = df.index[
                df[key_col] == key_value
            ]

            if len(idx) > 0:

                for col in df.columns:

                    df.at[
                        idx[0],
                        col
                    ] = entries[col].get()

                save_data(df)

                messagebox.showinfo(
                    "Saved",
                    "Device updated successfully.", parent=inventory_window
                )

            edit_window.destroy()

            load_table(df)

        tk.Button(
            edit_window,
            text="Save",
            command=save_changes
        ).pack(pady=10)

    # ----------------------------
    # DELETE DEVICE
    # ----------------------------
    def delete_selected():

        selected = tree.selection()

        if not selected:
            messagebox.showwarning(
                "Delete",
                "Please select a device first.",
                parent=inventory_window
            )
            return

        item = tree.item(selected[0])
        values = item["values"]

        # use Asset Tag as safe key
        asset_index = list(df.columns).index(COL_ASSET_TAG)
        asset_value = values[asset_index]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this device?",
            parent=inventory_window
        )

        if not confirm:
            return

       # reload latest data directly from excel
        updated_df = load_data()

        # clean columns
        updated_df.columns = updated_df.columns.str.strip()

        # remove selected device using Asset Tag
        updated_df = updated_df[
            updated_df[COL_ASSET_TAG]
            .astype(str)
            .str.strip()
            !=
            str(asset_value).strip()
        ]

        # IMPORTANT
        # reset indexes after delete
        updated_df = updated_df.reset_index(drop=True)

        # save updated dataframe
        save_data(updated_df)

        # refresh table
        load_table(updated_df)

    # ----------------------------
    # RIGHT CLICK MENU
    # ----------------------------
    menu = tk.Menu(
        inventory_window,
        tearoff=0
    )

    menu.add_command(
        label="View",
        command=view_selected
    )

    menu.add_command(
        label="Edit",
        command=edit_selected
    )


    menu.add_command(
        label="Delete",
        command=delete_selected
    )

    def show_menu(event):

        try:

            tree.selection_set(
                tree.identify_row(event.y)
            )

            menu.post(
                event.x_root,
                event.y_root
            )

        finally:
            menu.grab_release()

    tree.bind("<Button-3>", show_menu)

    # ----------------------------
    # PACK TREE
    # ----------------------------
    tree.pack(
        fill="both",
        expand=True
    )


def open_manually_add_device_window():
    add_window = tk.Toplevel(root)
    add_window.title("Manually Add Device")
    add_window.geometry("1200x800")

    # Asset Name
    label_asset_name = tk.Label(add_window, text="Asset Name:")
    label_asset_name.pack()
    entry_asset_name = tk.Entry(add_window)
    entry_asset_name.pack()

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
            COL_ASSET_NAME: entry_asset_name.get(),
            COL_SERIAL_NUMBER: entry_serial_number.get(),
            COL_DEVICE_TYPE: entry_device_type.get(),
            COL_MODEL_NUMBER: entry_model_number.get(),
            COL_MAC_ADDRESS: entry_mac_address.get(),
            COL_USER: entry_user.get(),
            COL_LOCATION: entry_location.get(),
            COL_DATE: datetime.now(),
            COL_NOTES: entry_notes.get(),
            COL_STATUS: entry_status.get()
        }

        add_new_device(device_dict)
        messagebox.showinfo("Success", "Device added successfully.", parent=add_window)
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
