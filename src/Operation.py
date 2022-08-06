#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.ExtendedEnum import ExtendedEnum

class OperationType(ExtendedEnum):
  MOVE = 'move'
  DELETE = 'delete'
  COPY = 'copy'

  @staticmethod
  def fromStr(label: str):
    try:
      return OperationType[label.upper()]
    except KeyError as e:
      raise e
  
  @staticmethod
  def toStringList() -> str:
    return "'%s' or '%s'"%("', '".join(OperationType.list()[:-1]),  OperationType.list()[-1])