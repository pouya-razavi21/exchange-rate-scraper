"""
utils.py

Utility functions:
- build_rates_dataframe(data: dict) -> pandas.DataFrame
- ensure_output_dir(path: Union[str, Path]) -> Path
- save_with_prompt(df, path, write_func) -> Path|bool

This module uses pathlib for paths and returns Path objects.
"""

from typing import Union
from pathlib import Path
import logging

import pandas as pd
from tkinter import messagebox

logger = logging.getLogger(__name__)


def build_rates_dataframe(data: dict) -> pd.DataFrame:
    """
    Convert API JSON data into a cleaned pandas DataFrame.

    Parameters:
        data: parsed JSON from API (must contain "conversion_rates")

    Returns:
        DataFrame with columns ['Currency', 'Rate'], Rate as float rounded to 4 decimals,
        sorted descending by Rate, and reset index.
    """
    rates = data.get("conversion_rates", {})
    df = pd.DataFrame(list(rates.items()), columns=["Currency", "Rate"])
    # Ensure numeric and consistent rounding
    df["Rate"] = pd.to_numeric(df["Rate"], errors="coerce").round(4)
    df = df.dropna(subset=["Rate"])
    df = df.sort_values(by="Rate", ascending=False).reset_index(drop=True)
    return df


def ensure_output_dir(path: Union[str, Path]) -> Path:
    """
    Make sure output directory exists and return a Path object.

    Parameters:
        path: path to directory

    Returns:
        Path object for the directory.
    """
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def save_with_prompt(df: pd.DataFrame, path: Union[str, Path], write_func) -> Union[Path, bool]:
    """
    Save DataFrame to path, prompting user if file exists.

    Parameters:
        df: pandas DataFrame
        path: target Path or str
        write_func: callable receiving Path to write the DataFrame (e.g. lambda p: df.to_csv(p, ...))

    Returns:
        Path: final written Path on success (may be modified if user chose to save with "_new")
        False: if user cancelled
    """
    p = Path(path)
    if p.exists():
        # Ask user what to do
        res = messagebox.askyesnocancel("فایل موجود است", f"{p}\nآیا جایگزین شود؟")
        if res is None:
            logger.info("User cancelled save for %s", p)
            return False
        if not res:
            new_p = p.with_name(p.stem + "_new" + p.suffix)
            write_func(new_p)
            logger.info("Saved to new file: %s", new_p)
            return new_p
    write_func(p)
    logger.info("Saved file: %s", p)
    return p
