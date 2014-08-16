import os
import fnmatch
import fileinput

print('A script to automatically update version strings in the DF Starter Pack')
print('Run at top level of pack.\n')

version_str = input('Input DF version to update to, in format "40_01":\n    ')

#get variables
version_list = version_str.split('_')
major_version_str, minor_version_str = version_list[0], version_list[1]
for folder in os.listdir('.'):
    if fnmatch.fnmatch(folder, 'Dwarf Fortress 40_?? Starter Pack r*'):
        pack_folder_str = folder
        graphics_folder = folder + '/LNP/graphics/'
        utilities_folder = folder + '/LNP/utilities/'
        data_folder = folder + '/Dwarf Fortress 0.40.' + minor_version_str + '/data/'

# check folder name
if os.path.exists(pack_folder_str + '/Dwarf Fortress 0.' + major_version_str + '.' + minor_version_str):
    pass
else:
    print('Entered version does not match DF folder name, aborting now!')
    exit()

# check LNPWin has 'version: 0'
with fileinput.input(files=(pack_folder_str + '/LNP/LNPWin.txt')) as f:
    for line in f:
        if fileinput.isfirstline():
            if line == 'version: 0\n':
                print('\nLNPWin version string is OK\n')
            else:
                print('\nWarning!    LNPWin version string needs to be updated\n')
                # can later rewrite line here to fix this

# check if embark profiles are installed
if os.path.isfile(data_folder + 'init/embark_profiles.txt'):
    print('Embark profiles are installed\n')
else:
    print('Warning!    Embark profiles are not installed\n')

# check soundsense config
soundsense_lines = 0
with fileinput.input(files=(utilities_folder + '/soundsense/configuration.xml')) as f:
    for line in f:
        if (fileinput.lineno() == 3) or (fileinput.lineno() == 5):
            if '0.40.' + minor_version_str in line:
                soundsense_lines += 1
                # can later rewrite line here to fix this
if soundsense_lines == 2:
    print('Soundsense configuration is OK\n')
else:
    print('Warning!    Soundsense configuration needs to be updated\n')

# check announcement filter config
for folder in os.listdir(utilities_folder):
    if fnmatch.fnmatch(folder, 'DF Announcement Filter 1.1'):
        AF_settings_file = utilities_folder + folder + '/settings.txt'
line_is_path = False
for line in open(AF_settings_file):
    if line_is_path:
        if line == '..\..\..\Dwarf Fortress 0.40.' + minor_version_str + '\n':
            print('Announcement Filter path setting is OK\n')
        else:
            print('Warning!    Announcement Filter path setting needs to be updated\n')
            # can later rewrite here to update the line
        break
    if line == '[DFPath]\n':
        line_is_path = True

# check that graphics are installed
if os.path.isfile(data_folder + 'art/Phoebus_16x16.png'):
    print('Phoebus graphics are installed\n')
else:
    print('Warning!    Phoebus graphics are not installed\n')

# check that graphics are simplified
for folder in os.listdir(graphics_folder):
    if os.path.isfile(graphics_folder + folder + '/Dwarf Fortress.exe'):
        print('Warning!    ', folder, 'graphics pack is not simplified\n')

# check that a compatible DT memory layout is present
for folder in os.listdir(utilities_folder):
    if fnmatch.fnmatch(folder, 'Dwarf Therapist *'):
        DT_memory_layout = utilities_folder + folder + '/etc/memory_layouts/windows/v0.40.' + minor_version_str + '_graphics.ini'
if os.path.isfile(DT_memory_layout):
    print('Therapist memory layout exists')
else:
    print('Warning!    Dwarf Therapist memory layout for this version is missing')

# reminders to check save compatibility and bump 'for version x' on dffd
print('\nReminders:\n    - check save compatibility with previous version')
print('    - update "for version 40.xx" on DFFD')
