######################################################################################
##                          CCIRCUIT DEBUG IMPROVER                                 ##
##                      Author: Michele Marzulli (emimarz)                          ##
##                      Date: 30/09/2014                                            ##
##                      Version: 1.0                                                ##
######################################################################################
#General utilities

__all__ = ['fromCPointerToString','fromCPointerToStringWithoutQuotes','numericValueCharPrint','handleCurrentIndentation','incrementIndentation','decrementIndentation']

#Modify output for C pointer such that only string is displayed (without address value)
def fromCPointerToString(pointer):
  return str(pointer).split(' ')[1]

def fromCPointerToStringWithoutQuotes(pointer):
  partial = str(pointer).split('\"')[1]
  return partial.split('\"')[0]

#Print only integer rapresentation of char (input is a multichar string)
def numericValueCharPrint(string):
  return string.split(' ')[0]


#Function to handle correct indentation levels for printing
#mode = 0 implies unit decrement on the indentation characters sequence and return current print
#mode = 1 implies unit increment on the indentation characters sequence and return current print

#Initialization value
counter = -1
multiplier = 4

def handleCurrentIndentation(mode):
  global counter
  if mode != 0 and mode != 1: 
    raise ValueError("Invalid indentation changing mode specified")
  if mode == 0: 
    counter -= 1 
  else:
    counter += 1
  ident = counter * multiplier
  return " "*ident 

def incrementIndentation():
  mode = 1
  return handleCurrentIndentation(mode)

def decrementIndentation():
  mode = 0
  return handleCurrentIndentation(mode)
  
