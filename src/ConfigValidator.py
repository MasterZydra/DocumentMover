#!/usr/bin/env python
# -*- coding: utf-8 -*-

from array import array
import configparser
import re

from src.ConfigReader import ConfigReader

class ConfigValidator(object):
  def __init__(self) -> None:
    self.__configParser = None
    self.__config = None
    self.__errors = []

  def validate(self, configParser: configparser.ConfigParser) -> bool:
    self.__configParser = configParser
    self.__config = None
    self.__errors = []

    result = True
    result &= self.__validateSources()
    result &= self.__validateDestinations()
    # Read the destinations so that in the rules the existence of the destinations can be checked
    self.__config = ConfigReader().readDestinations(self.__configParser)
    result &= self.__validateRules()

    self.__configParser = None
    return result

  def getErrors(self) -> array:
    return self.__errors

  def __validateSources(self) -> bool:
    atLeastOne = False
    sectionsValid = True
    for section in self.__configParser.sections():
      if not self.__match(section, 'source\.'):
        continue
      
      # Check that at least one source entry exists
      if not atLeastOne:
        atLeastOne = True

      # Check if every source has a path
      if not 'path' in self.__configParser[section]:
        self.__errors.append("Error in source '%s': Every source must contain a 'Path'"%(section))
        sectionsValid = False
      
      if 'recursively' in self.__configParser[section]:
        recursively = self.__configParser[section]['recursively'].lower()
        if recursively not in ['yes', 'no']:
          self.__errors.append("Error in source '%s': 'Recursively' must be 'yes' or 'no'"%(section))
          sectionsValid = False

    if not atLeastOne:
      self.__errors.append("Error: It must exist at least one source")
      sectionsValid = False

    return sectionsValid

  def __validateDestinations(self) -> bool:
    atLeastOne = False
    sectionsValid = True
    for section in self.__configParser.sections():
      if not self.__match(section, 'destination\.'):
        continue
      
      # Check that at least one destination entry exists
      if not atLeastOne:
        atLeastOne = True

      # Check if every destination has a path
      if not 'path' in self.__configParser[section]:
        self.__errors.append("Error in destination '%s': Every destination must contain a 'Path'"%(section))
        sectionsValid = False

    if not atLeastOne:
      self.__errors.append("Error: It must exist at least one destination")
      sectionsValid = False

    return sectionsValid

  def __validateRules(self) -> bool:
    atLeastOne = False
    sectionsValid = True
    for section in self.__configParser.sections():
      if not self.__match(section, 'rule\.'):
        continue

      # Check that at least one rule entry exists
      if not atLeastOne:
        atLeastOne = True

      # Check if every rule has a selector
      if not 'selector' in self.__configParser[section]:
        self.__errors.append("Error in rule '%s': Every rule must contain a 'Selector'"%(section))
        sectionsValid = False

      # Check if every rule has a destination
      if not 'destination' in self.__configParser[section]:
        self.__errors.append("Error in rule '%s': Every rule must contain a 'Destination'"%(section))
        sectionsValid = False
      # Check if the destination exists
      else:
        destination = 'Destination.' + self.__configParser[section]['destination']
        if self.__config.getDestination(destination) is None:
          self.__errors.append("Error in rule '%s': The destination '%s' does not exist"%(section, destination))
          sectionsValid = False

    if not atLeastOne:
      self.__errors.append("Error: It must exist at least one rule")
      sectionsValid = False

    return sectionsValid

  def __match(self, section: str, prefix: str) -> bool:
    return re.match(prefix, section, re.IGNORECASE)
