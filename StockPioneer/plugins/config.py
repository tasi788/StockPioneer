from configparser import ConfigParser

configure = ConfigParser()
configure.read('config.ini')


def get(key, value):
    """
    get string from config.ini
    """
    return configure.get(key, value)


def getint(key, value):
    """
    get int from config.ini
    """
    return configure.getint(key, value)
