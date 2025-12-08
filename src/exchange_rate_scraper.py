import requests
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import os

root = tk.Tk()
root.withdraw()

# output_dir = "exports"
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
output_dir = os.path.join(parent_dir, "exports")
os.makedirs(output_dir, exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename_csv = os.path.join(output_dir, f"exchange_rates_{timestamp}.csv")
filename_xlsx = os.path.join(output_dir, f"exchange_rates_{timestamp}.xlsx")

api_key = "2b0cfe3554e260aac4c02f27"
url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"

resp = requests.get(url, timeout=10)
data = resp.json()
if data.get("result") != "success":
    messagebox.showerror("خطا", "API دیتا نداد.")
    exit()
base_currency = data["base_code"]
last_update = data["time_last_update_utc"]

print(f"base currency: {base_currency}")
print(f"last update: {last_update}")

rates_df = pd.DataFrame(data['conversion_rates'].items(), columns=['Currency','Rate'])
rates_df['Rate'] = rates_df['Rate'].round(4)
rates_df = rates_df.sort_values(by="Rate", ascending=False).reset_index(drop=True)

print(rates_df.head(20))

if os.path.exists(filename_csv):
    result = messagebox.askyesnocancel("فایل موجود است",
                                       f"{filename_csv} وجود دارد. \n آیا میخواهید جایگزین شود؟")
    if result is None:
        exit()
    elif result:
        pass
    else:
        filename_csv = os.path.join(output_dir, f"exchange_rates_{timestamp}_new.csv")
rates_df.to_csv(filename_csv, index=False, encoding="utf-8-sig")

if os.path.exists(filename_xlsx):
    result = messagebox.askyesnocancel("فایل موجود است",
                                       f"{filename_xlsx} وجود دارد. \n آیا میخواهید جایگزین شود؟")
    if result is None:
        exit()
    elif result:
        pass
    else:
        filename_xlsx = os.path.join(output_dir, f"exchange_rates_{timestamp}_new.xlsx")
rates_df.to_excel(filename_xlsx, index=False, engine="openpyxl")

messagebox.showinfo("موفقیت", "فایل‌ها ذخیره شدند.")

