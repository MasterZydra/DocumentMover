#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
import re

from src.Config import Config, Rule, Source, Destination

class ConfigReader(object):
  def read(self, configParser: configparser.ConfigParser) -> Config:
    self.__config = Config()
    self.__configParser = configParser
    
    self.__readSources()
    self.__readDestinations()
    self.__readRules()

    self.__configParser = None
    return self.__config

  def __readSources(self) -> None:
    for section in self.__configParser.sections():
      if not self.__match(section, 'source\.'):
        continue

      path = self.__configParser[section]['path']

      recursively = False
      if 'recursively' in self.__configParser[section]:
        recursivelyStr = self.__configParser[section]['recursively'].lower()
        recursively = recursivelyStr == 'yes'

      source = Source(section, path, recursively)
      self.__config.addSource(source)

  def __readDestinations(self) -> None:
    for section in self.__configParser.sections():
      if not self.__match(section, 'destination\.'):
        continue
      
      destination = Destination(section, self.__configParser[section]['path'])
      self.__config.addDestination(destination)

  def __readRules(self) -> bool:
    for section in self.__configParser.sections():
      if not self.__match(section, 'rule\.'):
        continue

      rule = Rule(section, self.__configParser[section]['selector'])
      self.__config.addRule(rule)

  def __match(self, section: str, pattern: str) -> bool:
    return re.match(pattern, section, re.IGNORECASE)
