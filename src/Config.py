#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from src.Operation import OperationType

class Source(object):
  def __init__(self, name: str, path: str, recursively: bool = False) -> None:
    self.name = name
    self.path = path
    self.recursively = recursively

class Destination(object):
  def __init__(self, name: str, path: str) -> None:
    self.name = name
    self.path = path.strip()

class Rule(object):
  def __init__(self, name: str, selector: str, destination: str, subfolder: str = '', operation: OperationType = OperationType.MOVE) -> None:
    self.name = name
    self.selector = selector
    self.destination = destination
    self.subfolder = subfolder
    self.operation = operation

class Config(object):
  def __init__(self) -> None:
    self.createFolders = True
    self.defaultDestination = None
    self.sources = {}
    self.destinations = {}
    self.rules = {}

  def addSource(self, source: Source) -> None:
    self.sources[source.name.lower()] = source

  def addDestination(self, destination: Destination) -> None:
    self.destinations[destination.name.lower()] = destination

  def getDestination(self, name: str) -> Destination:
    return self.destinations.get(name.lower())

  def addRule(self, rule: Rule) -> None:
    self.rules[rule.name.lower()] = rule

  def toJSON(self) -> str:
      return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)