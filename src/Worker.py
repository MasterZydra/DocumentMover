#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.Config import Config

from os import listdir
from os.path import isfile, join

class Worker(object):
  def __init__(self, config: Config) -> None:
    self.__config = config
  
  def run(self) -> None:
    print('Worker run')
    for _, source in self.__config.sources.items():
      print('->', source.path)
      self.getFilesInDir(source.path)
    # source = self.__config.sources[self.__config.sources.keys()[0]]
    # print(source.path)

  def getFilesInDir(self, dir: str) -> None:
    # TODO catch FileNotFoundError
    for file in listdir(dir):
      if not isfile(join(dir, file)):
        continue
      print(file)
