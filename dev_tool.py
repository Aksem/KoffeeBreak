import argparse
import sys
import shutil
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Developer tool for contributing Koffeebreak")

    parser.add_argument('--firststart', action="store_true",
                    help='start configuration for contributing')
    args = parser.parse_args()
    
    if args.firststart:
        if sys.platform.startswith('linux'):
            icons_directory = os.getenv('HOME') + '/.local/share/icons/hicolor/scalable/apps'
            ICON_SOURCE = 'src/ui/img/icons/'
            if not os.path.exists(icons_directory):
                os.makedirs(icons_directory)
            icons_list = os.listdir(ICON_SOURCE)
            for icon in icons_list:
                shutil.copyfile(ICON_SOURCE + icon, icons_directory + '/' + icon)
    
