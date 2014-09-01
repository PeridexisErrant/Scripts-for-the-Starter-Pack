import os
import fnmatch
import fileinput
import shutil
import re
import zipfile
import hashlib

print('A script to prepare the DF Starter Pack for upload.')
print('Run from parent folder of pack.\n')

#get variables
for folder in os.listdir('.'):
    if fnmatch.fnmatch(folder, 'Dwarf Fortress 40_?? Starter Pack r*'):
        version_str = folder.replace('Dwarf Fortress ', '').replace('Starter Pack ', '')
        version_list = re.split('_| ', version_str)
        major_version_str, minor_version_str, pack_version_str = version_list[0], version_list[1], version_list[2]

        pack_folder_str = folder
        graphics_folder = folder + '/LNP/graphics/'
        utilities_folder = folder + '/LNP/utilities/'
        data_folder = folder + '/Dwarf Fortress 0.40.' + minor_version_str + '/data/'

        problems = 0
        break

# check LNPWin has 'version: 0', and if not fix that line
fixing_file = False
with fileinput.input(files=(pack_folder_str + '/LNP/LNPWin.txt')) as f:
    for line in f:
        if fileinput.isfirstline():
            if line == 'version: 0\n':
                print('LNPWin version string is OK')
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
    print('LNPWin version string was fixed OK')
    problems += 1

# check if embark profiles are installed, and if not copy them from defaults folder
if os.path.isfile(data_folder + 'init/embark_profiles.txt'):
    print('Embark profile install is OK')
else:
    shutil.copy2(pack_folder_str + '/LNP/defaults/embark_profiles.txt', data_folder + 'init/')
    print('Embark profiles were installed OK')
    problems += 1

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
            elif line == '</configuration>':
                print(line)
            else:
                print(line[:-1])
    print('Soundsense configuration was fixed OK')
    problems += 1

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
    problems += 1

# check that graphics are installed
if os.path.isfile(data_folder + 'art/Phoebus_16x16.png'):
    print('Phoebus graphics install is OK')
else:
    print('Warning!    Phoebus graphics are not installed')
    problems += 1

# check that graphics are simplified
for folder in os.listdir(graphics_folder):
    if os.path.isfile(graphics_folder + folder + '/Dwarf Fortress.exe'):
        print('Warning!    ', folder, 'graphics pack is not simplified\n')
        problems += 1

# check that a compatible DT memory layout is present
for folder in os.listdir(utilities_folder):
    if fnmatch.fnmatch(folder, 'Dwarf Therapist *'):
        DT_memory_layout = utilities_folder + folder + '/etc/memory_layouts/windows/v0.40.' + minor_version_str + '_graphics.ini'
if os.path.isfile(DT_memory_layout):
    print('Therapist memory layout is OK\n')
else:
    print('Warning!    Dwarf Therapist memory layout for this version is missing\n')
    problems += 1

make_pack = False
if problems == 0:
    update = input('Do you want to zip the pack '
                   'and prepare docs?  ("y" for yes)\n    ')
    if update == 'y':
        make_pack = True

if make_pack:
    # create zip, and move to past packages.  Remove older zip if present.
    if os.path.isfile(pack_folder_str + '.zip'):
        os.remove(pack_folder_str + '.zip')

    zf = zipfile.ZipFile(pack_folder_str + '.zip', 'w', zipfile.ZIP_DEFLATED)
    for dirname, subdirs, files in os.walk(pack_folder_str):
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
    zf.close()

    # get MD5 checksum of zip
    md5 = hashlib.md5()
    with open(pack_folder_str + '.zip', 'rb') as f: 
        for chunk in iter(lambda: f.read(8192), b''): 
            md5.update(chunk)
    MD5 = md5.hexdigest().upper()

    # copy and update documentation
    for item in ['forum_post.txt', 'contents_and_changelog.txt']:
        if os.path.isfile(item):
            os.remove(item)
    shutil.copy(pack_folder_str+'/LNP/About/pack contents and changelog.txt'
                , 'contents_and_changelog.txt')

    with fileinput.input(files=('contents_and_changelog.txt'), inplace=True) as f:
        for line in f:
            if line.startswith('[tr][td]' + version_str + '[/td][td]'):
                print('[tr][td]' + version_str + '[/td][td]' + MD5 + '[/td][/tr]')
            else:
                print(line.replace('\n',''))

    # create template forum post
    changelog_list = []
    changelog = False
    for line in open('contents_and_changelog.txt', 'r'):
        if line.strip() == version_str:
            changelog = True
            continue
        if changelog:
            if line == '\n':
                break
            changelog_list.append(line)

    with open('forum_post.txt', 'a') as f:
        f.write('The Starter Pack has updated to ' + version_str + '!  As usual, [url='
                'http://dffd.wimbli.com/file.php?id=7622]you can get it here.[/url]\n')
        f.write('\nChangelog:\n')
        for line in changelog_list:
            f.write(line)
        f.write('\nMD5:  ' + MD5)

    print('\nDone!  Pack ready for upload')
