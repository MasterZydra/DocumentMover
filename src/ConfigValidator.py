#!/usr/bin/env python
# -*- coding: utf-8 -*-

from array import array
import configparser
import re

class ConfigValidator(object):
  def __init__(self) -> None:
    self.__configParser = None
    self.__errors = []

  def validate(self, configParser: configparser.ConfigParser) -> bool:
    self.__configParser = configParser
    self.__errors = []
    result = True
    result &= self.__validateSources()
    result &= self.__validateDestinations()
    self.__configParser = None
    return result

  def getErrors(self) -> array:
    return self.__errors

  def __validateSources(self) -> bool:
    atLeastOneSource = False
    sectionsValid = True
    for section in self.__configParser.sections():
      if not self.__sectionExists(section, 'source.'):
        continue
      
      # Check that at least one source entry exists
      if not atLeastOneSource:
        atLeastOneSource = True

      # Check if every source has a path
      if not 'path' in self.__configParser[section]:
        self.__errors.append("Error in source '%s': Every source must contain a 'Path'"%(section))
        sectionsValid = False

      if 'recursively' in self.__configParser[section]:
        recursively = self.__configParser[section]['recursively'].lower()
        if recursively not in ['yes', 'no']:
          self.__errors.append("Error in source '%s': 'Recursively' must be 'yes' or 'no'"%(section))
          sectionsValid = False

    if not atLeastOneSource:
      self.__errors.append("Error: It must exist at least one source")

    return atLeastOneSource & sectionsValid

  def __validateDestinations(self) -> bool:
    atLeastOneSource = False
    sectionsValid = True
    for section in self.__configParser.sections():
      if not self.__sectionExists(section, 'destination.'):
        continue
      
      # Check that at least one source entry exists
      if not atLeastOneSource:
        atLeastOneSource = True

      # Check if every destination has a path
      if not 'path' in self.__configParser[section]:
        self.__errors.append("Error in destination '%s': Every destination must contain a 'Path'"%(section))
        sectionsValid = False

    if not atLeastOneSource:
      self.__errors.append("Error: It must exist at least one destination")

    return atLeastOneSource & sectionsValid

  def __sectionExists(self, section: str, prefix: str) -> bool:
    return re.match(prefix, section, re.IGNORECASE)
