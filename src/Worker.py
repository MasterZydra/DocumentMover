#!/usr/bin/env python
# -*- coding: utf-8 -*-

from array import array
from src.Config import Config, Destination, Rule, Source

import shutil
import re
from os import listdir
from os.path import isfile, join, isdir
from pathlib import Path

class Worker(object):
  def __init__(self, config: Config) -> None:
    self.__config = config
  
  def run(self) -> None:
    for _, source in self.__config.sources.items():
      for file in self.__getFilesInDir(source, source.path):
        for _, rule in self.__config.rules.items():
          self.__processRule(rule, file)

  def __getFilesInDir(self, source: Source, dir: str) -> array:
    # TODO catch FileNotFoundError
    files = []
    for file in listdir(dir):
      path = join(dir, file)
      if source.recursively and isdir(path):
        files += self.__getFilesInDir(source, path)
        continue
      if not isfile(path):
        continue
      files.append([file, dir])
    return files

  def __processRule(self, rule: Rule, file: array):
    if not re.match(rule.selector, file[0], re.IGNORECASE):
      return

    destination: Destination = self.__config.getDestination(rule.destination)

    filePath = join(file[1], file[0])
    destDir = join(destination.path, rule.subfolder)
    destPath = join(destDir, file[0])

    if self.__config.createFolders:
      # Create path if necessary
      Path(destDir).mkdir(parents=True, exist_ok=True)
    else:
      if not isdir(destDir):
        print("Error: The directory '%s' does not exist. Skipping file '%s'."%(destDir, filePath))
        return

    shutil.move(filePath, destPath)
    print("Move file %s to %s"%(filePath, destDir))
