import os, fnmatch, fileinput, shutil, re, zipfile, hashlib, urllib.request

def main():
    get_variables()
    global tests
    tests = []

    tests.append(misc_files())
    tests.append(documentation())
    tests.append(pylnp_json())
    tests.append(embark_profiles())
    tests.append(soundsense_config())
    tests.append(announcement_filter())
    tests.append(graphics_installed_and_all_simplified())
    tests.append(dwarf_therapist())
    if os.path.isfile(plugins_folder + 'twbt.plug.dll'):
        tests.append(twbt_config_and_files())
    
    for tup in tests:
        print('{0:27} {1:}'.format(tup[0], tup[1]))
    for tup in tests:
        if not tup[1] == 'is OK':
            raise SystemExit
    if make_pack():
        prep_pack_for_upload()


def get_variables():
    print('A script to prepare the DF Starter Pack for upload.')
    print('Run from parent folder of pack.\n')

    global version_str, major_version_str, minor_version_str, pack_version_str
    global pack_folder_str, graphics_folder, utilities_folder, data_folder, plugins_folder, DF_folder
    #get variables
    for folder in os.listdir('.'):
        if fnmatch.fnmatch(folder, 'Dwarf Fortress 40_?? Starter Pack r*'):
            version_str = folder.replace('Dwarf Fortress ', '').replace('Starter Pack ', '')
            version_list = re.split('_| ', version_str)
            major_version_str, minor_version_str, pack_version_str = version_list[0], version_list[1], version_list[2]

            pack_folder_str = folder
            DF_folder = folder + '/Dwarf Fortress 0.40.' + minor_version_str + '/'
            graphics_folder = folder + '/LNP/graphics/'
            utilities_folder = folder + '/LNP/utilities/'
            data_folder = folder + '/Dwarf Fortress 0.40.' + minor_version_str + '/data/'
            plugins_folder = folder + '/Dwarf Fortress 0.40.' + minor_version_str + '/hack/plugins/'
            break
    if not os.path.isdir(data_folder):
        print('Warning!    DF folder is malformed!')
        raise SystemExit


def misc_files():
    if os.path.isfile(pack_folder_str+'/PyLNP.user'):
        os.remove(pack_folder_str+'/PyLNP.user')
    if not os.path.isfile(DF_folder + 'dfhack.init'):
        return 'dfhack.init', 'not found'
    return 'dfhack.init', 'is OK'


def documentation():
    # check contents and changelog documentation
    docs_ok = True
    changelog, hashline = False, 0
    with fileinput.input(files=(pack_folder_str + '/LNP/About/pack contents and changelog.txt')) as f:
        for line in f:
            if changelog:
                if line == '\n':
                    break
                elif len(line) < 10:
                    docs_ok = False
            elif line.startswith('[tr][td]'):
                if ((hashline == 1 and not line == '[tr][td]'+version_str+'[/td][td]unavailable[/td][/tr]\n')
                    or (hashline > 1 and 'unavailable' in line)):
                    docs_ok = False
                hashline += 1
            elif line.strip() == version_str:
                changelog = True
    if not docs_ok:
        changelog, hashline = False, 0
        with fileinput.input(files=(pack_folder_str + '/LNP/About/pack contents and changelog.txt'), inplace=True) as f:
            for line in f:
                if changelog:
                    # remove short lines
                    if line == '\n':
                        print()
                        changelog = False
                    elif len(line) < 10:
                        continue
                    elif line.startswith('40_'):
                        changelog = False
                        print('\n'+line[:-1])
                    else:
                        print(line[:-1])
                elif line.startswith('[tr][td]'):
                    if hashline == 1:
                        if version_str in line:
                            print('[tr][td]'+version_str+'[/td][td]unavailable[/td][/tr]')
                        else:
                            print('[tr][td]'+version_str+'[/td][td]unavailable[/td][/tr]')
                            print(line[:-1])
                    elif 'unavailable' in line:
                        continue
                    else:
                        print(line[:-1])
                    hashline += 1
                elif line.strip() == version_str:
                    changelog = True
                    print(line[:-1])
                else:
                    print(line[:-1])
        return 'Pack documentation', 'was fixed'
    else:
        return 'Pack documentation', 'is OK'

def pylnp_json():
    # check and update version string in PyLNP.json
    if os.path.isfile(pack_folder_str + '/LNP/PyLNP.json'):
        with open(pack_folder_str + '/LNP/PyLNP.json') as f:
            if '"packVersion": "'+version_str in f.read():
                return 'Version in PyLNP.json',  'is OK'
            else:
                badjson = True
        if badjson:
            with fileinput.input(files=(pack_folder_str + '/LNP/PyLNP.json'), inplace=True) as f:
                for line in f:
                    if line.startswith('        "packVersion": "'):
                        print('        "packVersion": "'+version_str+'"')
                    else:
                        print(line[:-1])
            return 'PyLNP.json version string', 'was fixed'

def embark_profiles():
    # check if embark profiles are installed, and if not copy them from defaults folder
    if os.path.isfile(data_folder + 'init/embark_profiles.txt'):
        return 'Embark profile install', 'is OK'
    else:
        shutil.copy2(pack_folder_str + '/LNP/defaults/embark_profiles.txt', data_folder + 'init/')
        return 'Embark profile install', 'was fixed'

