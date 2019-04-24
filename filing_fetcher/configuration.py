# -*- coding: utf-8 -*-
"""
Provides configuration for the project.

Defaults are defined in the `Config` class definition.
They are overridden by values in ~/config/filing_fetcher_config.yml.

Warning:
    Modifying config values is not prevented.
    Config is implemented as a singleton, so any modification will
    be visible anywhere else the configuration is used.

Usage:
    ``
    config = configuration.get_config()
    config.CONFIG_NAME
    ``

@author: Philip Lee
"""
import logging
import os
from abc import ABCMeta, abstractmethod
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)

CONFIG_FILEPATH = str(Path.home().joinpath('config').joinpath('filing_fetcher_config.yml'))


class Singleton(type):

    def __init__(cls, *args, **kwargs):
        cls.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):

        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
            return cls.__instance
        else:
            return cls.__instance


class ConfigProvider(metaclass=ABCMeta):

    source_name = 'Unnamed Source'

    @abstractmethod
    def fetch_config(self):
        raise NotImplementedError('ConfigProviders must implement fetch_config')


class YamlConfigProvider(ConfigProvider):

    def __init__(self, filepath):
        self.filepath = filepath
        self.source_name = f'Yaml file: {filepath}'

    def fetch_config(self):

        if os.path.isfile(self.filepath):

            logger.info(f'Reading config from {self.filepath}')
            print('Reading config from', self.filepath)
            with open(self.filepath, 'rb') as f:
                yaml_conf = yaml.load(f)

            return yaml_conf.items()

        else:
            logger.info(f'Config file: {self.filepath} does not exist.')
            return list()


# Private method from enum
def _is_dunder(name):
    """Returns True if a __dunder__ name, False otherwise."""
    return (name[:2] == name[-2:] == '__' and
            name[2:3] != '_' and
            name[-3:-2] != '_' and
            len(name) > 4)


# Private method from enum
def _is_sunder(name):
    """Returns True if a _sunder_ name, False otherwise."""
    return (name[0] == name[-1] == '_' and
            name[1:2] != '_' and
            name[-2:-1] != '_' and
            len(name) > 2)


def _is_under(name):
    return _is_sunder(name) or _is_dunder(name)


class Config(metaclass=Singleton):
    """Defines the configuration names and defaults for the project."""

    config_provider = YamlConfigProvider(filepath=CONFIG_FILEPATH)

    def __init__(self):

        self.BASIC_COMPANY_INFO_FILEPATH = None
        self.LOG_DIR = str(Path.home().joinpath('logs'))

        for key, value in Config.config_provider.fetch_config():

            if key in self.__dict__ and not _is_under(key):
                logger.info(f'Overriding default value of {key} with value from {Config.config_provider.source_name}')
                self.__dict__[key] = value


def get_config():
    return Config()


if __name__ == '__main__':

    log_format = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s'
    logging.basicConfig(format=log_format)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    logger.info('test')

    config = get_config()

    print(f'BASIC_COMPANY_INFO_FILEPATH: {config.BASIC_COMPANY_INFO_FILEPATH}')
