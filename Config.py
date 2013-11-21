import ConfigParser
import os


class Config(object):

    def __init__(self, configfile):
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)
        self._config = ConfigParser.ConfigParser()
        self._config.read(configfile)

    def sectionmap(self, section):
        dict1 = {}
        options = self._config.options(section)
        for option in options:
            try:
                dict1[option] = self._config.get(section, option)
            except:
                dict1[option] = None
        return dict1
