######################################################################################
##                          CCIRCUIT DEBUG IMPROVER                                 ##
##                      Author: Michele Marzulli (emimarz)                          ##
##                      Date: 30/09/2014                                            ##
##                      Version: 1.0                                                ##
######################################################################################
import re
import os 
import gdb
import gdb.types
import gdb.printing


objTypes = dict()
objTypes['opiHandle'] = re.compile("opiHandle")
objTypes['ooTypedItr'] = re.compile("_ooTypedItr")
objTypes['ooNameTypedItr'] = re.compile("_ooNameTypedItr")

regex = re.compile("^\$")
tempfile = os.getcwd() + "/" + "tempfile.txt"


class PowerPrint(gdb.Command):
    """GDB command to print IptNMS Circuit objects and simple ones

    Usage: powerprint [object]
    """
	
    def __init__(self):
        super(PowerPrint, self).__init__("powerprint",gdb.COMMAND_DATA)

    def invoke(self,arg,from_tty):
        argv = gdb.string_to_argv(arg);
        argc = len(argv)
        if argc > 1:
	  print "Sorry, one argument at time, please!"
	if argc == 0:
	  print "Sorry, at least one argument, please"
        if argc == 1:
	  value = gdb.parse_and_eval(arg)
	  if value is None:
	    print "Sorry, I can't evaluate the given argument!"
          else:
            if value.type.tag is not None:
	      for objType in objTypes:
	        if re.search(objTypes[objType],value.type.tag):
                  self.prepareForCleanOutput()
                  self.printObjectName(arg)
                  self.printObjectId(value)
                  self.cleanOutput()
		  return None
            #if arg isn't a db object or is a simple var (tag attr is None), try with traditional print command 
            printCommand = "print " + arg    # this print however could invoke some pretty printer!!
            gdb.execute(printCommand)
            return None

    def complete(self,text,word):
	return gdb.COMPLETE_COMMAND
    
    def printObjectName(self,objName):
	getNameCommand = "print " + objName + "->" + "GetName()"
	print "OBJECT NAME:"
	gdb.execute(getNameCommand)

    def printObjectId(self,value):
        DB = value['_id']['_DB']
        OC = value['_id']['_OC']
        page = value['_id']['_page']
        slot = value['_id']['_slot']
	print "OBJECT ID:"
        print "_DB: {0}, _OC: {1}, _page: {2}, _slot: {3}".format(DB,OC,page,slot)
        
    def prepareForCleanOutput(self):
        gdb.execute("set logging file " + tempfile)
        gdb.execute("set logging redirect on")
        gdb.execute("set logging overwrite on")
        gdb.execute("set logging on")

    def cleanOutput(self):
        gdb.execute("set logging off")
        with open(tempfile,"r") as f:
          for line in f:
	    if not regex.search(line): 
            	print line.strip() 
        os.remove(tempfile)

	
        


def register_custom_commands():
    """Method to insert all command objects to add"""
    PowerPrint()

register_custom_commands()


