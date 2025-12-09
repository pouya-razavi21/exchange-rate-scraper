"""
exchange_rate_scraper.py

Fetches exchange rates from ExchangeRate-API and saves to CSV/XLSX.

- Input: API key via environment variable `API_KEY`
- API Docs: https://www.exchangerate-api.com/docs/overview
- Output: timestamped CSV and XLSX files in project_root/exports/
- Dependencies: requests, pandas, python-dotenv, openpyxl, tkinter
"""

import requests     # HTTP requests to ExchangeRate API
import pandas as pd     # DataFrame manipulation and file export
from datetime import datetime    # Timestamp for filenames
import tkinter as tk    # GUI dialogs (confirmations / alerts)
from tkinter import messagebox     # Message dialog boxes
import os   # File and directory operations
from dotenv import load_dotenv    # Read API key from .env
import logging     # Log script activity
import sys
from pathlib import Path

# Configure logging format and level
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("شروع اجرای اسکریپت")

# Create hidden Tkinter root window for dialogs
root = tk.Tk()
root.withdraw()

# Load API key from .env file
load_dotenv()
BASE_CURRENCY = "USD"
api_key = os.getenv('API_KEY')
BASE_URL = "https://v6.exchangerate-api.com/v6"
if not api_key:
    messagebox.showerror("Error", "در env. API_KEY تعریف نشده.")
    sys.exit(1)
url = (f"{BASE_URL}/{api_key}/latest/{BASE_CURRENCY}")

# Determine project root and export directory
# Create exports directory if not exists
current_dir = Path(__file__).resolve().parent
output_dir = current_dir.parent / "exports"
output_dir.mkdir(exist_ok=True)

# Create timestamped filenames
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename_csv = output_dir / f"exchange_rates_{timestamp}.csv"
filename_xlsx = output_dir / f"exchange_rates_{timestamp}.xlsx"

# Fetch exchange rates from API and parse JSON
try:
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()
except requests.exceptions.RequestException as e:
    messagebox.showerror("Network Error", f"خطا در اتصال به API: \n{e}")
    sys.exit()
except ValueError:
    messagebox.showerror("Parse Error", f"پاسخ API قابل تبدیل به JSON نبود.")
    sys.exit()

# Handle network errors and invalid JSON 
if data.get("result") != "success":
    logging.error(f"API Error: {data.get('error-type')}")
    messagebox.showerror("خطا", "API دیتا نداد.")
    sys.exit()
base_currency = data["base_code"]
last_update = data["time_last_update_utc"]

logging.info(f"Base Currency: {base_currency}")
logging.info(f"Last Update: {last_update}")

# Build DataFrame from conversion rates and sort descending
rates_df = pd.DataFrame(data['conversion_rates'].items(), columns=['Currency','Rate'])
rates_df['Rate'] = rates_df['Rate'].round(4)
rates_df = rates_df.sort_values(by="Rate", ascending=False).reset_index(drop=True)

# Print first 20 data at screen
logging.info(rates_df.head(20))
# print(rates_df.head(20))

def save_with_prompt(df, path, write_func):
    """Save DataFrame to a file path.
       If file exists, ask user before overwrite.
       Returns:
       bool: True on successful save, False if user canceled.
    """
    path = Path(path)
    if path.exists():
        res = messagebox.askyesnocancel("فایل موجود است", f"{path}\nآیا جایگزین شود؟")
        if res is None:
            return False
        elif not res:
            new_path = path.with_name(path.stem + "_new" + path.suffix)
            # base, ext = os.path.splitext(path)
            # path = f"{base}_new{ext}"
            return new_path
    write_func(path)
    return True

# Save CSV and Excel files using the helper function
save_with_prompt(rates_df, filename_csv, lambda p: rates_df.to_csv(p, index=False, encoding="utf-8-sig"))
save_with_prompt(rates_df, filename_xlsx, lambda p: rates_df.to_excel(p, index=False, engine="openpyxl"))

logging.info(f"Saved CSV: {filename_csv}")
logging.info(f"Saved Excel: {filename_xlsx}")

# Show completion dialog
messagebox.showinfo("موفقیت", "فایل‌ها ذخیره شدند.")

