######################################################################################
##                          CCIRCUIT DEBUG IMPROVER                                 ##
##                      Author: Michele Marzulli (emimarz)                          ##
##                      Date: 30/09/2014                                            ##
##                      Version: 1.0                                                ##
######################################################################################
import re
import gdb
import gdb.types
import gdb.printing


import CCPrettyPrinters.CCUtilities

import CCPrettyPrinters.composite.setoftypeIterator

ListWalker = CCPrettyPrinters.composite.setoftypeIterator.ListWalker

###SETOFTYPE PRINTER

class SetOfPrinter(object):
  """Only for a setof or a derived type"""
  
  def __init__(self,value):
    self.value = value
    self.listMember = self.value['m_ItemList']

  def __iter__(self):
    return ListWalker(self.listMember,self.value)

  def to_string(self):
    strings = ["\n"]
    indent = CCPrettyPrinters.CCUtilities.incrementIndentation()
    try:
      k = 0
      strings.append(indent + self.value.type.tag + " SetOf :")
      for setOfElem in self:
        k += 1
        indent2 = CCPrettyPrinters.CCUtilities.incrementIndentation()
        try:
          strings.append("\n" + indent2 + "Element " + str(k) + ":")
          strings.append(str(setOfElem))
        finally:
          CCPrettyPrinters.CCUtilities.decrementIndentation()
    finally:
      CCPrettyPrinters.CCUtilities.decrementIndentation()
    return "".join(strings)

  def display_hint(self):
    return "SetOf Type"

