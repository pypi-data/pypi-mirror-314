#!/usr/bin/env python3
# coding: utf-8
from __future__ import annotations

import glob
import os.path
import platform
import sys

from volkanic.utils import under_home_dir


def _get_chrome_user_data_dir() -> str:
    # https://stackoverflow.com/a/13874620/2925169
    # https://newbedev.com/how-can-i-view-archived-google-chrome-history
    # -i-e-history-older-than-three-months
    if sys.platform == "darwin":
        return under_home_dir("Library/Application Support/Google/Chrome")
    elif sys.platform in ["linux", "linux2"]:
        return under_home_dir(".config/google-chrome/Default")
    elif sys.platform in ["win32", "cygwin", "msys"]:
        if platform.win32_ver()[0] in ["XP", "2000"]:
            return under_home_dir(
                r"Local Settings\Application Data",
                r"Google\Chrome\User Data",
            )
        else:
            return under_home_dir(r"\AppData\Local\Google\Chrome\User Data")
    else:
        raise RuntimeError("current platform is not supported")


def get_chrome_default_profile_dir() -> str:
    user_data_dir = _get_chrome_user_data_dir()
    names = ["Profile 1", "Default"]
    for name in names:
        path = os.path.join(user_data_dir, name)
        if os.path.exists(path):
            return path
    raise RuntimeError("chrome default profile dir is not found")


def under_chrome_default_dir(*paths) -> str:
    return os.path.join(get_chrome_default_profile_dir(), *paths)


def get_chrome_history_db_files() -> list[str]:
    pattern = os.path.join(_get_chrome_user_data_dir(), "*", "History")
    paths = glob.glob(pattern)
    paths.sort(key=os.path.getsize, reverse=True)
    return paths
