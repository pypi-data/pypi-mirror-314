import os

import yaml

from fild.process.dictionary import merge_with_updates


class ConfigSection:
    def __init__(self, key, section_value, parent):
        object.__setattr__(self, 'parent', parent)
        object.__setattr__(self, 'key', key)
        object.__setattr__(self, 'initial_dict', section_value)

    def __getattr__(self, item):
        value = self.initial_dict[item]

        is_section = isinstance(value, dict)
        is_section_list = isinstance(value, list)

        if is_section or is_section_list:
            value = ConfigSection(item, value, self)

        return value

    def set_value(self, key, value):
        if isinstance(self.parent, ConfigFile):
            self.parent.initial_dict = merge_with_updates(
                self.parent.initial_dict, {self.key: {key: value}},
                extend_only=True
            )
        elif isinstance(self.parent, ConfigSection):
            self.parent.set_value(self.key, {key: value})

    def __setattr__(self, key, value):
        if key not in self.__dict__:
            self.set_value(key, value)

    def get(self, key, default=None):
        if key not in self.initial_dict:
            return default

        return getattr(self, key)

    def keys(self):
        return self.initial_dict.keys()

    def items(self):
        return self.initial_dict.items()

    def values(self):
        return self.initial_dict.values()

    def __getitem__(self, item):
        return self.__getattr__(item)  # FIXME payload only?

    def __setitem__(self, key, value):
        return self.__setattr__(key, value)

    def __len__(self):
        return len(self.initial_dict)

    def __contains__(self, item):
        return item in self.initial_dict

    def __str__(self):
        return str(self.initial_dict)


class ConfigFile(type):
    def __getattr__(cls, key):
        if cls.initial_dict is None:
            cls.initialize()

        value = cls.initial_dict[key]

        if isinstance(value, dict):
            value = ConfigSection(key, value, cls)

        return value

    def __getitem__(cls, item):
        return cls.__getattr__(item)  # pylint: disable=no-value-for-parameter

    def __contains__(cls, item):
        if cls.initial_dict is None:
            cls.initialize()

        return item in cls.initial_dict


class Cfg(metaclass=ConfigFile):  # pylint: disable=too-few-public-methods
    initial_dict = None

    @staticmethod
    def initialize(config_file=None, local_config=None):

        config_file = config_file or f'{os.getcwd()}/etc/config.yaml'

        with open(config_file, 'r', encoding='utf-8') as config_yaml:
            Cfg.initial_dict = yaml.load(config_yaml, Loader=yaml.FullLoader)

        local_config = local_config or f'{os.getcwd()}/etc/local.yaml'

        if os.path.exists(local_config):
            with open(local_config, 'r', encoding='utf-8') as local_yaml:
                Cfg.initial_dict = merge_with_updates(
                    Cfg.initial_dict,
                    yaml.load(local_yaml, Loader=yaml.FullLoader)
                )
