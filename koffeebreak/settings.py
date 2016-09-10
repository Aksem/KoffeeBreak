from configparser import ConfigParser

def read():
    #add checking for existing file and if it is true.
    settings = ConfigParser()
    settings.read('settings.ini')
    for time_item in settings['TIME']:
        settings['TIME'][time_item] = str(int(settings['TIME'][time_item]) * 60)
    return settings

def set_default(settings=None):
    #try to remove?
    settings['TIME'] = {'short_break': 5,
                        'long_break': 10,
                        'short_work': 25,
                        'shorts_before_long': 3}
    write(settings)
    
def update(new_settings):
    settings = new_settings
    write(settings)

def write(settings):
    with open('settings.ini', 'w') as configfile:
        settings.write(configfile)
