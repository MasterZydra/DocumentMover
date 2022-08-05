#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

class Source(object):
  def __init__(self, name: str, path: str) -> None:
    self.name = name
    self.path = path.strip()

class Destination(object):
  def __init__(self, name: str, path: str) -> None:
    self.name = name
    self.path = path.strip()

class Config(object):
  def __init__(self) -> None:
    self.sources = {}
    self.destinations = {}

  def addSource(self, source: Source) -> None:
    self.sources[source.name] = source

  def addDestination(self, destination: Destination) -> None:
    self.destinations[destination.name] = destination

  def toJSON(self):
      return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)