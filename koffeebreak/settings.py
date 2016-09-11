from configparser import ConfigParser

def read():
    #add checking for existing file and if it is true.
    settings = ConfigParser()
    settings.read('settings.ini')
    for time_item in settings['TIME']:
        settings['TIME'][time_item] = str(int(settings['TIME'][time_item]) * 60)
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

def set_default(settings=None):
    #try to remove?
    settings['TIME'] = {'short_break': 5,
                        'long_break': 10,
                        'work_time': 25,
                        'shorts_before_long': 3}
    settings['EXECUTION'] = {'gui': 'qt',
                             'state': 'work-full'}
    write(settings)
    
def update(new_settings):
    settings = new_settings
    write(settings)

def write(settings):
    with open('settings.ini', 'w') as configfile:
        settings.write(configfile)
