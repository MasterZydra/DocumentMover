#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
import re

from src.Config import Config, Source, Destination

class ConfigReader(object):
  def read(self, configParser: configparser.ConfigParser) -> Config:
    self.__config = Config()
    self.__configParser = configParser
    
    self.__readSources()
    self.__readDestinations()

    self.__configParser = None
    return self.__config

  def __readSources(self) -> None:
    for section in self.__configParser.sections():
      if not self.__sectionExists(section, 'source.'):
        continue
      
      source = Source(section, self.__configParser[section]['path'])
      self.__config.addSource(source)

  def __readDestinations(self) -> None:
    for section in self.__configParser.sections():
      if not self.__sectionExists(section, 'destination.'):
        continue
      
      destination = Destination(section, self.__configParser[section]['path'])
      self.__config.addDestination(destination)

  def __sectionExists(self, section: str, prefix: str) -> bool:
    return re.match(prefix, section, re.IGNORECASE)
