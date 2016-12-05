import re
import io
import os

# Point the script to your CSGO folder and it will get up to date skin IDs and names and output to item_index.txt

SteamPath = 'C:/Program Files (x86)/Steam/steamapps/common/Counter-Strike Global Offensive/'

skindata = {}
with open(os.path.join(SteamPath, 'csgo/scripts/items/items_game.txt'), 'r') as itemfile:
    start = False
    count = 0
    currnum = None

    for line in itemfile.readlines():
        if start:
            number = False
            tempdata = {}

            if re.match(r'^"\d*"$', line.strip()):
                currnum = int(line.strip().replace('"', ''))
                skindata[currnum] = {}
                number = True

            if '{' in line:
                count += 1
            if '}' in line:
                count -= 1

            if count == 0:
                start = False
                continue

            if line.strip() == '{' or line.strip() == '}':
                continue

            if currnum and not number:
                try:
                    first, second = line.strip().replace('"', '').split('\t\t')
                    skindata[currnum][first] = second
                except ValueError:
                    pass

        if line.strip() == '"paint_kits"':
            start = True

    skindata.pop(0)
    skindata.pop(9001)



namedata = {}
with io.open(os.path.join(SteamPath, 'csgo/resource/csgo_english.txt'), 'r', encoding='utf-16-le') as languagefile:
    # Steam language files are encoded in utf-16LE
    start = False
    count = 0
    currnum = None

    for line in languagefile.readlines():
        if line.strip() == '//Recipes':
            start = False
            break

        if start:
            if line.strip().startswith('"Paint'):
                tag, name = re.split(r'"\s+"', line.strip())

                if 'tag' in tag.lower():
                    namedata['#' + tag.replace('"', '').lower()] = name.replace('"', '')

        if line.strip() == '// Paint Kits':
            start = True


with open('item_index.txt', 'w') as outfile:
    for n in skindata:
        tag = skindata[n]['description_tag']

        outfile.write("%s: %s\n" % (n, namedata[tag.lower()].encode('utf-8')))
