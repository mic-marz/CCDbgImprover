######################################################################################
##                          CCIRCUIT DEBUG IMPROVER                                 ##
##                      Author: Michele Marzulli (emimarz)                          ##
##                      Date: 30/09/2014                                            ##
##                      Version: 1.0                                                ##
######################################################################################
import gdb
import gdb.types
import gdb.printing

import CCPrettyPrinters.CCUtilities

#The wrapper is useful for name attribute
class ReferencePrinterWrapper(object):

  def __init__(self,name):
    self.enabled = True
    self.name = name

  def __call__(self,value):
    if value.type.code == gdb.TYPE_CODE_REF:
      return ReferencePrinter(value)
    return None

class ReferencePrinter(object):
  def __init__(self,value):
    self.value = value
    self.dereferencedValue = self.value.referenced_value()

  def to_string(self):
    strings = ["\n"]
    indent = CCPrettyPrinters.CCUtilities.incrementIndentation()
    try:
      strings.append(indent)
      strings.append("Reference object: dereferenced object: ")
      strings.append(str(self.dereferencedValue))
    finally:
      CCPrettyPrinters.CCUtilities.decrementIndentation()
    return "".join(strings)
