import os, fnmatch, fileinput, shutil, re, zipfile, hashlib, urllib.request, filecmp, glob

def main():
    """Call all the components of the script."""
    get_variables()
    global tests
    tests = []

    tests.append(keybinds())
    tests.append(documentation())
    tests.append(pylnp_json())
    tests.append(embark_profiles())
    tests.append(soundsense_config())
    tests.append(announcement_filter())
    tests.append(graphics_installed_and_all_simplified())
    tests.append(misc_files())
    tests.append(dwarf_therapist())
    tests.append(twbt_config_and_files())
    
    for tup in tests:
        print('{0:27} {1:}'.format(tup[0], tup[1]))
    for tup in tests:
        if not tup[1] == 'is OK':
            raise SystemExit
    if make_pack():
        prep_pack_for_upload()


def get_variables():
    """Set up a lot of paths as global variables (bad but easy!)"""
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
    """Checks various little bits."""
    files = ['/PyLNP.user', '/stderr.txt', '/stdout.txt']
    for k in files:
        if os.path.isfile(pack_folder_str+k):
            os.remove(pack_folder_str+k)
    with open(DF_folder + '/gamelog.txt', 'w') as f:
        f.write('')
    if not all(os.path.exists(DF_folder + os.path.relpath(f, pack_folder_str + '/LNP/extras/'))
               for f in glob.glob(pack_folder_str + '/LNP/extras/*')):
        # note: this only checks top-level files and folders, not all files
        tests.append(('Extras files', 'need installation'))
    if not os.path.isfile(DF_folder + 'dfhack.init'):
        return 'dfhack.init', 'not found'
    return 'misc. file status', 'is OK'


def keybinds():
    """Check that keybindings haven't changed between versions"""
    if filecmp.cmp(data_folder + 'init/interface.txt',
                   pack_folder_str + '/LNP/keybinds/Vanilla DF.txt',
                   shallow=False):
        return 'Keybinds status', 'is OK'
    return 'Keybinds status', 'needs updating'


def documentation():
    """Check contents list, changelog, and documentation."""
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
    """Check and update version string in PyLNP.json"""
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
    """Check if embark profiles are installed, and if not copy them from defaults folder."""
    if os.path.isfile(data_folder + 'init/embark_profiles.txt'):
        return 'Embark profile install', 'is OK'
    else:
        shutil.copy2(pack_folder_str + '/LNP/defaults/embark_profiles.txt', data_folder + 'init/')
        return 'Embark profile install', 'was fixed'
    # later: check that the embarks in /extras/ are the same as in /defaults/

def soundsense_config():
    """Check soundsense config and update if required."""
    if os.path.isfile(DF_folder + '/hack/scripts/soundsense.lua'):
        lua_was_ok = True
    else:
        shutil.copyfile(utilities_folder + '/soundsense/dfhack/scripts/soundsense.lua', DF_folder + '/hack/scripts/soundsense.lua')
        lua_was_ok = False
    soundsense_lines = 0
    with fileinput.input(files=(utilities_folder + '/soundsense/configuration.xml')) as f:
        for line in f:
            if (fileinput.lineno() == 3) or (fileinput.lineno() == 5):
                if '0.40.' + minor_version_str in line:
                    soundsense_lines += 1
    if soundsense_lines == 2:
        if lua_was_ok:
            return 'Soundsense configuration', 'is OK'
        else:
            return 'Soundsense configuration', 'was fixed'
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
    """Check announcement filter config and update if required."""
    folder = glob.glob(utilities_folder + 'DF Announcement Filter*')
    if folder:
        AF_settings_file = folder[0] + '/settings.txt'
    else:
        return 'Announcement Filter path', 'not found'
    update_path, line_is_path, line_int = False, False, -1
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
    """Check that I haven't forgotten to copy over a graphics pack."""
    # later, can I pull from Fricy's repo to fix this?
    packs = ['ASCII Default', 'CLA', 'Ironhand', 'Mayday',
             'Obsidian', 'Phoebus', 'Spacefox']
    for p in packs:
        if not os.path.isdir(graphics_folder + p):
            tests.append(('Graphics pack:  ' + p, 'not found'))

    """Check that graphics are simplified."""
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
    """Check that DT memory layout for the current version is present."""
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
    """Check if TwbT is installed."""    
    if not os.path.isfile(plugins_folder + 'twbt.plug.dll'):
        return 'TwbT plugin', 'not installed'
        
    # note: much of this can be removed once PyLNP updates it's tileset support

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
    """Get user bool to continue or not."""
    update = input('\nDo you want to zip the pack '
                   'and prepare docs?  ("y" for yes)\n    ')
    if update == 'y':
        return True
    else:
        return False

def prep_pack_for_upload():
    """Create zip, create updated documentation, etc."""
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

    # rename folder, to avoid removing checksum from docs etc.
    next_pack_name = ('Dwarf Fortress '+major_version_str+'_'+minor_version_str+
                      ' Starter Pack r'+str(int(pack_version_str[1:])+1))
    os.rename(pack_folder_str, next_pack_name)

    print('\nDone!  Pack ready for upload')

if __name__ == '__main__':
    main()
