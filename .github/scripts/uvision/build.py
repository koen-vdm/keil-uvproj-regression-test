# ####################################################################################
# @file uvision-build.py
#
# @brief builds projects in repository using ARM Keil uVision 5. This will only work
# on a Windows machine that has Keil uVision 5 installed.
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

"""Builds projects in repository using ARM Keil uVision 5."""

import argparse
import subprocess

from common import bcolors, findProjectFiles

parser = argparse.ArgumentParser(
    prog="uVisionBuild",
    description="builds projects in repository using ARM Keil uVision 5.",
    epilog="Due to the dependency to Keil uVision 5 this script will only \
                              work on a Windows machine that has Keil uVision 5 installed. \
                              please be aware of the Keil license agreement before using this \
                              script. The build also depends on the DA145xx SDK6. The project \
                              must either be cloned inside the 'projects' folder of the SDK  \
                              or the projects must be linked using dlg_make_keil5_env_v2.000.py",
)
parser.add_argument(
    "-d",
    "--dir",
    default=".",
    help="The directory to search project files. \
                    default='.'",
)
args = parser.parse_args()

# get list of examples
projects = findProjectFiles(args.dir)

# projects = projects[0:3] # only build first few examples for debugging purposes

for p in projects:
    print(bcolors.OKBLUE + "building " + p.title + "..." + bcolors.ENDC)
    returncode = subprocess.call(
        ["C:/Keil_v5/UV4/UV4.exe", "-b", p.path, "-z", "-o", p.logfile]
    )
    # Keil returns 0 if build is ok, 1 if there are warnings, and 2-20 if there are errors
    colors = [bcolors.OKGREEN, bcolors.WARNING] + [bcolors.FAIL] * 18
    with open(p.basedir + p.logfile, "r") as f:
        print(colors[returncode] + f.read() + bcolors.ENDC)
