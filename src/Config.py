#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

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
  def __init__(self, name: str, selector: str) -> None:
    self.name = name
    self.selector = selector

class Config(object):
  def __init__(self) -> None:
    self.sources = {}
    self.destinations = {}
    self.rules = {}

  def addSource(self, source: Source) -> None:
    self.sources[source.name] = source

  def addDestination(self, destination: Destination) -> None:
    self.destinations[destination.name] = destination
  
  def addRule(self, rule: Rule) -> None:
    self.rules[rule.name] = rule

  def toJSON(self) -> str:
      return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)