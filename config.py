import os
import sys

# ----------------------------
# Base directory (works for .py + EXE)
# ----------------------------
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ----------------------------
# Shared file paths
# ----------------------------
EXL_FILE = os.path.join(BASE_DIR, "inventory.xlsx")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")
