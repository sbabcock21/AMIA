from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.

import sys
base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable('SleepAligner.py', base=base, shortcutName='SleepAligner',shortcutDir='DesktopFolder',icon='sleep_icon.ico')
]

buildOptions = dict(
    packages = [],
    excludes = [],
    includes = ["atexit"],
    include_files = []
)

bdist_msi_options = dict(
    upgrade_code = '{64f92bf1-1e67-400a-ad2a-1ed71c924680}'
)

setup(
    name='SleepAligner',
    version = '1.1',
    description = 'A program to combine sleep log and actigraphy data for the Harvard sleep lab',
    options = dict(build_exe = buildOptions,
                   bdist_msi = bdist_msi_options),
    executables = executables
)