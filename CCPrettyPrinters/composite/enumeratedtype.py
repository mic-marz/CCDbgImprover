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


###ENUMTYPE PRINTER
class EnumPrinter(object):
  """Only for an enumerated or a derived type"""

  def __init__(self,value):
    self.value = value
    self.enumValue = self.value['m_Value']

  def enumString(self):
    members = gdb.parse_and_eval(self.value.type.tag + "_Members")
    if members.type.code != gdb.TYPE_CODE_ARRAY:
      raise TypeError("Error in EnumMembers type")
    index = 0
    while True:
      if members[index]['value'] == self.enumValue:
        return CCPrettyPrinters.CCUtilities.fromCPointerToStringWithoutQuotes(members[index]['pszName'])
      index += 1  

  def to_string(self):
    strings = ["\n"]
    indent = CCPrettyPrinters.CCUtilities.incrementIndentation()
    try:
      strings.append(indent)
      strings.append("Enum Value: ")
      strings.append(self.enumString())
      strings.append(" (");
      strings.append(str(self.enumValue))
      strings.append(") ")
    finally:
      CCPrettyPrinters.CCUtilities.decrementIndentation()
    return "".join(strings)

  def display_hint(self):
    return "Enumerated Type"

