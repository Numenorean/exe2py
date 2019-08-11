import os
import re
import shutil
import random
import zipfile
import binascii
import uncompyle6
import pyinstxtractor


def get_libs(main_file):
    libs = []
    try:
        f = open('../'+main_file.replace('.exe', '')+'_source.py/'+main_file.replace('.exe', '')+'_source.py', 'r')
    except:
        f = open('../'+source+'/'+source, 'r')
    lines = f.readlines()
    for line in lines:
            if line[0:6] == 'import':
                libs += re.sub('\sas\s\w+', '', re.search('import\s(.+\\n)', line).group(1)).replace('\n', '').split(', ')
            elif line[0:4] == 'from':
                libs.append(re.search('from\s(.+)\simport\s.+\\n', line).group(1))
            else:pass
    f.close()
    return libs
    

def main_source(file, source):
    global bindata, source_file
    source_file = file
    if source == '':
        source = '_source.py'
    arch = pyinstxtractor.PyInstArchive(file)
    if arch.open():
            if arch.checkFile():
                if arch.getCArchiveInfo():
                    arch.parseTOC()
                    arch.extractFiles()
                    arch.close()
                    print('[*] Successfully extracted pyinstaller archive: {0}'.format(file))
            arch.close()
    if os.path.isfile(file.replace('.exe', '')) != True:
        print('[*] Not found {} file!'.format(file.replace('.exe', '')))
        file = input('[?] Select a "Possible entry point" file from the top list -> ')+'.exe'
    try:os.remove(file.replace('exe', 'pyc'))
    except:pass
    os.rename(file.replace('.exe', ''), file.replace('exe', 'pyc'))
    pycfile = file.replace('exe', 'pyc')
    archive = zipfile.ZipFile('base_library.zip', 'r')
    bindata = binascii.unhexlify(binascii.hexlify(archive.read('abc.pyc')).split(b'e3')[0])
    archive.close()
    open('newf5a99.pyc', 'w').close()
    with open('newf5a99.pyc', 'r+b') as new:
        new.write(bindata)
        with open(pycfile, 'rb') as old:
            new.write(old.read())
    os.remove(pycfile)
    os.rename('newf5a99.pyc', pycfile)
    if source == '_source.py':
        if os.path.isdir('../'+file.replace('.exe', '')+source) != True:
            os.mkdir('../'+file.replace('.exe', '')+source)
        with open('../'+file.replace('.exe', '')+source+'/'+file.replace('.exe', '')+'_source.py', "w") as fileobj:
            uncompyle6.uncompyle_file(pycfile, fileobj)
    else:
        if os.path.isdir('../'+source) != True:
            os.mkdir('../'+source)
        with open('../'+source+'/'+source, "w") as fileobj:
            uncompyle6.uncompyle_file(pycfile, fileobj)
    return file


def all_source(fi, source):
    if source == '':
        source = '_source.py'
    files = os.listdir('PYZ-00.pyz_extracted/')
    files = list(set(fi).intersection(files))
    if source == '_source.py':
        if os.path.isdir('../'+file.replace('.exe', '')+source+'/libs') != True:
            os.mkdir('../'+file.replace('.exe', '')+source+'/libs')
        for i in files:
            print('[*] Processing {}'.format(i))
            open('../'+file.replace('.exe', '')+source+'/libs/'+i, 'w').close()
            with open('../'+file.replace('.exe', '')+source+'/libs/'+i, 'r+b') as new:
                new.write(bindata)
                with open('PYZ-00.pyz_extracted/'+i, 'rb') as old:
                    new.write(binascii.unhexlify(binascii.hexlify(old.read())[24:]))
            with open('../'+file.replace('.exe', '')+source+'/libs/'+i.replace('.pyc', '.py'), "w") as fileobj:
                uncompyle6.uncompyle_file('../'+file.replace('.exe', '')+source+'/libs/'+i, fileobj)
            os.remove('../'+file.replace('.exe', '')+source+'/libs/'+i)
            print('[+] Successfully decompiling {}'.format(i))
    else:
        if os.path.isdir('../'+source+'/libs') != True:
            os.mkdir('../'+source+'/libs')
        for i in files:
            print('[*] Processing {}'.format(i))
            open('../'+source+'/libs/'+i, 'w').close()
            with open('../'+source+'/libs/'+i, 'r+b') as new:
                new.write(bindata)
                with open('PYZ-00.pyz_extracted/'+i, 'rb') as old:
                    new.write(binascii.unhexlify(binascii.hexlify(old.read())[24:]))
            with open('../'+source+'/libs/'+i.replace('.pyc', '.py'), "w") as fileobj:
                uncompyle6.uncompyle_file('../'+source+'/libs/'+i, fileobj)
            os.remove('../'+source+'/libs/'+i)
            print('[+] Successfully decompiling {}'.format(i))


if __name__ == '__main__':
    print('''


                ___              
               |__ \             
   _____  _____   ) |_ __  _   _ 
  / _ \ \/ / _ \ / /| '_ \| | | |
 |  __/>  <  __// /_| |_) | |_| |
  \___/_/\_\___|____| .__/ \__, |
                    | |     __/ |
                    |_|    |___/ 

''')
    file = input('[?] Select file -> ')
    source = input('[?] Name of source code file -> ')
    file = main_source(file, source)
    o = input('[*] Now you got main-source file\n[?] Get additional libraries (Y/n) -> ')
    if o == 'Y' or o == 'y':
        if os.listdir('PYZ-00.pyz_extracted/') == []:
            print('[X] No additional libraries found (report me the error in the issues on the GitHub, or write to Telegram: @usbuse)')
        else:
            libs = get_libs(file)
            libs_str = '\n'.join(libs)
            print('[*] Maybe these libraries:\n###################\n'+libs_str+'\n###################')
            fi = input('[?] Select files(,) from '+source_file+'_extracted/PYZ-00.pyz_extracted/ -> ').replace(' ', '').split(',')
            for i in range(0, len(fi)):
                fi[i] = fi[i].replace('.pyc', '')+'.pyc'
            all_source(fi, source)
            input()
    else:
        print('[X] Exit')
        input()
