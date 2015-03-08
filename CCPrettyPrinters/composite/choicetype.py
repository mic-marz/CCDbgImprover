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


###CHOICETYPE PRINTER
class ChoicePrinter(object):
  """Only for a choice or a derived type"""

  def __init__(self,value):
    self.value = value
    self.tag = self.value['m_Tag']
    self.descriptions = []
    self.getDescriptions()
    k = 0
    while True:
      if self.descriptions[k]['index'] == self.tag:
        break
      k += 1
    self.tagToString()
    self.getChoicedType()

  def tagToString(self):
    self.tagString = CCPrettyPrinters.CCUtilities.fromCPointerToStringWithoutQuotes(self.descriptions[self.tag]['pszName'])

  def printField(self):
    return self.memberToString(self.choicedType)
  
  def getChoicedType(self): 
    #Useful to fetch member type: Getxxxx methods are in same order of FieldDescriptions array
    #But gdb.parse_and_eval works only on c++ const methods (like "Get....")
    getMethod = gdb.parse_and_eval(self.value.type.tag + "::" + "Get" + self.tagString)
    if getMethod.type.code != gdb.TYPE_CODE_FUNC:
      raise TypeError("Error in Get" + self.tagString + " method type")
    self.choicedType = getMethod.type.target()

  def memberToString(self,memberType):
    memberPtr = self.value['m_pMember']
    if memberPtr.type.code != gdb.TYPE_CODE_PTR:
      raise TypeError("Error in \"m_pMember\" type")
    member = memberPtr.dereference().cast(memberType)
    return str(member)

  def getDescriptions(self):
    descriptions = self.value['m_Descriptors']
    if descriptions is None:
      raise ValueError("Access error in \"m_Descriptors\" member")
    if descriptions.type.code != gdb.TYPE_CODE_PTR:
      raise TypeError("Error in \"m_Descriptors\" member type")
    self.descriptions = descriptions

  def to_string(self):
    strings = ["\n"]
    indent = CCPrettyPrinters.CCUtilities.incrementIndentation()
    try:
      strings.append(indent + "Choiced " + self.tagString + " (" + self.choicedType.tag + ")")
      strings.append(indent + self.printField())
    finally:
      CCPrettyPrinters.CCUtilities.decrementIndentation()
    return "".join(strings)

  def display_hint(self):
    return "Choice Type"

