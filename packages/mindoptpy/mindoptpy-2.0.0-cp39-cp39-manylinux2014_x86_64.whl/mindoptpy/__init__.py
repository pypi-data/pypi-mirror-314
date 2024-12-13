import os
import platform
import subprocess
import sys

module_path = os.path.abspath(os.path.dirname(__file__))

lic_paths = []

def check_licenses(paths):
    for lic in ['mindopt.lic', 'fl_client.ini', 'ce_license.ini']:
        for path in paths:
            if os.path.exists(os.path.join(path, lic)):
                os.environ['MINDOPT_LICENSE_PATH'] = path
                return

# MINDOPT_LICENSE_PATH specify path
if 'MINDOPT_LICENSE_PATH' in os.environ:
    lic_paths.append(os.environ['MINDOPT_LICENSE_PATH'])

# HOME path
lic_paths.append(os.path.join(os.path.expanduser('~'), 'mindopt'))

# Full installer path
if 'MINDOPT_HOME' in os.environ:
    lic_paths.append(os.path.dirname(os.environ['MINDOPT_HOME']))

check_licenses(lic_paths)

# Reset MINDOPT_HOME for looking milp/miqcp libs
os.environ['MINDOPT_HOME'] = module_path

if platform.system() == "Windows":
    sys.path.append(os.path.join(module_path, 'win64-x86', 'lib'))
elif platform.system() == "Darwin":
    if subprocess.check_output(['sysctl', '-in', 'sysctl.proc_translated'], universal_newlines=True).strip() == "1":
        raise ImportError("MindOpt won't run in Rosetta environment. (Got virtual x86_64, actually arm64)")

from .mindoptpy import *