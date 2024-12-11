# SIRP-D-SI Converter Service

This software ensures the reliability of the <a href="https://gitlab1.ptb.de/d-ptb/d-si/xsd-d-si/-/blob/master/wiki/doc/UnitSystem.md">D-SI Syntax</a> by testing its internal syntax consistencies and by providing metadata within the <a href="https://si-digital-framework.org/SI/unitExpr?lang=en">SI Reference Point</a> (SIRP), which relates to prefixes, units, and exponents.

The software accepts Base or Compound Units in D-SI unit syntax and provides several pieces of information about the input:

* Its consistency according to the D-SI Syntax.

* Its transformation into Prefixes, Units and Exponents SIRP Syntax. 

* Its representation as a Permanent Identifier according to SIRP.

* Its representation as an RDF structure according to SIRP. 

* Its Metadata from the SIRP framework.

## Code Files

Several D-SI Compound Units are being shown as examples to demonstrate the functionality of the software.

### transformation.py: 

This file handles the validation and transformation logic.

### app.py:

This file serves as the flask interface.

### test.py:

This file serves as an example of how the classes from the transformation.py can be used inside any other software

### Classes

There are four main classes that can be accessed externally:

* class verboseDsiCompoundUnitValidation
  
The function messageResponse(compoundunit) within the class provides detailed information regarding the validation of the D-SI Compound Unit. If the input Compound Unit is valid, the information detailed above. If it is invalid, the class returns different messages depending on whether the Compound Unit is a valid D-SI unit or not. Additionally, it offers suggestions for correcting the input Compound Unit.

* class jsonDsiCompoundUnitValidation

The function messageResponse([string]) within the class provides detailed information regarding the validation of the D-SI Compound Unit. If the input Compound Unit is valid, the information detailed above. If it is invalid, the class returns different messages depending on whether the Compound Unit is a valid D-SI unit or not. Additionally, it offers suggestions for correcting the input Compound Unit.

* class compoundUnitValidation

The funtion validation([string]) within the class performs the validation and stores the results in variables that can be accessed externally.

* class dsiValidator

This is used to interact from the power shell.

## Example Usage 

### Prerequisites for everything except the web server:

This is an example of how to list things you need to use the software and how to install them.
* python
  ```
  pip install rdflib
  pip install re
  pip install sys
  pip install pprint
  ```
### dsiValidator
* python
 ```
 python trasformation.py -h
 #shows the help
 ```
* python
 ```
 python trasformation.py -json \metre
 #inputs the DSI unit after the '-json' and returns information about the unit in json format
 ```
* python
 ```
 python trasformation.py -v \metre
 #inputs the DSI unit after the '-v' and returns information about the unit in a verbose way
 ```

### test.py

 ```
 #input:
 info=compoundUnitValidation('\\metre')
 info.validation()
 #variables that can be accessed:
 print(f"The {info.input_compound_unit} validation is: {info.valid_dsi_unit}")
 print(f"The unit has an SIRP correspondance: {info.output_sirp_correspondance}")
 print(f"The system has a message: {info.output_human_message}")
 print(f"The SIRP PID Unit is: {info.output_pid}")
 print(f"The SIRP Unit is: {info.output_compound_unit}")
 ```
        
## Terminology

* D-SI Prefix: (e.g. \milli, \kilo, etc.)

* D-SI Unit: (e.g. \gram, \candela, \metre, etc.)

* D-SI Exponent: (e.g. \tothe{5}, etc.)

* SIRP Prefix: (e.g. milli, kilo, etc.)

* SIRP Unit: (e.g. gram, candela, metre, etc.)

* SIRP Symbol: (e.g. m, s, kg)

* SIRP Exponent: (e.g. -1, 2, 5, etc.)

* SIRP Compound Unit Symbol: (e.g. m-1, m·s-2, kg)

* SIRP Compound Unit PID: (e.g. https://si-digital-framework.org/SI/units/millisecond-1)
