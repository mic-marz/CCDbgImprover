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

###MSG
class MsgPrinter(object):
  """Only for a msg or a derived type"""

  def __init__(self,value):
    self.value = value
    self.name = CCPrettyPrinters.CCUtilities.fromCPointerToString(self.value['m_pszMessageString'])
    obj = self.value['m_pSyntax']
    if obj.type.code != gdb.TYPE_CODE_PTR:
      raise TypeError("Error in m_pSyntax type")
    obj = obj.dereference()
    self.objType = gdb.lookup_type(str.replace(self.value.type.tag,"Msg",""))
    self.obj = obj.cast(self.objType)

  def to_string(self):
    strings = ["\n"]
    indent = CCPrettyPrinters.CCUtilities.incrementIndentation()
    try:
      strings.append(indent)
      strings.append("Msg " + self.name + " : ")
      strings.append("syntax object ")
      strings.append("(" + self.objType.tag + ") :")
      strings.append(self.printObject())
    finally:
      CCPrettyPrinters.CCUtilities.decrementIndentation()
    return "".join(strings)

  def printObject(self):
    return str(self.obj)

  def display_hint(self):
    return "Msg Type"


