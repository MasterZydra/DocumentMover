#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.ConfigValidator import ConfigValidator
from src.ConfigReader import ConfigReader
from src.Worker import Worker

import argparse
import os
from os.path import join
import sys
from configparser import ConfigParser

def main() -> int:
    parser = argparse.ArgumentParser(description='DocumentMover is a command line tool that automatically moves files in directories. Rules determine where the files get moved.')
    parser.add_argument('-p', dest='path', type=str, help='path to the folder with config file', default='.')
    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print('Error: "' + args.path + '" is not a valid path')
        return -1

    print('Document Mover')

    configParser = ConfigParser()
    if not os.path.isfile(join(args.path, '.documentMover')):
      print('Error: No configuration file ".documentMover" found in the given path')
      return -1

    configParser.read(join(args.path, '.documentMover'))

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