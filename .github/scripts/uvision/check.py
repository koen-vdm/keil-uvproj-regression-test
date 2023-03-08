# ####################################################################################
# @file uvision-check.py
#
# @brief checks Keil uVision 5 build output log files.
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

"""Checks Keil uVision 5 build output log files."""

import argparse

from common import findProjectFiles, getTargetsFromFile

parser = argparse.ArgumentParser(
    prog="uVisionCheck",
    description="checks build logs in repository produced by ARM Keil uVision 5.",
    epilog="This script will only work if the logs are in the expected place. \
                             which is next to the .uvprojx file with the name log.txt",
)
parser.add_argument(
    "-d", "--dir", default=".", help="The directory to search log files. default='.'"
)
parser.add_argument(
    "-t",
    "--targets",
    default=".github/config/targets.json",
    help="The targets \
                    definition file. default='.github/config/targets.json'",
)
args = parser.parse_args()

# markers indicating different failure modes of build
errors = [
    (
        "SDK not found",
        "error: no such file or directory: '../../../../..//sdk/platform/arch/main/hardfault_handler.c",
    ),
    (
        "wrong compiler version",
        "*** Please review the installed ARM Compiler Versions:",
    ),
]

passmarker = '.axf" - 0 Error(s),'

# get list of targets
targets = getTargetsFromFile(args.targets)

# get list of examples
projects = findProjectFiles(args.dir)

# projects = projects[0:3] # only build first few examples for debugging purposes

for t in targets:
    for p in projects:
        with open(p.basedir + "\\" + p.logfile) as log, open(p.path) as proj:
            if ("<TargetName>" + t.name + "</TargetName>") in proj.read():
                if (t.acronym + passmarker) in log.read():
                    t.passed.append(p)
                else:
                    t.failed.append(p)

# print output
for t in targets:
    print("\npassed " + t.name + ":")
    for p in t.passed:
        print(p.path)
    print("\nfailed " + t.name + ":")
    for f in t.failed:
        print(f.path)
    print("\n---------------")
    print("| PASSED: " + str(len(t.passed)) + " ")
    print("| FAILED: " + str(len(t.failed)) + " ")
    print("---------------")
