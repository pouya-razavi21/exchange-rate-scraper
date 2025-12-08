import requests
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("شروع اجرای اسکریپت")

root = tk.Tk()
root.withdraw()

load_dotenv()
api_key = os.getenv('API_KEY')
url = (f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD")

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
output_dir = os.path.join(parent_dir, "exports")
os.makedirs(output_dir, exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename_csv = os.path.join(output_dir, f"exchange_rates_{timestamp}.csv")
filename_xlsx = os.path.join(output_dir, f"exchange_rates_{timestamp}.xlsx")

try:
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()
except requests.exceptions.RequestException as e:
    messagebox.showerror("Network Error", f"خطا در اتصال به API: \n{e}")
    exit()
except ValueError:
    messagebox.showerror("Parse Error", f"پاسخ API قابل تبدیل به JSON نبود.")
    exit()

if 'error' in data:
    logging.error(f"API Error: {data.get('error-type')}")
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

def save_with_prompt(df, path, write_func):
    if os.path.exists(path):
        res = messagebox.askyesnocancel("فایل موجود است", f"{path}آیا جایگزین شود؟")
        if res is None:
            return False
        elif not res:
            base, ext = os.path.splitext(path)
            path = f"{base}_new{ext}"
    write_func(path)
    return True

save_with_prompt(rates_df, filename_csv, lambda p: rates_df.to_csv(p, index=False, encoding="utf-8-sig"))
save_with_prompt(rates_df, filename_xlsx, lambda p: rates_df.to_excel(p, index=False, engine="openpyxl"))

logging.info(f"Saved CSV: {filename_csv}")
logging.info(f"Saved Excel: {filename_xlsx}")


# if os.path.exists(filename_csv):
#     result = messagebox.askyesnocancel("فایل موجود است",
#                                        f"{filename_csv} وجود دارد. \n آیا میخواهید جایگزین شود؟")
#     if result is None:
#         exit()
#     elif result:
#         pass
#     else:
#         filename_csv = os.path.join(output_dir, f"exchange_rates_{timestamp}_new.csv")
# rates_df.to_csv(filename_csv, index=False, encoding="utf-8-sig")

# if os.path.exists(filename_xlsx):
#     result = messagebox.askyesnocancel("فایل موجود است",
#                                        f"{filename_xlsx} وجود دارد. \n آیا میخواهید جایگزین شود؟")
#     if result is None:
#         exit()
#     elif result:
#         pass
#     else:
#         filename_xlsx = os.path.join(output_dir, f"exchange_rates_{timestamp}_new.xlsx")
# rates_df.to_excel(filename_xlsx, index=False, engine="openpyxl")

messagebox.showinfo("موفقیت", "فایل‌ها ذخیره شدند.")

