#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum

class ExtendedEnum(Enum):
  @classmethod
  def list(cls):
    return list(map(lambda c: c.value, cls))
