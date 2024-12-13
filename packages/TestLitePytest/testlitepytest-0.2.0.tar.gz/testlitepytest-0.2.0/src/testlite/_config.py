import os
import configparser


class SingletonMetaClass(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class CONFIG:
    __metaclass__ = SingletonMetaClass

    _REPORTSDIRNAME = 'TestLiteReports'
    _DELETEREPORTSDIR = True
    _REPORTSSAVETYPE = 'BINARY'
    _TESTLITEURL = 'http://127.0.0.1:8000'

    def __init__(self):
        self.config = configparser.ConfigParser()
        if os.path.exists('TestLiteConfig.ini'):
            self.have_config_file = True
            self.config.read('TestLiteConfig.ini')
        else:
            self.have_config_file = False
 
    @property
    def TESTLITEURL(self):
        config_value = self.config.get('TestLiteConfig', 'TESTLITEURL', fallback=None)
        if config_value is not None:
            return config_value
        else:
            return self._TESTLITEURL
        
    @property
    def DELETEREPORTSDIR(self):
        config_value = self.config.get('TestLiteConfig', 'DELETEREPORTSDIR', fallback=None)
        if config_value is not None:
            return config_value
        else:
            return self._DELETEREPORTSDIR
        
    @property
    def REPORTSDIRNAME(self):
        config_value = self.config.get('TestLiteConfig', 'REPORTSDIRNAME', fallback=None)
        if config_value is not None:
            return config_value
        else:
            return self._REPORTSDIRNAME
        
    @property
    def REPORTSSAVETYPE(self):
        config_value = self.config.get('TestLiteConfig', 'REPORTSSAVETYPE', fallback=None)
        if config_value is not None:
            return config_value
        else:
            return self._REPORTSSAVETYPE