import os
import fnmatch
import fileinput
import shutil

print('A script to automatically update version strings in the DF Starter Pack')
print('Run from parent folder of pack.\n')

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

# check folder name, and if it doesn't match user input abort script
if os.path.exists(pack_folder_str + '/Dwarf Fortress 0.' + major_version_str + '.' + minor_version_str):
    pass
else:
    print('Entered version does not match DF folder name, aborting now!')
    exit()

# check LNPWin has 'version: 0', and if not fix that line
fixing_file = False
with fileinput.input(files=(pack_folder_str + '/LNP/LNPWin.txt')) as f:
    for line in f:
        if fileinput.isfirstline():
            if line == 'version: 0\n':
                print('\nLNPWin version string is OK')
                break
            else:
                fixing_file = True
                break
if fixing_file:
    with fileinput.input(files=(pack_folder_str + '/LNP/LNPWin.txt'), inplace=True) as f:
        for line in f:
            if fileinput.isfirstline():
                print('version: 0')
            else:
                print(line[:-1])
    print('\nLNPWin version string was fixed OK')

# check if embark profiles are installed, and if not copy them from defaults folder
if os.path.isfile(data_folder + 'init/embark_profiles.txt'):
    print('Embark profile install is OK')
else:
    shutil.copy2(pack_folder_str + '/LNP/defaults/embark_profiles.txt', data_folder + 'init/')
    print('Embark profiles were installed OK')

# check soundsense config and update if required
soundsense_lines = 0
with fileinput.input(files=(utilities_folder + '/soundsense/configuration.xml')) as f:
    for line in f:
        if (fileinput.lineno() == 3) or (fileinput.lineno() == 5):
            if '0.40.' + minor_version_str in line:
                soundsense_lines += 1
if soundsense_lines == 2:
    print('Soundsense configuration is OK')
else:
    with fileinput.input(files=(utilities_folder + '/soundsense/configuration.xml'), inplace=True) as f:
        for line in f:
            if fileinput.lineno() == 3:
                print('\t' '<gamelog encoding="Cp850" path="..\\..\\..\\Dwarf Fortress 0.40.' + minor_version_str + '\\gamelog.txt"/>')
            elif fileinput.lineno() == 5:
                print('\t\t' '<item path="..\\..\\..\\Dwarf Fortress 0.40.' + minor_version_str + '\\ss_fix.log"/>')
            else:
                print(line[:-1])
    print('Soundsense configuration was fixed OK')

# check announcement filter config and update if required
for folder in os.listdir(utilities_folder):
    if fnmatch.fnmatch(folder, 'DF Announcement Filter 1.1'):
        AF_settings_file = utilities_folder + folder + '/settings.txt'
update_path = False
line_is_path = False
line_int = -1
for line in open(AF_settings_file):
    if line_is_path:
        if line == '..\..\..\Dwarf Fortress 0.40.' + minor_version_str + '\n':
            print('Announcement Filter path is OK')
        else:
            update_path = True
        break
    if line == '[DFPath]\n':
        line_is_path = True
if update_path:
    with fileinput.input(files=(AF_settings_file), inplace=True) as f:
        for line in f:
            if line == '[DFPath]\n':
                line_int = fileinput.lineno() + 1
            if fileinput.lineno() == line_int:
                print('..\..\..\Dwarf Fortress 0.40.' + minor_version_str)
            else:
                print(line[:-1])
    print('Announcement Filter path was updated OK')

# check that graphics are installed
if os.path.isfile(data_folder + 'art/Phoebus_16x16.png'):
    print('Phoebus graphics instal is OK')
else:
    print('Warning!    Phoebus graphics are not installed')

# check that graphics are simplified
for folder in os.listdir(graphics_folder):
    if os.path.isfile(graphics_folder + folder + '/Dwarf Fortress.exe'):
        print('Warning!    ', folder, 'graphics pack is not simplified\n')

# check that a compatible DT memory layout is present
for folder in os.listdir(utilities_folder):
    if fnmatch.fnmatch(folder, 'Dwarf Therapist *'):
        DT_memory_layout = utilities_folder + folder + '/etc/memory_layouts/windows/v0.40.' + minor_version_str + '_graphics.ini'
if os.path.isfile(DT_memory_layout):
    print('Therapist memory layout is OK\n')
else:
    print('Warning!    Dwarf Therapist memory layout for this version is missing\n')

# reminders to check save compatibility and bump 'for version x' on dffd
print('Reminders:\n    - check save compatibility with previous version')
print('    - update "for version 40.xx" on DFFD')
