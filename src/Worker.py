#!/usr/bin/env python
# -*- coding: utf-8 -*-

from array import array
from datetime import datetime
from src.Operation import OperationType
from src.Config import Config, Destination, Rule, Source

import shutil
import re
import os
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
    for file in os.listdir(dir):
      path = join(dir, file)
      if source.recursively and isdir(path):
        files += self.__getFilesInDir(source, path)
        continue
      if not isfile(path):
        continue
      files.append([file, dir])
    return files

  def __processRule(self, rule: Rule, file: array) -> None:
    if not re.match(rule.selector, file[0], re.IGNORECASE):
      return

    destination: Destination = self.__config.getDestination(rule.destination)

    filePath = join(file[1], file[0])
    subfolder = self.__replaceVariables(rule.subfolder)
    destDir = join(destination.path, subfolder)
    destPath = join(destDir, file[0])

    self.__executeOperation(rule, filePath, destPath, destDir)

  def __executeOperation(self, rule: Rule, filePath: str, destPath: str, destDir: str) -> None:
    if rule.operation == OperationType.MOVE or rule.operation == OperationType.COPY:
        if self.__config.createFolders:
          # Create path if necessary
          Path(destDir).mkdir(parents=True, exist_ok=True)
        else:
          if not isdir(destDir):
            print("Error: The directory '%s' does not exist. Skipping file '%s'."%(destDir, filePath))
            return

    match rule.operation:
      case OperationType.MOVE:
        shutil.move(filePath, destPath)
        print("Moved file\n   %s\nto %s"%(filePath, destDir))
        return

      case OperationType.DELETE:
        os.remove(filePath)
        print("Deleted file %s"%(filePath))
        return 

      case OperationType.COPY:
        shutil.copy(filePath, destPath)
        print("Copied file\n   %s\nto %s"%(filePath, destDir))
        return

  def __replaceVariables(self, path: str) -> str:
    if "{day}" in path:
      path = path.replace("{day}", str(datetime.now().day))
    if "{month}" in path:
      path = path.replace("{month}", str(datetime.now().month))
    if "{year}" in path:
      path = path.replace("{year}", str(datetime.now().year))
    return path
