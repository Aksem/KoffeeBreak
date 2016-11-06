"""
Usage:
--------------------------------------------------------------------------
 to build package:       python3 setup.py build
 to install package:     python3 setup.py install
 to remove installation: python3 setup.py uninstall
--------------------------------------------------------------------------
 to create source distribution:   python3 setup.py sdist
--------------------------------------------------------------------------
 to create binary RPM distribution:  python3 setup.py bdist_rpm
--------------------------------------------------------------------------.
 Help on available distribution formats: --help-formats
"""

import os, sys

# Get packages
def is_package(directory):
    if os.path.isdir(directory):
        marker = os.path.join(directory, '__init__.py')
        if os.path.isfile(marker):
            return True
    return False

def get_packages(path = os.path.dirname(os.path.abspath(__file__))):
    packages = []
    items = []
    print()
    if os.path.isdir(path):
        if is_package(path):
            packages.append(path)
        try:
            items = os.listdir(path)
        except:
            pass
        for item in items:
            directory = os.path.join(path, item)
            if os.path.isdir(directory):
                packages += get_packages(directory)
    packages.sort()
    return packages

def create_package_list(path = os.path.dirname(os.path.abspath(__file__)), excludes=[]):
    pkgs = []
    for item in get_packages(path):
        res = item.replace('/', '.')
        check = True
        for exclude in excludes:
            if len(res) >= len(exclude) and res[:len(exclude)] == exclude:
                check = False
                break
        if check:
            pkgs.append(res)
    return pkgs

# create list of data files
def get_data_files(copy_to = None, copy_from = None):
    if not copy_from or not copy_to or not os.path.isdir(copy_to):
        print('Incorrect path for data file.')
        return []
    res = []
    if os.path.isdir(copy_from):
        items = os.listdir(copy_from)
        lis = []
        for item in items:
            lis.append(os.path.join(copy_from, item))
        tup = copy_to, lis
        res.append(tup)
    elif os.path.isfile(copy_from):
        tup = copy_to, [copy_from]
        res.append(tup)
    return res

INSTALL_PATH = '/usr/share/koffeebreak'
_scripts = ['src/scripts/koffeebreak']

_copy_desktop = get_data_files(copy_to = '/usr/share/applications', copy_from ='koffeebreak.desktop')
_copy_icons = get_data_files(copy_to = '/usr/share/icons/hicolor/scalable/apps', copy_from = 'src/ui/img/icons')

_data_files = _copy_desktop + _copy_icons

if len(sys.argv) == 1:
    print ('Please specify build options!')
    print (__doc__)
    sys.exit(0)

if len(sys.argv) > 1:
    if sys.argv[1] == 'uninstall':
        if os.path.isdir(INSTALL_PATH):
            print ('REMOVE: ' + INSTALL_PATH)
            os.system('rm -rf ' + INSTALL_PATH)
            for item in _scripts:
                filename = os.path.basename(item)
                print ('REMOVE: /usr/bin/' + filename)
                os.system('rm -rf /usr/bin/' + filename)
            for item in _data_files:
                location = item[0]
                file_list = item[1]
                for file_item in file_list:
                    filename = os.path.basename(file_item)
                    filepath = os.path.join(location, filename)
                    print ('REMOVE: ' + filepath)
                    os.system('rm -rf ' + filepath)
            print ('Desktop database update: ')
            os.system('update-desktop-database')
            print ('DONE!')
        else:
            print ('KoffeeBreak installation is not found!')
        sys.exit(0)

from distutils.core import setup

setup (name = 'koffeebreak',
        version = '0.1',
        author = 'Yuri Fabirovsky, Vladyslav Hnatiuk',
        author_email = 'fabirovskij@open365.com, vladyslav5@meta.ua',
        url = 'https://github.com/Aksem/KoffeeBreak',
        download_url = 'https://github.com/Aksem/KoffeeBreak',
        description = 'New powerful KDE application for keeping breaks!',
        long_description = '',
        license = 'GNU-2.0',
        keywords = 'break keep coffee koffee',
        packages = create_package_list('koffeebreak'),
        package_data = {
            'koffeebreak': ['*.py', '*.ini'],
            'koffeebreak.ui': ['*.py', 'forms/*.py']
        },
        data_files = _data_files,
        scripts = _scripts,
        classifiers = [
            'Development Status :: 5 - Production/Stable',
            'Environment :: Desktop',
            'Environment :: MacOS X',
            'Environment :: Win32 (MS Windows)',
            'Environment :: X11 Applications',
            'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
            'Operating System :: POSIX',
            'Operating System :: MacOS',
            'Operating System :: Microsoft :: Windows',
            'Programming Language :: Python :: 3',
            'Topic :: Utilities',
        ],
    )
