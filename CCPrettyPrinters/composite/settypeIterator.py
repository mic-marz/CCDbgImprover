######################################################################################
##                          CCIRCUIT DEBUG IMPROVER                                 ##
##                      Author: Michele Marzulli (emimarz)                          ##
##                      Date: 30/09/2014                                            ##
##                      Version: 1.0                                                ##
######################################################################################
import gdb
import gdb.types
import gdb.printing


#Iterator for SetPrinter:
#iterates only on present fields and returns indexes
class SetWalker(object):
  """For set types"""

  def __init__(self, setValue):
    self.index = 0
    self.numMembers = setValue.value['m_NumMembers']
    self.mask = setValue.value['m_Mask'] 

  def __iter__(self):
    return self

  def next(self):
    j = self.index
    while j < self.numMembers:
      if self.mask & (1 << j):
        self.index = j + 1  
        return j 
      j += 1
    raise StopIteration
