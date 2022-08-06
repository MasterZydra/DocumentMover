#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.ConfigValidator import ConfigValidator
from src.ConfigReader import ConfigReader
from src.Worker import Worker

import argparse
import os
from os.path import join
import sys
from configparser import ConfigParser, DuplicateSectionError

VERSION='v0.1.0'

def main() -> int:
    parser = argparse.ArgumentParser(description='DocumentMover is a command line tool that automatically moves files in directories. Rules determine where the files get moved.')
    parser.add_argument('-val', dest='validate', help='only validate the config file without executing it', action='store_true')
    parser.add_argument('--version', dest='version', help='show the version of the program', action='store_true')
    parser.add_argument('-p', dest='path', type=str, help='path to the folder with config file', default='.')
    args = parser.parse_args()

    if args.version:
      showVersion()
      return 0

    if not os.path.isdir(args.path):
        print('Error: "' + args.path + '" is not a valid path')
        return -1

    configParser = ConfigParser()
    if not os.path.isfile(join(args.path, '.documentMover')):
      print('Error: No configuration file ".documentMover" found in the given path')
      return -1

    try:
      configParser.read(join(args.path, '.documentMover'))
    except DuplicateSectionError as e:
      print('Error:', e.message)
      return -1

    if not validate(configParser, args.validate):
      return -1
    
    if args.validate:
      return 0
    
    configReader = ConfigReader()
    config = configReader.read(configParser)

    worker = Worker(config)
    worker.run()

    return 0

def validate(configParser: ConfigParser, validateOnly: bool) -> bool:
    configValidator = ConfigValidator(validateOnly)
    isValid = configValidator.validate(configParser)

    if validateOnly and isValid and len(configValidator.getErrors()) > 0:
      for error in configValidator.getErrors():
        print(error)

    if isValid:
      return True

    print('The config is invalid!')
    for error in configValidator.getErrors():
      print(error)
    return False

def showVersion() -> None:
  print('DocumentMover version', VERSION)

if __name__ == '__main__':
    sys.exit(main())