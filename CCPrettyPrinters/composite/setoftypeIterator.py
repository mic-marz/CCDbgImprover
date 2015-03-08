######################################################################################
##                          CCIRCUIT DEBUG IMPROVER                                 ##
##                      Author: Michele Marzulli (emimarz)                          ##
##                      Date: 30/09/2014                                            ##
##                      Version: 1.0                                                ##
######################################################################################
import gdb
import gdb.types
import gdb.printing



#Iterator for SetOfPrinter (list walker)
class ListWalker(object):
  """For list embedded in setOfType objects"""

  def __init__(self,list,setOfValue):
    self.list = list
    self.elemCount = self.list['iElemCount']
    self.headElemPtr = self.list['pHead']
    if self.headElemPtr.type.code != gdb.TYPE_CODE_PTR:
      raise TypeError("Error in head element type of the list")
    self.currElem = self.headElemPtr.dereference() #currElem stores list element
    self.iterCount = 0
    self.getElemType(setOfValue)

  def getElemType(self,setOfValue):
    #Useful to fetch basic member type: 
    #But gdb.parse_and_eval works only on c++ const methods (like "This")
    getThisMethod = gdb.parse_and_eval(setOfValue.type.tag + "::" + "This")
    if getThisMethod.type.code != gdb.TYPE_CODE_FUNC:
      raise TypeError("Error in GetFirst method type")
    self.elemType = getThisMethod.type.target().target()

  def __iter__(self):
    return self

  def next(self):
    while (self.iterCount < self.elemCount):
      if self.currElem['pData'].type.code != gdb.TYPE_CODE_PTR : 
         raise TypeError("Error in element type of the list")
      retElem = self.currElem['pData'].dereference().cast(self.elemType)
      self.iterCount += 1
      self.currElem = self.currElem['pNext'].dereference()
      return retElem
    raise StopIteration
