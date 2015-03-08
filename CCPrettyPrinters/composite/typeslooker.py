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


#For composite types
import CCPrettyPrinters.composite.enumeratedtype
import CCPrettyPrinters.composite.settype
import CCPrettyPrinters.composite.setoftype
import CCPrettyPrinters.composite.choicetype
import CCPrettyPrinters.composite.msg 

regexes = dict()
regexes['enumRegex'] = re.compile("enumeratedtype")
regexes['setRegex'] = re.compile("settype")
regexes['setofRegex'] = re.compile("setoftype")
regexes['choiceRegex'] = re.compile("choicetype")
regexes['msgRegex'] = re.compile("Message$")


compositePrinters = dict()
compositePrinters['enumPrinter'] = (regexes['enumRegex'],CCPrettyPrinters.composite.enumeratedtype.EnumPrinter)
compositePrinters['setPrinter' ]= (regexes['setRegex'],CCPrettyPrinters.composite.settype.SetPrinter) 
compositePrinters['setofPrinter'] = (regexes['setofRegex'],CCPrettyPrinters.composite.setoftype.SetOfPrinter)
compositePrinters['choicePrinter'] = (regexes['choiceRegex'],CCPrettyPrinters.composite.choicetype.ChoicePrinter)
compositePrinters['msgPrinter'] = (regexes['msgRegex'],CCPrettyPrinters.composite.msg.MsgPrinter)



#Object useful as printer with its own subprinters
class CompositeTypesLooker(object):
  """General Composite Types Looker"""

  def __init__(self,value):
    self.value = value

  def to_string(self):
    found = False
    for member in self.value.type.fields():
      if member.is_base_class == True:
        memberType = member.type.tag
        for printer in compositePrinters:
          if re.search(compositePrinters[printer][0], memberType) is not None:
            pr = compositePrinters[printer][1](self.value)
            return pr.to_string()
    return None 

  def display_hint(self):
    return "General types looker with suprinters (for composite types)"

