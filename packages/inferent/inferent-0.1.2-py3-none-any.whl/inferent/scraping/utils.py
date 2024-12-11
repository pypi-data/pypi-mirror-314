"""Scraping utils"""

import json
import logging
import os
import shutil
from typing import List, Any, Tuple, Callable

import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(
    level=logging.INFO,
)
logger = logging.getLogger("scraping.utils")


def _load_checkpoint(
    folder_prefix: str, datatype: str = "dict"
) -> Tuple[List, Any]:
    folder_path = f"{folder_prefix}_checkpoint"
    os.makedirs(folder_path, exist_ok=True)

    already_list_path = os.path.join(folder_path, "already_list.json")
    already_data_path = os.path.join(folder_path, f"already_data.{datatype}")

    if os.path.exists(already_data_path):
        with open(already_list_path, "r", encoding="ascii") as f:
            already_list = json.load(f)

        if datatype in ["dict", "list", "item"]:
            with open(already_data_path, "r", encoding="ascii") as f:
                already_data = json.load(f)
        elif datatype == "df":
            already_data = pd.read_csv(already_data_path)
        else:
            raise ValueError(f"Unsupported datatype: {datatype}")
    else:
        already_list = []

        if datatype == "dict":
            already_data = {}
        elif datatype in ["list", "item"]:
            already_data = []
        elif datatype == "df":
            already_data = pd.DataFrame()
        else:
            raise ValueError(f"Unsupported datatype: {datatype}")

    return already_list, already_data


def _save_checkpoint(folder_prefix: str, already_list: List, already_data: Any):
    folder_path = f"{folder_prefix}_checkpoint"
    os.makedirs(folder_path, exist_ok=True)

    already_list_path = os.path.join(folder_path, "already_list.json")
    already_data_path = os.path.join(
        folder_path, f"already_data.{type(already_data).__name__}"
    )

    with open(already_list_path, "w", encoding="ascii") as f:
        json.dump(already_list, f)

    if isinstance(already_data, (dict, list)):
        with open(already_data_path, "w", encoding="ascii") as f:
            json.dump(already_data, f)
    elif isinstance(already_data, pd.DataFrame):
        already_data.to_csv(already_data_path, index=False)
    else:
        raise ValueError(f"Unsupported datatype: {type(already_data)}")


def _flush_checkpoint(folder_prefix: str):
    folder_path = f"{folder_prefix}_checkpoint"
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)


def checkpoint_scrape(
    folder_prefix: str,
    l: List,
    cb: Callable,
    datatype: str = "list",
    every: int = 5,
):
    """Scrapes a list l using a callback

    Keeps track of an intermediate storage such that if we have scraped an
    item, we do not re-scrape it.
    """
    already_list, already_data = _load_checkpoint(folder_prefix, datatype)

    counter = 0
    for ll in l:
        if ll in already_list:
            continue
        output = cb(l)

        if datatype == "item":
            assert isinstance(output, list), "Wrong datatype"
            already_data.append(output)
        if datatype == "list":
            assert isinstance(output, list), "Wrong datatype"
            already_data.extend(output)
        if datatype == "dict":
            assert isinstance(output, dict), "Wrong datatype"
            already_data.update(output)
        elif datatype == "df":
            assert isinstance(output, pd.DataFrame), "Wrong datatype"
            already_data = pd.concat([already_data, output], axis=1)

        already_list.append(ll)

        counter += 1
        if counter >= every:
            _save_checkpoint(folder_prefix, already_list, already_data)

    # We've hit the end!
    _flush_checkpoint(folder_prefix)
    return already_data


def title_cond(title_text: str) -> "Callable[[WebDriver], bool]":
    """Shortcut for title condition, used often"""
    return EC.title_contains(title_text)


def css_cond(css_text: str) -> "Callable[[WebDriver], bool]":
    """Shortcut for css condition, used often"""
    return EC.presence_of_element_located((By.CSS_SELECTOR, css_text))
