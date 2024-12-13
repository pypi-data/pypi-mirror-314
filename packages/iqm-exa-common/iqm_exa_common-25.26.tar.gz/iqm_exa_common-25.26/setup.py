#  ********************************************************************************
#  Copyright (c) 2019-2024 IQM Finland Oy.
#  All rights reserved. Confidential and proprietary.
#
#  Distribution or reproduction of any information contained herein
#  is prohibited without IQM Finland Oy’s prior written permission.
#  ********************************************************************************

from setuptools import setup
from pathlib import Path

def get_version():
    build_version_fpath = Path("version.txt")
    if build_version_fpath.exists():
        # Assume there's only one line specifying the version in the file
        return build_version_fpath.read_text().strip()
    return "0.1dev0"

if __name__ == "__main__":
    setup(version=get_version())
