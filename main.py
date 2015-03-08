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


packageDir = gdb.PYTHONDIR + "/CCDbgImprover"
if packageDir not in sys.path:
  sys.path.append(packageDir)


#For commands
import CCCommands


#Pretty printings
#For basic types
import CCPrettyPrinters.basic
import CCPrettyPrinters.composite.typeslooker
import CCPrettyPrinters.composite.reference

basicPrinters = dict()
#Each dictionary value contains a tuple in the form (pattern, printer object)
basicPrinters['ChStringPrinter'] = ('Chstring',CCPrettyPrinters.basic.general.ChstringPrinter)
basicPrinters['C++StdStringPrinter'] = ('std::basic_string',CCPrettyPrinters.basic.general.CplusplusStdstringPrinter)
basicPrinters['BoolPrinter'] = ('Booltype',CCPrettyPrinters.basic.general.BoolPrinter)
basicPrinters['IntTypePrinter'] = ('Inttype',CCPrettyPrinters.basic.general.IntTypePrinter)
basicPrinters['FloatPrinter'] = ('Float',CCPrettyPrinters.basic.general.FloatPrinter)
basicPrinters['NullTypePrinter'] = ('nulltype',CCPrettyPrinters.basic.general.NullTypePrinter)
basicPrinters['OctectStringPrinter'] = ('OctectString',CCPrettyPrinters.basic.general.OctectStringPrinter) 
basicPrinters['BitStringPrinter'] = ('Bitstring',CCPrettyPrinters.basic.general.BitStringPrinter)


pBr = gdb.printing.RegexpCollectionPrettyPrinter("Basic Types Printers")
for printer in basicPrinters:
  pBr.add_printer(printer,basicPrinters[printer][0],basicPrinters[printer][1])


pCr = gdb.printing.RegexpCollectionPrettyPrinter("General Composite Printer")
#Subprinter for interface types
pCr.add_printer('I38Printer','^I38_',CCPrettyPrinters.composite.typeslooker.CompositeTypesLooker) 
pCr.add_printer('I36Printer','^I36_',CCPrettyPrinters.composite.typeslooker.CompositeTypesLooker) 
pCr.add_printer('ICHRHPrinter','^ICHRH_',CCPrettyPrinters.composite.typeslooker.CompositeTypesLooker) 
pCr.add_printer('ILHPrinter','^ILH_',CCPrettyPrinters.composite.typeslooker.CompositeTypesLooker) 
pCr.add_printer('LMPrinter','^LM_',CCPrettyPrinters.composite.typeslooker.CompositeTypesLooker) 
pCr.add_printer('IHFeederrinter','^IHFEEDER_',CCPrettyPrinters.composite.typeslooker.CompositeTypesLooker) 



#gdb.printing.register_pretty_printer inserts objects at the beginning of the list 
gdb.printing.register_pretty_printer(None,pBr)
gdb.printing.register_pretty_printer(None,pCr)

#Reference Types Printer must be the first one checked by gdb!!!
#It returns a gdb.Value object relative to the target type
pRr = CCPrettyPrinters.composite.reference.ReferencePrinterWrapper("Reference Types Printer")
gdb.pretty_printers.insert(0,pRr)