def soundsense_config():
    # check soundsense config and update if required
    soundsense_lines = 0
    with fileinput.input(files=(utilities_folder + '/soundsense/configuration.xml')) as f:
        for line in f:
            if (fileinput.lineno() == 3) or (fileinput.lineno() == 5):
                if '0.40.' + minor_version_str in line:
                    soundsense_lines += 1
    if soundsense_lines == 2:
        return 'Soundsense configuration', 'is OK'
    else:
        with fileinput.input(files=(utilities_folder + '/soundsense/configuration.xml'), inplace=True) as f:
            for line in f:
                if fileinput.lineno() == 3:
                    print('\t' '<gamelog encoding="Cp850" path="..\\..\\..\\Dwarf Fortress 0.40.' + minor_version_str + '\\gamelog.txt"/>')
                elif fileinput.lineno() == 5:
                    print('\t\t' '<item path="..\\..\\..\\Dwarf Fortress 0.40.' + minor_version_str + '\\ss_fix.log"/>')
                elif line == '</configuration>':
                    print(line)
                    break
                else:
                    print(line[:-1])
        return 'Soundsense configuration', 'was fixed'

def announcement_filter():
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
                return 'Announcement Filter path', 'is OK'
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
        return 'Announcement Filter path', 'was fixed'

def graphics_installed_and_all_simplified():
    # check that graphics are simplified
    for folder in os.listdir(graphics_folder):
        if os.path.isfile(graphics_folder + folder + '/Dwarf Fortress.exe'):
            # we can't return here, so we append directly to the list (cheeky)
            tests.append((folder + ' graphics pack', 'not simplified'))
    # check that graphics are installed
    if os.path.isfile(data_folder + 'art/Phoebus_16x16.png'):
       return 'Phoebus graphics install', 'is OK'
    else:
        return 'Phoebus graphics', 'not installed'


def dwarf_therapist():
    # check that a compatible DT memory layout is present
    memory_layout_file = 'v0.40.' + minor_version_str + '_graphics.ini'
    for folder in os.listdir(utilities_folder):
        if fnmatch.fnmatch(folder, 'Dwarf*Therapist*'):
            DT_layout_path = utilities_folder + folder + '/share/memory_layouts/windows/'
    if os.path.isfile(DT_layout_path + memory_layout_file):
        return 'Therapist memory layout', 'is OK'
    else:
        url = str('https://raw.githubusercontent.com/splintermind/'
                  'Dwarf-Therapist/DF2014/share/memory_layouts/windows/'
                  + memory_layout_file)
        try:
            url_content = urllib.request.urlopen(url).read().decode(encoding='UTF-8')
            with open(DT_layout_path + memory_layout_file, 'w') as f:
                f.write(url_content)
            return 'Therapist memory layout', 'was downloaded'
        except:
            return 'Therapist memory layout', 'not available!'

def twbt_config_and_files():
    # check if TwbT is installed
    TwbT_folder = 'DF addons (zipped)/TwbT/'

    # folders to install to:
    graphics_packs = []
    for d in os.listdir(graphics_folder):
        if os.path.isdir(graphics_folder + d):
            if not 'ascii' in d.lower():
                graphics_packs.append(d)

    # install files to graphics packs
    problem_packs = set()
    for pack in graphics_packs:
        art_folder = graphics_folder + pack + '/data/art/'
        init_folder = graphics_folder + pack + '/data/init/'

        # files to copy into each graphics pack
        to_copy_list = ['shadows.png',
                        'overrides.txt',
                        'Vanilla DF - 24x - Items.png',
                        'curses_640x300.png']

        # copy all the items into place if not present
        for item in os.listdir(TwbT_folder):
            for string in to_copy_list:
                if string in item and item.endswith('.png') and not os.path.isfile(art_folder + item):
                    shutil.copy(TwbT_folder + item, art_folder)
                    problem_packs.add(pack)
                elif string in item and item.endswith('.txt') and not os.path.isfile(init_folder + item):
                    shutil.copy(TwbT_folder + item, init_folder)
                    problem_packs.add(pack)
        
        # edit init files to work with TwbT
        init_OK = True
        for string in ['[FONT:curses_640x300.png]'
                       , '[FULLFONT:curses_640x300.png]'
                       , '[PRINT_MODE:TWBT]']:
            if not string in open(init_folder+'init.txt').read():
                init_OK = False
        if not init_OK:
            with fileinput.input(files=(graphics_folder + pack + '/data/init/init.txt')
                                 , inplace=True) as f:
                for line in f:
                    if line.startswith('[FONT:'):
                        print('[FONT:curses_640x300.png]')
                    elif line.startswith('[FULLFONT:'):
                        print('[FULLFONT:curses_640x300.png]')
                    elif line.startswith('[PRINT_MODE:'):
                        print('[PRINT_MODE:TWBT]')
                    else:
                        print(line[:-1])
            problem_packs.add(pack)
    # print messages if things were changed
    if not len(problem_packs) == 0:
        for pack in problem_packs:
            tests.append((pack + ' TwbT graphics', 'was fixed'))
    else:
        tests.append(('Each TwbT file install', 'is OK'))
    
    return 'TwbT plugin install', 'is OK'

#########################################################################

def make_pack():
    print()
    update = input('Do you want to zip the pack '
                   'and prepare docs?  ("y" for yes)\n    ')
    if update == 'y':
        return True
    else:
        return False

def prep_pack_for_upload():
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

    # insert checksum in old non-zipped docs
    hashline = 0
    with fileinput.input(files=(pack_folder_str + '/LNP/About/pack contents and changelog.txt'), inplace=True) as f:
        for line in f:
            if line.startswith('[tr][td]' + version_str + '[/td][td]'):
                print('[tr][td]' + version_str + '[/td][td]' + MD5 + '[/td][/tr]')
            else:
                print(line.replace('\n',''))

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

if __name__ == '__main__':
    main()
