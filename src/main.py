# src/main.py
import logging
import sys
from datetime import datetime
from pathlib import Path

from api import load_api_key_from_env, fetch_rates
from utils import build_rates_dataframe, ensure_output_dir, save_with_prompt

# configure root logger once
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    api_key = load_api_key_from_env()
    if not api_key:
        # use messagebox or CLI print depending on your UI mode
        from tkinter import messagebox
        messagebox.showerror("Error", "API_KEY not found in environment")
        sys.exit(1)

    base = "USD"
    try:
        data = fetch_rates(api_key, base=base, retries=2)
    except Exception as e:
        from tkinter import messagebox
        messagebox.showerror("Error", f"Failed to fetch rates: {e}")
        sys.exit(1)

    df = build_rates_dataframe(data)
    logger.info(df.head(10))

    project_root = Path(__file__).resolve().parent.parent
    out_dir = ensure_output_dir(project_root / "exports")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_path = out_dir / f"exchange_rates_{timestamp}.csv"
    xlsx_path = out_dir / f"exchange_rates_{timestamp}.xlsx"

    saved_csv = save_with_prompt(df, csv_path, lambda p: df.to_csv(p, index=False, encoding="utf-8-sig"))
    if not saved_csv:
        logger.info("CSV save cancelled by user")
    saved_xlsx = save_with_prompt(df, xlsx_path, lambda p: df.to_excel(p, index=False, engine="openpyxl"))
    if not saved_xlsx:
        logger.info("XLSX save cancelled by user")

    from tkinter import messagebox
    messagebox.showinfo("موفقیت", "فایل‌ها ذخیره شدند.")

if __name__ == "__main__":
    main()
