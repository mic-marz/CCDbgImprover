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

import CCPrettyPrinters.composite.settypeIterator

SetWalker = CCPrettyPrinters.composite.settypeIterator.SetWalker 

###SETTYPE PRINTER

class SetPrinter(object):
  """Only for a set or a derived type"""

  def __init__(self,value):
    self.value = value

    self.descriptions = []
    self.getDescriptions()

  def __iter__(self):
    return SetWalker(self)

  def fieldToString(self,fieldIdx):
    k = 0
    while True:
      if self.descriptions[k]['index'] == fieldIdx:
        aux = CCPrettyPrinters.CCUtilities.fromCPointerToStringWithoutQuotes(self.descriptions[k]['pszName'])
        fieldName = "m_" + aux
        return fieldName
      k += 1

  #fieldIndex refers to index in "<type>_Descs" (which is an array of FieldDescriptor structures)
  def fieldToValue(self,fieldIndex):
    fieldName = self.fieldToString(fieldIndex)
    return str(self.value[fieldName])

  def printField(self,fieldIdx):
    fieldPrint = []
    indent2 = CCPrettyPrinters.CCUtilities.incrementIndentation()
    try:
      fieldName = self.fieldToString(fieldIdx)
      fieldPrint.append("\n" + indent2 + "\"" + fieldName + "\"")
      fieldPrint.append(" :")
      fieldPrint.append(str(self.value[fieldName])) 
    finally:
      CCPrettyPrinters.CCUtilities.decrementIndentation()
    return " ".join(fieldPrint)

  def getDescriptions(self):
    descriptions = self.value['m_Descriptors']
    if descriptions is None:
      raise ValueError("Access error in \'m_Descriptors\' member")
    if descriptions.type.code != gdb.TYPE_CODE_PTR:
      raise TypeError("Error in \'m_Descriptors\' member type")
    self.descriptions = descriptions

  def to_string(self):
    strings = ["\n"]
    indent = CCPrettyPrinters.CCUtilities.incrementIndentation()
    try:
      strings.append(indent + "Set Type: ")
      #loop that cycles over every set field 
      for f in self:
        strings.append(self.printField(f))
    finally:
      CCPrettyPrinters.CCUtilities.decrementIndentation()
    return "".join(strings)

  def display_hint(self):
    return "Set Type"

