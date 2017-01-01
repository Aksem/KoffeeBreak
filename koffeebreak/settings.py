from configparser import ConfigParser
import os
import sys

def get_config_dir(appname=None):
    system = sys.platform
    if system.startswith("win32"):
        pass
    if system.startswith("darwin"):
        pass
    else:
        path = os.getenv('XDG_CONFIG_HOME', os.path.expanduser("~/.config"))
        if appname:
            path = os.path.join(path, appname)
    return path

def read():
    #add checking for existing file and if it is true.
    config_file = os.path.join(get_config_dir('KoffeeBreak'), 'settings.ini')
    if not os.path.exists(config_file):
        set_default()
    settings = ConfigParser()
    settings.read(config_file)
    for item in settings['TIME']:
        settings['TIME'][item] = str(int(settings['TIME'][item]) * 60)
    return settings

def read_parameter(config, parameter, p_type="str"):
    if p_type == "str":
        p_value = config[parameter[0]][parameter[1]]
    elif p_type == "int":
        p_value = int(config[parameter[0]][parameter[1]])
    elif p_type == "bool":
        p_value = bool(config[parameter[0]][parameter[1]])
    else:
        p_value = None
    return p_value

def set_default():
    #try to remove?
    settings = ConfigParser()
    settings['TIME'] = {'work_time': 25,
                        'time_of_short_break': 5,
                        'time_of_long_break': 10,
                        'work_time_when_postpone_break': 5 }
    settings['BREAKS'] = {'number_of_short_breaks': 3}
    settings['EXECUTION'] = {'gui': 'qt',
                             'state': 'work-full'}
    write(settings)

def update(new_settings):
    settings = new_settings
    write(settings)

def write(settings):
    config_file = os.path.join(get_config_dir('KoffeeBreak'), 'settings.ini')
    if not os.path.exists(os.path.dirname(config_file)):
        os.makedirs(os.path.dirname(config_file))
    with open(config_file, 'w') as configfile:
        settings.write(configfile)
