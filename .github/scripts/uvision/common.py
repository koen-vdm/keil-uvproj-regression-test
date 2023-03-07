# ####################################################################################
# @file uvision-common.py
#
# @brief common classes and functions used for uVision 5 build and check script.
#
# Copyright (c) 2023 Dialog Semiconductor. All rights reserved.
#
# This software ("Software") is owned by Dialog Semiconductor. By using this Software
# you agree that Dialog Semiconductor retains all intellectual property and proprietary
# rights in and to this Software and any use, reproduction, disclosure or distribution
# of the Software without express written permission or a license agreement from Dialog
# Semiconductor is strictly prohibited. This Software is solely for use on or in
# conjunction with Dialog Semiconductor products.
#
# EXCEPT AS OTHERWISE PROVIDED IN A LICENSE AGREEMENT BETWEEN THE PARTIES OR AS
# REQUIRED BY LAW, THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. EXCEPT AS OTHERWISE PROVIDED
# IN A LICENSE AGREEMENT BETWEEN THE PARTIES OR BY LAW, IN NO EVENT SHALL DIALOG
# SEMICONDUCTOR BE LIABLE FOR ANY DIRECT, SPECIAL, INDIRECT, INCIDENTAL, OR
# CONSEQUENTIAL DAMAGES, OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR
# PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,
# ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THE SOFTWARE.
#
# #####################################################################################

"""Common classes and functions used for uVision 5 build and check script."""

import json
import os


class Target:
    """Build targets are devices for which the build is intended."""

    def __init__(self, name, acronym):
        """Initialize the target using only the name and acronym."""
        self.name = name
        self.acronym = acronym
        self.metadata = []
        self.passed = []
        self.failed = []


def getTargetsFromFile(file):
    """Get a list with target devices."""
    targetlist = []
    f = open(file)
    targetsData = json.load(f)
    for tD in targetsData:
        targetlist.append(Target(tD["name"], tD["acronym"]))
    return targetlist


class Project:
    """Projects are all of the individual uVision project files in this repository."""

    def __init__(self, path):
        """Initialize the Project using the path."""
        self.path = path
        self.filename = path.split("\\")[len(path.split("\\")) - 1]
        self.title = self.filename.replace(".uvprojx", "")
        self.basedir = self.path.replace(self.filename, "")
        self.logfile = self.title + "_log.txt"

    def findLog(self):
        """Get corresponding log file."""
        return {"path": self.path, "group": self.group, "title": self.title}


def findProjectFiles(directory):
    """Get a list with ubprojx files in a directory."""
    filelist = []
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            if str(f).endswith(".uvprojx"):
                filelist.append(Project(os.path.abspath(os.path.join(dirpath, f))))
    return filelist
