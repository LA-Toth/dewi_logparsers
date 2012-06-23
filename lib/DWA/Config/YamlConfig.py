# vim: sts=4 ts=8 et ai

import yaml
import os

class YamlConfig(object):
    def __init__(self):
        self.__config_file = None
        self.clear()
        self.root_node = 'dwa'

    def open(self, cfgfile):
        self.__config_file = cfgfile
        if os.path.exists(self.__config_file):
            with open(self.__config_file, 'r') as file:
                self.config = yaml.load(file)
        else:
            self.clear()

    def write(self):
        with open(self.__config_file, 'w') as file:
            yaml.dump(self.config, file)

    def close(self):
        self.__config_file = None
        self.config = None

    def set_config(self, config):
        self.config = config

    def get_config(self):
        return self.config

    def clear(self):
        self.config = dict()


    def get_program_config(self, path):
        return self.get(self.root_node + '.' + path)

    def set_program_config(self, path, value):
        return self.set(self.root_node + path, value)

    def get(self, path):
        parts = path.split('.')
        for x in parts:
            if not x: del x

        current = self.config
        for part in parts:
            try:
                current = current[part]
            except KeyError:
                return None

        return current

    def set(self, path, value):
        parts = path.split('.')
        for x in parts:
            if not x: del x

        current = self.config
        last_part = None
        last_current = None
        for part in parts:
            last_part = part
            last_current = current
            try:
                current = current[part]
            except KeyError:
                current[part] = dict()
                current = current[part]

        if last_part:
            last_current[last_part] = value
        else:
            self.config = value