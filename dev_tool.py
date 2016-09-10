import argparse
import sys
import shutil
import os
from subprocess import Popen, PIPE

def generate_pyuic_forms(UI_FORMS_SOURCE, PY_FORMS_DIRECTORY):
    ui_forms_list = os.listdir(UI_FORMS_SOURCE)
    for ui_form in ui_forms_list:
        with Popen(['pyuic5', UI_FORMS_SOURCE + ui_form], 
                    stdout=PIPE, universal_newlines=True) as proc:
            pyuic_form_name = PY_FORMS_DIRECTORY + ui_form[:-3] + '_form.py'
            with open(pyuic_form_name, 'w') as py_form:
                py_form.write(proc.stdout.read())
            print("Successfully generated " + pyuic_form_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Developer tool for contributing Koffeebreak")

    parser.add_argument('--firststart', action="store_true",
                    help='start configuration for contributing')
    parser.add_argument('--updateui', action="store_true",
                    help='Update all .py forms after changing .ui files')
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
    
    if args.updateui:
        UI_FORMS_SOURCE = 'src/ui/forms/'
        PY_FORMS_DIRECTORY = 'koffeebreak/ui/forms/'
        generate_pyuic_forms(UI_FORMS_SOURCE, PY_FORMS_DIRECTORY)
