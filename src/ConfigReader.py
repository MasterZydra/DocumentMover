#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
import re

from src.Config import Config, Rule, Source, Destination
from src.Operation import OperationType

class ConfigReader(object):
  def read(self, configParser: configparser.ConfigParser) -> Config:
    self.__config = Config()
    self.__configParser = configParser
    
    self.__readCommon()
    self.__readDestinations()
    self.__readSources()
    self.__readRules()

    self.__configParser = None
    return self.__config

  def readDestinations(self, configParser: configparser.ConfigParser) -> Config:
    self.__config = Config()
    self.__configParser = configParser
    
    self.__readDestinations()

    self.__configParser = None
    return self.__config

  def __readCommon(self) -> None:
    for section in self.__configParser.sections():
      if not self.__match(section, '^common$'):
        continue

      if 'createFolders' in self.__configParser[section]:
        createFoldersStr = self.__configParser[section]['createFolders'].lower()
        self.__config.createFolders = createFoldersStr == 'yes'

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

      selector = self.__configParser[section]['selector']
      destination = 'Destination.' + self.__configParser[section]['destination']
      # Subfolder
      subfolder = ''
      if 'subfolder' in self.__configParser[section]:
        subfolder = self.__configParser[section]['subfolder']
      # Operation
      operation = OperationType.MOVE
      if 'operation' in self.__configParser[section]:
          operation = OperationType.fromStr(self.__configParser[section]['operation'])

      rule = Rule(section, selector, destination, subfolder, operation)
      self.__config.addRule(rule)

  def __match(self, section: str, pattern: str) -> bool:
    return re.match(pattern, section, re.IGNORECASE)
