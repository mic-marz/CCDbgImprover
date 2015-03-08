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

#CHSTRING PRINTER
#This printer is valid for Chstring and all types mapped to it 
#(like GraphicString, GeneralString, ...)
class ChstringPrinter(object): 
  """For Chstring and remapped objects"""

  def __init__(self,value):
    self.value = value

  def to_string(self):
    indent = CCPrettyPrinters.CCUtilities.incrementIndentation()
    try:
      strings = ["\n"]
      strings.append(indent)
      strings.append("Chstring value (len: " + str(self.value['len']))
      strings.append(") : " + CCPrettyPrinters.CCUtilities.fromCPointerToString(self.value['value']))
    finally:
      CCPrettyPrinters.CCUtilities.decrementIndentation()
    return "".join(strings)

  def display_hint(self):
    return "Chstring"


#C++ STD STRING PRINTER
class CplusplusStdstringPrinter(object):
  """For C++ std::string objects"""

  def __init__(self,value):
    self.value = value

  def to_string(self):
    indent = CCPrettyPrinters.CCUtilities.incrementIndentation()
    try:
      strings = ["\n"]
      strings.append(indent)
      strings.append("Std string value : ")
      strings.append(CCPrettyPrinters.CCUtilities.fromCPointerToString(self.value['_M_dataplus']['_M_p']))
    finally:
      CCPrettyPrinters.CCUtilities.decrementIndentation()
    return "".join(strings)

  def display_hint(self):
    return "C++ Std String"


###BOOLTYPE
class BoolPrinter(object):
  """Only for a boolean or a derived type"""

  def __init__(self,value):
    self.value = value

  def to_string(self):
    indent = CCPrettyPrinters.CCUtilities.incrementIndentation()
    try:
      strings = ["\n"]
      strings.append(indent)
      strings.append("Bool Value: ")
      strings.append(CCPrettyPrinters.CCUtilities.numericValueCharPrint(str(self.value['value'])))
    finally:
      CCPrettyPrinters.CCUtilities.decrementIndentation()
    return "".join(strings)

  def display_hint(self):
    return "Boolean Type"


#FLOAT PRINTER
class FloatPrinter(object): 
  """For Float objects"""

  def __init__(self,value):
    self.value = value
    self.mantissa = self.value['mantissa']
    self.base = self.value['base']
    self.exp = self.value['exp']

  def to_string(self):
    indent = CCPrettyPrinters.CCUtilities.incrementIndentation()
    try:
      strings = ["\n"]
      strings.append(indent)
      strings.append("Float value : ")
      strings.append(str(self.mantissa) + "*")
      strings.append(CCPrettyPrinters.CCUtilities.numericValueCharPrint(str(self.base)) + "^")
      strings.append(CCPrettyPrinters.CCUtilities.numericValueCharPrint(str(self.exp)))
    finally:
      CCPrettyPrinters.CCUtilities.decrementIndentation()
    return "".join(strings)


  def display_hint(self):
    return "Float Type"


#INTTYPE PRINTER
class IntTypePrinter(object): 
  """For Inttype objects"""

  def __init__(self,value):
    self.value = value

  def to_string(self):
    indent = CCPrettyPrinters.CCUtilities.incrementIndentation()
    try:
      strings = ["\n"]
      strings.append(indent)
      strings.append("Int value : " + str(self.value['value']))
    finally:
      CCPrettyPrinters.CCUtilities.decrementIndentation()
    return "".join(strings)

  def display_hint(self):
    return "Int Type"


#NULLTYPE PRINTER
class NullTypePrinter(object): 
  """For nulltype objects"""

  def __init__(self,value):
    self.value = value

  def to_string(self):
    indent = CCPrettyPrinters.CCUtilities.incrementIndentation()
    try:
      strings = ["\n"]
      strings.append(indent)
      strings.append("Null type object")
    finally:
      CCPrettyPrinters.CCUtilities.decrementIndentation()
    return "".join(strings)

  def display_hint(self):
    return "Null Type"


#OCTECTSTRING PRINTER
class OctectStringPrinter(object):
  """For octect string objects"""

  def __init__(self,value):
    self.value = value
    octStrPtr = self.value['value']
    if octStrPtr.type.code != gdb.TYPE_CODE_PTR:
      raise TypeError("Error in value type")
    self.octString = octStrPtr

  def to_string(self):
    indent = CCPrettyPrinters.CCUtilities.incrementIndentation()
    try:
      strings = ["\n"]
      strings.append(indent)
      strings.append("Octect string value (len: " + str(self.value['len']) + ") : ")
      for k in range(self.value['len']):
        strings.append("0x" + CCPrettyPrinters.CCUtilities.numericValueCharPrint(str(self.octString[k])) + " ")
    finally:
      CCPrettyPrinters.CCUtilities.decrementIndentation()
    return "".join(strings)

  def display_hint(self):
    return "OctectString Type"


#BITSTRING PRINTER
class BitStringPrinter(object):
  """For bit string objects"""

  def __init__(self,value):
    self.value = value

  def to_string(self):
    indent = CCPrettyPrinters.CCUtilities.incrementIndentation()
    try:
      strings = ["\n"]
      strings.append(indent)
      strings.append("Bit string value : ")
      val=int(str(self.value['value']))
      strings.append(bin(val))
    finally:
      CCPrettyPrinters.CCUtilities.decrementIndentation()
    return "".join(strings)

  def display_hint(self):
    return "BitString Type"
