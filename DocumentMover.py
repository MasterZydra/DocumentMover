#!/usr/bin/env python
# -*- coding: utf-8 -*-

from calendar import c
from src.ConfigValidator import ConfigValidator
from src.ConfigReader import ConfigReader
from src.Worker import Worker

import sys
from configparser import ConfigParser

def main() -> int:
    print('Document Mover')

    configParser = ConfigParser()
    configParser.read('./.documentMover')

    if not validate(configParser):
      return -1

    configReader = ConfigReader()
    config = configReader.read(configParser)

    worker = Worker(config)
    worker.run()

    return 0

def validate(configParser: ConfigParser) -> bool:
    configValidator = ConfigValidator()
    isValid = configValidator.validate(configParser)

    if isValid:
      return True

    print('The config is invalid!')
    for error in configValidator.getErrors():
      print(error)
    return False


if __name__ == '__main__':
    sys.exit(main())