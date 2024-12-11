#####
#Example:
#input='\\milli\\second\\tothe{-1}\\milli\\volt\\tothe{2}'
#info_u=transformation(input)
#####
from rdflib import Graph, Literal, RDF, Namespace, BNode
import re, sys
import pprint

    
#validate data
class verboseCompoundUnitValidation:
    """
    Class to output verbose data from class compoundUnitValidation
    
    
    """
    def __init__(self,dsiCompoundUnit):
        self.input_compound_unit=str(dsiCompoundUnit)
    
    def verbose_response(self):
        
        info=compoundUnitValidation(self.input_compound_unit)
        info.validation()
        
        if(info.output_sirp_correspondance):
            print("")
            print('D-SI Input Compound Unit:', self.input_compound_unit)
            print("#")
            print(f"valid D-SI Unit: {info.valid_dsi_unit}")
            print("")
            print(f"output human message Validation: {info.output_human_message}")
            print("")
            print('SIRP Compound Unit: ', info.output_compound_unit)
            
            print("")
            print('SIRP PID: ', info.output_pid)
            
            print("")
            print('SIRP\'s Predicates and Objects according to each Subject without its prefix to asure human readibility:')
            print(' ')
            print('     [object,predicate,subject]')
            print(' ')
            for string in info.sirp_metadata_triples:
                print('    ', string)
            
            print('.............')
            
            print("Compound Unit ttl:")
            
            print(info.__g__.serialize(format="ttl"))
            
            print("#")
        else:
            print('Input Compound Unit:', self.input_compound_unit)
            print("#")
            print(f"valid D-SI Unit: {info.valid_dsi_unit}")
            print("#")
            print(f"output human message Validation: {info.output_human_message}")
            print("#")
            
class json_compound_unit_validation:
    """
    Class to output json data from compoundUnitValidation
    
    """
    
    def __init__(self,dsiCompoundUnit):
        self.input_compound_unit=str(dsiCompoundUnit)
        # Estructura JSON
    
    def __create_sirp_json__(self,input_unit,validity_output_human_message,\
                             sirp_syntax,output_pid,triple,ttl_metadata,\
                                 valid_dsi_unit,output_sirp_correspondance):
        #input_unit,validity_output_human_message,sirp_syntax,output_pid,metadata
        
        #output: json
        
        
        data = {
            "__input unit__":"this is the input compound unit intended to be\ a d-si unit__",
            "input_unit": input_unit,
            "__results_":"the validation output_human_message",
            "results": {
                "validation_output_human_message": validity_output_human_message,
                "valid_boolean":valid_dsi_unit,
                "validSirpBoolean":output_sirp_correspondance
            
            },
            "__sirp_transformation__":"tbd",
            "sirp_transformation": {
                "sirp_syntax": sirp_syntax
            },
            "__permanent_identifier__":"tbd",
            "permanent_identifier": {
                "identifier": output_pid
            },
            "__rdf_representation__":"tbd",
            "rdf_representation": {
                "sirp_metadata_triples": triple
            },
            "__metadata__":"tbd",
            "metadata": {
                "ttl_representation": ttl_metadata
            }
        }
        
        
                
        return data
        
        
    def json_message_response(self):
        
        #
        #function to interface with flask
        #
        
        info=compoundUnitValidation(self.input_compound_unit)
        info.validation()
        
        
        # Convertir a JSON
        #json_output = json.dumps(info.data, indent=4)
        sirp_metadata_triples=[]
        for string in info.sirp_metadata_triples:
            sirp_metadata_triples.append(string)
        serializedTtl=info.__g__.serialize(format="ttl")
        
        json_output = self.__create_sirp_json__(info.input_compound_unit,
                                            info.output_human_message,
                                            info.output_compound_unit,
                                            info.output_pid,
                                            sirp_metadata_triples,
                                            serializedTtl,
                                            info.valid_dsi_unit,
                                            info.output_sirp_correspondance
                                            )
        
        # Mostrar resultado
                
        return json_output

class compoundUnitValidation:
    
    """
    
    Class to convert D-SI unit to SIRP and validate D-SI units
    
    """
    
    
    def __init__(self,input_compound_unit):
        #acccesible from outside
        self.input_compound_unit=str(input_compound_unit) #the input
        self.output_compound_unit="" 
        self.sirp_metadata_triples=[]
        self.output_pid=""
        self.output_human_message=None
        self.valid_dsi_unit=True
        self.output_sirp_correspondance=False
        
        #the self_list classified by prefix unit or exponent
        self.__input_compound_unitAsAList__ = ""
        self.__input_compound_unit_classified__ = [] #the input_compound_unit separated in a list
        self.__filteredCompoundUnitComponentsAsAList__=""
        self.__prefixPID__='https://si-digital-framework.org/SI/units/'
        self.__error_unchaining_compound_unit__=False
        self.__error_classifying_unit__=False
        
        
        # Definir los namespaces
        self.__SI__ = Namespace("http://si-digital-framework.org/SI#")
        self.__UNITS__ = Namespace("http://si-digital-framework.org/SI/units/")
        self.__XSD__ = Namespace("http://www.w3.org/2001/XMLSchema#")
        self.__PREFIXES__ = Namespace("http://si-digital-framework.org/SI/prefixes/")
        self.__OWL__ = Namespace("http://www.w3.org/2002/07/owl#")
        self.__RDF_NS__ = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
        self.__RDFS__ = Namespace("http://www.w3.org/2000/01/rdf-schema#")
        self.__g__=Graph()
        self.__g__.bind("si", self.__SI__)
        self.__g__.bind("units", self.__UNITS__)
        self.__g__.bind("prefixes", self.__PREFIXES__)
        self.__g__.bind("owl", self.__OWL__)
        self.__g__.bind("xsd", self.__XSD__)
        
        #These are unit to check the validation of the input
        
        self.__unit_decibel__=['decibel']
        
        self.__component_per__=['per']
        
        self.__unit_meter__ = ["meter"]
               
        self.__dsi_unit_degree_celsius__ = ["degreecelsius"]
        
        self.__sirp_unit_degree_Celsius__ = ["degreeCelsius"]
        
        #pref to be check
        self.unitsWithoutPrefixes = ["one", "kilogram",'ppm','percent']
        
        self.unitsWithoutKilo = ["gram"]
        
        #exponents to be check
        self.unitsWithoutExponents = ["one",'ppm','percent']

        #decimal units outside SIRP
        self.decimalDsiUnitsWithoutCorrespondanceInSIRP=["one","ppm","percent"]
        
        self.eightEdSiBrochUnits=['clight','planckbar','electronmass',\
        'naturalunittime','elementarycharge','atomicunittime','bohr',\
        'hartree','bar','mmHg','angstrom','nauticalmile','barn','knot',\
        'erg','dyne','poise','stokes','stilb','phot','gal','maxwell',\
        'gauss','oersted']
        
        #non si units
        self.allowedNonSIUnit=['minute','hour','day','degree',\
        'arcminute','arcsecond','hectare','litre','tonne',\
        'electronvolt','dalton','astronomicalunit','neper',\
        'bel']
        
        #binary
        self.binaryDsiPrefixesWithoutCorrespondanceInSIRP=['kibi','mebi',\
                                                            'gibi', 'tebi',\
                                                           'pebi','exbi',\
                                                               'zebi','yobi']
        self.binaryDsiUnitsWithoutCorrespondanceInSIRP=["bit","byte"]
        
        #decimal prefixes
        self.decimalPrefixes=['deca','hecto','kilo','mega','giga',\
        'tera','peta','exa','zetta','yotta','ronna','quetta','deci',\
        'centi','milli','micro','nano','pico','femto','atto','zepto',\
        'yocto','ronto','quecto']
        
        #
        self.siDerived=['gram','radian','steradian','hertz',\
        'newton','pascal','joule','watt','coulomb','volt','farad'\
        'ohm','siemens','weber','tesla','henry','degreecelsius'\
        'lumen','lux','becquerel','sievert','gray','katal','bit'\
        'byte','ppm','percent']
        
        #
        self.dsiPlatinumUnits=['one','day','hour','minute',\
        'degree','arcminute','arcsecond']
        
        #
        self.siBaseUnits=['metre','kilogram','second',\
        'ampere','kelvin','mole','candela']

    #principal

    def validation(self):
        #
        #Main function of the class
        #
        
        ###
        #set up info 
        ###
        self.__set_up__()
        ####
        #First unchain the components within the string given
        ####
        self.__unchain_input_compound_unit__()
        ####
        #Then match the words as pref, units or exponents with sirp ttl
        ####
        
        if( not self.__error_unchaining_compound_unit__):
            self.__classify_compound_unit_components__()
            if (not self.__error_classifying_unit__):
                self.__check_compound_unit_syntax__()
                if (self.output_sirp_correspondance):
                    self.__sirp_meta_data_output__()
                    self.__extract_unique_dsi_components__()
                    self.__output_triplets__()
            
                else: return None        
            else: return None                    
        else: return None
        
        
    def __set_up__(self):
        
        self.__error_unchaining_compound_unit__=False
        self.__error_classifying_unit__=False
        self.output_sirp_correspondance=True
        self.valid_dsi_unit=True
        return None
        
        
    #############
    #main function 1           
    #############
    
    def __unchain_input_compound_unit__(self):
        ####
        #unchain words separated by "\\" in a vector 
        #
        #receives self.input_compound_unit
        #delivers: self.__input_compound_unitAsAList__
        # if error: self.output_human_message="Syntax recognition error, missing '\\' "
        #
        ####
        if not self.input_compound_unit.startswith("\\"): 
            self.__error_unchaining_compound_unit__=True
            self.valid_dsi_unit=False
            self.output_sirp_correspondance=False
            if(not self.output_human_message): 
                self.output_human_message="Syntax recognition error, missing '\\' "
            return None

        #####
        #unchains the d-si units pattern into different components in a list
        #####
        patron = r'[^\\{}]+(?:\{[^}]*\})*'
        
        # find all the words
        input_compound_unitAsAList = re.findall(patron, self.input_compound_unit)
        
        #words->__input_compound_unitAsAList__
        
        # Limpiar espacios en blanco en cada palabra si es necesario
        input_compound_unitAsAList = [p.strip() for p in input_compound_unitAsAList]
        
        self.__input_compound_unitAsAList__=input_compound_unitAsAList
    
    #############
    #main function 2           
    #############
    
    def __classify_compound_unit_components__(self):
        ####
        ##check if it any of the elements are recognizable words 
        ##and add it to the list  
        ####
        # inputs: self.__input_compound_unitAsAList__
        #
        # outputs: self.__input_compound_unit_classified__
        #          
        #          self.output_human_message
        #          
        
        for subject in self.__input_compound_unitAsAList__:
            newEntry=self.__actual_prefix_search__(subject)
            if (newEntry!=None): 
                self.__input_compound_unit_classified__.append(newEntry)
                #print(f"newEntry: {newEntry}")
            
            else:
                newEntry=self.__actual_unit_search__(subject)
                
                if(newEntry!=None and len(newEntry)==7):
                    #print(f"newEntry: {newEntry}")
                    self.__input_compound_unit_classified__.append(newEntry)
                    
                    
                elif (newEntry!=None and len(newEntry)==2):
                    #print(f"newEntry: {newEntry}")
                    subject=self.__actual_prefix_search__(newEntry[0])
                    
                    self.__input_compound_unit_classified__.append(subject)
                    subject=self.__actual_unit_search__(newEntry[1])
                    
                    self.__input_compound_unit_classified__.append(subject)
                    
                else:
                    newEntry=self.__exponent_issue__(subject)
                    #print(f"newEntry: {newEntry}")
                    if (newEntry!=None):
                        self.__input_compound_unit_classified__.append(newEntry)
                    else: 
                        self.__error_classifying_unit__=True
                        self.output_sirp_correspondance=False
                        self.valid_dsi_unit=False
                        if(not self.output_human_message): 
                            self.output_human_message=f"Syntax not found: no subject, unit, or exponent:'\\{subject}'."
                        return None
        if(self.valid_dsi_unit and not self.output_human_message): 
            self.output_human_message="Valid D-SI Unit"

    def __exponent_issue__(self,subject):
        #
        # search for the exponent string
        #
        #input: subject
        #output: vector if its ok
        #none if it is not
        
        pattern = r"(-?\d+)"
        # Buscar el número en la cadena
        match = re.search(pattern, subject)
        
        if not(match): return None
           
        # Extraer el número encontrado
        number = match.group(1)
        # Crear el nuevo string con el formato "tothe{numero}"
        newChain = f"tothe{{{number}}}"
        # Comparar con la cadena original
        if newChain == subject: return ["exponent",subject,number]
        else: return None
    
    def __actual_unit_search__(self, searchSubject):
        
        #
        #inputs:
        #
        #outputs:
        #
        
        
        #This is for the case the input subject has to be changed, and preserve both.
        correctedSubject=searchSubject
                
        #
        #these are exceptions to still have a valid D-SI unit without corresponce in SIRP:
        #
        
        
        if (searchSubject in self.decimalDsiUnitsWithoutCorrespondanceInSIRP):
            #These are not only stand alone units, for now but doesnt have a correspondance in SIRP
            self.output_sirp_correspondance=False
            if(not self.output_human_message): 
                self.output_human_message=f"The Unit '\\{searchSubject}' is a Valid D-SI Unit, that is not included in the SIRP"
            return(["unit",searchSubject,"","decimal",correctedSubject,"SI unit","Not Included in SIRP"])
        
        elif (searchSubject in self.binaryDsiUnitsWithoutCorrespondanceInSIRP):
            self.output_sirp_correspondance=False
            if(not self.output_human_message): 
                self.output_human_message=f"The Unit '\\{searchSubject}' is a Valid Binary D-SI Unit, that is not included in the SIRP"
            return(["unit",searchSubject,"","binary",correctedSubject,"SI unit","Not Included in SIRP"])
        
        elif (searchSubject in self.eightEdSiBrochUnits):
            self.output_sirp_correspondance=False
            if(not self.output_human_message): 
                self.output_human_message=f"The Unit '\\{searchSubject}' is a Valid D-SI Unit included in the 8th Edition SI Brochure, but not in the SIRP"
            return(["unit",searchSubject,"","decimal",correctedSubject,"SI unit","Not Included SIRP"])
        
        
        #
        #these are exceptions not allowded:
        #
        
        #per not allowded
        elif (searchSubject in self.__component_per__):
            self.__error_classifying_unit__=True
            self.output_sirp_correspondance=False
            self.valid_dsi_unit=False
            self.output_human_message="The mapping of \\per to the SIRP is not implemented yet."
            return None
        
        #degreeCelsius not allowed
        elif(searchSubject in self.__sirp_unit_degree_Celsius__):
            self.__error_classifying_unit__=True
            self.output_sirp_correspondance=False
            self.valid_dsi_unit=False
            self.output_human_message="The notation '\\degreeCelsius' is not allowded in the D-SI, use the notation '\\degreecelsius' instead"
            return None
        
        
        #meter notation
        elif (searchSubject in self.__unit_meter__):
            print(searchSubject)
            self.__error_classifying_unit__=True
            self.output_sirp_correspondance=False
            self.valid_dsi_unit=False
            self.output_human_message="The notation \\meter is not allowded in the D-SI, use the notation \\metre instead"
            return None
        
        #
        #This is to change the subject towards validating the unit:
        #
        
        #if I have to split the decibel
        elif(searchSubject in self.__unit_decibel__):
            return "deci","bel"
            
        #is the subject compatible to be queriable?
        elif (not(self.__is_valid_uri_subject__(searchSubject))):
            return None

        #change degreecelsius  to quereable degreeCelsius
        elif (searchSubject in self.__dsi_unit_degree_celsius__):
            #self.__error_classifying_unit__=True
            searchSubject=self.__sirp_unit_degree_Celsius__[0]
        
        #
        #To query the subject:
        #
        
        #is there in the ttl?
        #input: subject to find in the ttl; context: i
        g_units = Graph()
        g_units.parse("SI_Digital_Framework/SI_Reference_Point/TTL/units.ttl", format="ttl")
        query_ = f"""
            SELECT ?objeto WHERE {{
                <http://si-digital-framework.org/SI/units/{searchSubject}> <http://si-digital-framework.org/SI#hasSymbol> ?objeto .
        }}
        """
        
        #print(query_)
        try:
            results = g_units.query(query_)
        except Exception as e:
            self.output_human_message = f"Error executing query: {str(e)}"
            return None
        
        for row in results:
            info=["unit",searchSubject,str(row.objeto),"decimal",correctedSubject,"SI unit","included in SIRP"]
            return(info)

    def __actual_prefix_search__(self, subject):
        
        #
        #Check if subject is a D-SI unit and or SIRP unit
        #
        #input: a vector if it is a valid d-si unit
        #
        #output: None if it is not
        #
        
        #This is to have a valid dsi unit without sirp correspon
        if (subject in self.binaryDsiPrefixesWithoutCorrespondanceInSIRP):
            return(["prefixes",subject,"","binary","SI prefix","Not Included in SIRP"])
        
        #to have a valid uri subject: 
        elif (not(self.__is_valid_uri_subject__(subject))):
            return None
        
        else:
            g_prefixes = Graph()
            g_prefixes.parse("SI_Digital_Framework/SI_Reference_Point/TTL/prefixes.ttl", format="ttl")        
            query = f"""
                SELECT ?objeto WHERE {{
                    <http://si-digital-framework.org/SI/prefixes/{subject}> <http://si-digital-framework.org/SI#hasSymbol> ?objeto .
            }}
            """
            results = g_prefixes.query(query)
            
            for row in results:
                return(["prefixes",subject,str(row.objeto),"decimal","SI prefix","Not Included in SIRP"])
    
    def __is_valid_uri_subject__(self,subject):
        #
        #check if the unit is querable
        #
        #input: subject to be quearied,
        #
        #output: true ok to be
        #       false not possible
        #
        # Expresión regular que coincide con caracteres permitidos en un URI
        pattern = r'^[a-zA-Z0-9._~:/?#\[\]@!$&\'()*+,;=%-]+$'
        
        if re.match(pattern, subject):
            return True
        else:
            return False

    #############
    #main function 3          
    #############
    
    def __check_compound_unit_syntax__(self):
        #
        #check if the syntax of te comp unit is ok according to D-SI
        #
        #internal functions: self.__check_unit_with_exponent__()
        #
        #input: self.__input_compound_unit_classified__
        #
        #outputs: self.output_human_message
        #         None when the proccess has ended
        
        compound_unit_list = self.__input_compound_unit_classified__
        
        #print(compound_unit_list)
        
        if not compound_unit_list or not compound_unit_list[0]:
            self.output_sirp_correspondance=False
            self.valid_dsi_unit=False
            self.output_human_message = "No unit provided"
            return None
        #print(len(compound_unit_list))
        
        j = 0
        
        while j < len(compound_unit_list):
            current = compound_unit_list[j][0]
            
            if current == "prefixes":
                if j + 1 >= len(compound_unit_list) or compound_unit_list[j + 1][0] != "unit":
                    #si el siguiente no es una unidad...
                    self.output_sirp_correspondance=False
                    self.valid_dsi_unit=False
                    self.output_human_message = f"After the prefix '\\{compound_unit_list[j][1]}', there should be a unit."
                    return None
                else:
                    if self.__check_prefix_with_unit__(compound_unit_list[j], compound_unit_list[j + 1]):
                        if j + 2 < len(compound_unit_list) and \
                            compound_unit_list[j + 2][0] == "exponent" \
                            and self.__check_unit_with_exponent__(compound_unit_list[j + 1][1], compound_unit_list[j + 2][1]):
                            j += 3  # Mover al siguiente bloque si hay un exponente válido
                        else:
                            j += 2  # Avanzar si no hay exponente
                    else:
                        return None

            elif current == "unit":
                if j + 1 < len(compound_unit_list) and compound_unit_list[j + 1][0] == "exponent":
                    if self.__check_unit_with_exponent__(compound_unit_list[j][1], compound_unit_list[j + 1][1]):
                        j += 2  # Avanzar si hay un exponente válido
                    else:
                        return None
                else: 
                    j+=1
                
                
            elif current == "exponent":
                
                self.output_sirp_correspondance=False
                self.valid_dsi_unit=False
                self.output_human_message = f"Before the exponent '\\{compound_unit_list[j][1]}', there should be a unit."
                return None

            else:
                
                self.output_sirp_correspondance=False
                self.valid_dsi_unit=False
                self.output_human_message = "Error"
                return None
        
        return None

    def __check_prefix_with_unit__(self, prefix,unit):
        ###
        ##return true if they are compatible
        ###
        #input:  self.__input_compound_unitAsAList__
        #        unit
        #        prefix
        #
        #output: 
        #        self.output_human_message
        #        true/None
        
        arr=self.__input_compound_unitAsAList__
        for i in range(len(arr)):
            if arr[i] == "deci" and arr[i+1] == "bel":
                self.output_sirp_correspondance=False
                self.valid_dsi_unit=False
                self.output_human_message = "The unit '\\deci\\bel' should be '\\decibel'. Unit not allowded in the D-SI"

        #check if the actual unit was written after a correct prefix
        checkUnitWithPrefix=(unit[1] in self.unitsWithoutPrefixes)                
        #check if kilo is present
        checkUnitWithoutKiloGram = ( (prefix[1] == "kilo") and (unit[1] == "gram") )
        
        checkDecimalOrBinaryCompoundUnit = prefix[3] != unit[3] 
        
        if checkUnitWithPrefix:
            
            self.output_sirp_correspondance=False
            self.output_human_message=f"The Compound Unit '\\{unit[1]}' should not have a prefix."
            self.valid_dsi_unit=False
            return None
        
        elif checkUnitWithoutKiloGram:
            self.output_sirp_correspondance=False
            self.output_human_message=f"The Compound Unit '\\{prefix[1]}\\{unit[1]}' should be written as '\\kilogram'."
            self.valid_dsi_unit=False
            return None
            
        elif checkDecimalOrBinaryCompoundUnit:
            self.output_sirp_correspondance=False
            self.output_human_message=f"Compatibility Error: Prefix '\\{prefix[1]}' is {prefix[3]}', and Unit '\\{unit[1]}' is {unit[3]}."
            self.valid_dsi_unit=False
            return None

        
        
        else: return True

    def __check_unit_with_exponent__(self, unit, exponent):
        ###
        ##return true if they are compatible
        ###
        #receives: unit exponent
        #return: True if the unit belongs to the units with exponents
        # None
        #check if the actual unit was written after a correct prefix
        #
        
        check_unit_with_exponent=(unit in self.unitsWithoutExponents)
        
        if check_unit_with_exponent:
            self.output_sirp_correspondance=False
            self.output_human_message=f"The unit '\\{unit}' should not have an exponent."
            self.valid_dsi_unit=False
            return None
        else: return True
    
    
    #############
    #main function 4
    #############
    
    def __sirp_meta_data_output__(self):
        ###
        # to output metadata 
        #
        # input: list of compound unit list classified in d-si
        #
        # output: the unit in sirp
        ###
        
        
        compound_unit_list = self.__input_compound_unit_classified__
        compoundUnit = ""
        PID = ""

        j = 0
        while j < len(compound_unit_list):
            current = compound_unit_list[j][0]

            if current == "prefixes":
                
                compoundUnit += compound_unit_list[j][2] + compound_unit_list[j + 1][2]
                PID += compound_unit_list[j][1] + compound_unit_list[j + 1][1]
                
                if j + 2 < len(compound_unit_list) and compound_unit_list[j + 2][0] == "exponent": #if it is prefix unit + exponent:
                    
                    #e.g. [km-2]
                    compoundUnit += compound_unit_list[j + 2][2]
                    PID += compound_unit_list[j + 2][2]
                    
                    if j + 3 < len(compound_unit_list):
                        #more than one pre uni expo
                        if(j==0):
                            #it was the first pre uni expo
                            UnitProduct=self.__left_prefix_unit_exponent_product__(compound_unit_list[j][1],
                                                                               compound_unit_list[j+1][1],
                                                                               compound_unit_list[j+2][2])
                            
                        else:
                            UnitProduct=self.__right_prefix_unit_exponent_product__(compound_unit_list[j][1],\
                                                                                compound_unit_list[j+1][1],\
                                                                                    compound_unit_list[j+2][2],\
                                                                                        UnitProduct)
                            UnitProduct=self.__combine_product__(UnitProduct)
                        #move to the next
                        j += 3
                        compoundUnit+='.'
                        PID+='.'
                        
                    else:
                        if(j==0):
                            #it was the first and last unit
                            self.__unique_prefix_unit_exponent__(compound_unit_list[j][1],\
                                                              compound_unit_list[j+1][1],\
                                                              compound_unit_list[j+2][2])
                            #move to the next and end
                            
                        else:
                            #it was the last but not the first
                            UnitProduct=self.__right_prefix_unit_exponent_product__(compound_unit_list[j][1],\
                                                                                compound_unit_list[j+1][1],\
                                                                                compound_unit_list[j+2][2],\
                                                                                    UnitProduct)
                        j += 3
                else:#solo es prefijo y unidad                    
                    if j + 2 < len(compound_unit_list):
                        if (j==0):
                            #first prefix and unit
                            UnitProduct=self.__left_prefix_unit_product__(compound_unit_list[j][1],compound_unit_list[j+1][1])
                            
                        else:
                            #not first pref and unit
                            UnitProduct=self.__right_prefix_unit_product__(compound_unit_list[j][1],\
                                                                        compound_unit_list[j+1][1],\
                                                                        UnitProduct)
                            UnitProduct=self.__combine_product__(UnitProduct)
                        #move to the next
                        j += 2
                        compoundUnit+='.'
                        PID+='.' 
                        
                    else:
                        if(j==0):
                            #Only prefix and unit
                            #e.g. [<m>.s]
                            self.__unique_prefix_unit__(compound_unit_list[j][1],\
                                                      compound_unit_list[j+1][1])
                            
                        else:
                            #last is a prefix and unit
                            UnitProduct=self.__right_prefix_unit_product__(compound_unit_list[j][1],compound_unit_list[j+1][1],UnitProduct)
                            
                        
                        #move to the next and end
                        j+=2
                        
            elif current == "unit":
                compoundUnit += compound_unit_list[j][2]
                PID += compound_unit_list[j][1]

                if j + 1 < len(compound_unit_list) and compound_unit_list[j + 1][0] == "exponent":
                    
                    compoundUnit += compound_unit_list[j + 1][2]
                    PID += compound_unit_list[j + 1][2]
                    
                    if j + 2 < len(compound_unit_list):
                        if(j==0):
                            #the first unit + exponent
                            UnitProduct=self.__left_unit_exponent_product__(compound_unit_list[j][1],compound_unit_list[j+1][2])
                            #is the first of the elements but not the last 
                        
                        else:
                            
                            UnitProduct=self.__right_unit_exponent_product__(compound_unit_list[j][1],compound_unit_list[j+1][2],UnitProduct)
                            UnitProduct=self.__combine_product__(UnitProduct)
                            
                        j += 2
                        compoundUnit+='.'
                        PID+='.'
                    
                    else:
                        if(j==0):
                            #If it is only the unit and the exponent a special element will be displayed
                            self.__unique_unit_exponent__(compound_unit_list[j][1],compound_unit_list[j+1][2])
                            
                        else:
                            UnitProduct=self.__right_unit_exponent_product__(compound_unit_list[j][1],compound_unit_list[j+1][2],UnitProduct)
                            
                        j += 2    
                elif(j + 1 < len(compound_unit_list)):
                        
                        if(j==0):
                            #is the first of the elements but not the last                            
                            UnitProduct=self.__left_unit_product__(compound_unit_list[j][1])
                        else:
                            #Is not the first of the elements and also not the last 
                            UnitProduct=self.__right_unit_product__(compound_unit_list[j][1],UnitProduct)
                            UnitProduct=self.__combine_product__(UnitProduct)
                            
                        j+=1
                        compoundUnit+='.'
                        PID+='.'
                        
                elif(j==0):
                    #Only the unit has a special treatment
                    self.__unique_unit__(compound_unit_list[j][2],compound_unit_list[j][1])
                    j+=1
                
                elif(j>0):
                    #The last of the element, so to the Node UnitProduct I will add the right element
                    UnitProduct=self.__right_unit_product__(compound_unit_list[j][1],UnitProduct)
                    
                    j+=1
            
            elif current == "exponent":
                self.output_human_message = f"Before any exponent (e.g. '{list[j][1]}'), there should be a unit."
                
            else:
                self.output_human_message = "Error"
                

        self.output_compound_unit = compoundUnit
        self.output_pid = self.__prefixPID__ + PID
    
    def __unique_unit__(self,symbol,unit):
        #output: modified graph
        
        MeasurementUnit = BNode()  
        unit_uri = self.__UNITS__[unit]
        self.__g__.add((MeasurementUnit, RDF.type, self.__SI__.MeasurementUnit))
        self.__g__.add((MeasurementUnit, self.__SI__.hasSymbol, Literal(symbol)))
        self.__g__.add((MeasurementUnit, self.__OWL__.sameAs, unit_uri))
                
        return None    
        
    def __left_unit_product__(self,unitLeft):
        #output: modified graph

        UnitProduct = BNode()
        
        unit_uri_left = self.__SI__[unitLeft]
        
        self.__g__.add((UnitProduct, RDF.type, self.__SI__.UnitProduct))
        self.__g__.add((UnitProduct, self.__SI__.hasLeftUnitTerm, unit_uri_left))
        
        return UnitProduct
        
    def __right_unit_product__(self,unitRight,UnitProduct):
        #output: modified graph
        
        unit_uri_Right = self.__SI__[unitRight]
                
        self.__g__.add((UnitProduct, self.__SI__.hasRightUnitTerm, unit_uri_Right))
                
        return UnitProduct
    
    def __unique_unit_exponent__(self,unit,exponent):
        #output: modified graph
            
        UnitPower = BNode()  
        unit_uri = self.__UNITS__[unit]
        self.__g__.add((UnitPower, RDF.type, \
                        self.__SI__.UnitPower))        
        self.__g__.add((UnitPower, self.__SI__.hasNumericExponent, \
                        Literal(exponent, datatype=self.__XSD__.short)))
        self.__g__.add((UnitPower, \
                        self.__SI__.hasUnitBase, unit_uri))
                
        return UnitPower

    def __left_unit_exponent_product__(self,unit,exponent):
        #output: modified graph
        
        UnitPower=self.__unique_unit_exponent__(unit,exponent)
        
        UnitProduct = BNode()
        
        self.__g__.add((UnitProduct, RDF.type, self.__SI__.UnitProduct))
        self.__g__.add((UnitProduct, self.__SI__.hasLeftUnitTerm,UnitPower))
        
        return UnitProduct

    def __right_unit_exponent_product__(self,unit,exponent,UnitProduct):
        #output: modified graph
            
        UnitPower=self.__unique_unit_exponent__(unit,exponent)
        self.__g__.add((UnitProduct, self.__SI__.hasRightUnitTerm,UnitPower))
        return UnitProduct
            
    def __unique_prefix_unit__(self,prefix,unit):
        #output: modified graph
        
        PrefixedUnit = BNode()  
        
        unit_uri = self.__UNITS__[unit]
        
        prefix_uri = self.__PREFIXES__[prefix]
        
        self.__g__.add((PrefixedUnit, RDF.type, self.__SI__.PrefixedUnit))        
        self.__g__.add((PrefixedUnit, self.__SI__.hasNonPrefixedUnit, unit_uri))
        self.__g__.add((PrefixedUnit, self.__SI__.hasPrefix,prefix_uri))
        
        return PrefixedUnit

    def __left_prefix_unit_product__(self,prefix,unit):
        #output: modified graph
            
        PrefixedUnit=self.__unique_prefix_unit__(prefix,unit)
        UnitProduct = BNode()
        self.__g__.add((UnitProduct, RDF.type, self.__SI__.UnitProduct))
        self.__g__.add((UnitProduct, self.__SI__.hasLeftUnitTerm,PrefixedUnit))
        return UnitProduct
            
    def __right_prefix_unit_product__(self,prefix,unit,UnitProduct):
        #output: modified graph
            
        PrefixedUnit=self.__unique_prefix_unit__(prefix,unit)
        self.__g__.add((UnitProduct, self.__SI__.hasRightUnitTerm,PrefixedUnit))
        return UnitProduct

    def __unique_prefix_unit_exponent__(self,prefix,unit,exponent):
        #output: modified graph
        
        UnitPower = BNode()  
        
        unit_uri = self.__UNITS__[unit]
        
        self.__g__.add((UnitPower, RDF.type, self.__SI__.UnitPower))        
        self.__g__.add((UnitPower, \
                        self.__SI__.hasNumericExponent, \
                        Literal(exponent, datatype=self.__XSD__.short)
                        ))
        
        PrefixedUnit = BNode()
        
        self.__g__.add((UnitPower, self.__SI__.hasUnitBase, PrefixedUnit))
        
        prefix_uri = self.__PREFIXES__[prefix]
        
        self.__g__.add((PrefixedUnit, RDF.type, self.__SI__.PrefixedUnit))        
        self.__g__.add((PrefixedUnit, self.__SI__.hasNonPrefixedUnit, unit_uri))
        self.__g__.add((PrefixedUnit, self.__SI__.hasPrefix,prefix_uri))
                
        return UnitPower

    def __left_prefix_unit_exponent_product__(self,prefix,unit,exponent):
        #output: modified graph
        
        UnitPower=self.__unique_prefix_unit_exponent__(prefix,unit,exponent)
        
        UnitProduct = BNode()
        
        self.__g__.add((UnitProduct, RDF.type, self.__SI__.UnitProduct))
        self.__g__.add((UnitProduct, self.__SI__.hasLeftUnitTerm,UnitPower))
        
        
        return UnitProduct

    def __right_prefix_unit_exponent_product__(self,prefix,unit,exponent, UnitProduct):
        #output: modified graph
            
        UnitPower=self. __unique_prefix_unit_exponent__(prefix,unit,exponent)
        self.__g__.add((UnitProduct, RDF.type, self.__SI__.UnitProduct))
        self.__g__.add((UnitProduct, self.__SI__.hasRightUnitTerm,UnitPower))
               
        return UnitProduct
    
    def __combine_product__(self,InnerUnitProduct):
       #output: modified graph
            
        UnitProduct=BNode()
        
        self.__g__.add((UnitProduct, RDF.type, self.__SI__.UnitProduct))
        self.__g__.add((UnitProduct, self.__SI__.hasLeftUnitTerm, InnerUnitProduct))
        
        
        return UnitProduct

    #####
    #main function 5
    #####

    def __extract_unique_dsi_components__(self):
        #
        
        listas = self.__input_compound_unit_classified__
        
        listas_filtradas = []
        for lista in listas:
            if lista not in listas_filtradas and lista[0] != "exponent":
                listas_filtradas.append(lista)
        
        #print(listas_filtradas)
        
        self.__filteredCompoundUnitComponentsAsAList__ = [lista[1] for lista in listas_filtradas]
    
    #####
    #main function 6
    #####
    
    def __output_triplets__(self):
        
        ###
        #
        ###
        
        #input:
        #output:
        
        uniqueComponents=self.__filteredCompoundUnitComponentsAsAList__
        
        try:
            g_units = Graph()
            g_units.parse("SI_Digital_Framework/SI_Reference_Point/TTL/units.ttl", format="ttl")
            g_prefixes = Graph()
            g_prefixes.parse("SI_Digital_Framework/SI_Reference_Point/TTL/prefixes.ttl", format="ttl")
            
            for subject in uniqueComponents:

                query = f"""
                    SELECT ?predicate ?object WHERE {{
                        <http://si-digital-framework.org/SI/units/{subject}> ?predicate ?object .
                }}
                """

                resultados = g_units.query(query)
                for row in resultados:
                    string_predicate=str(row.predicate)
                    string_object=str(row.object)
                    predicate_modified = string_predicate.replace("http://www.w3.org/2004/02/skos/core#", "")
                    predicate_modified = predicate_modified.replace("http://si-digital-framework.org/SI#", "")
                    predicate_modified = predicate_modified.replace("http://www.w3.org/1999/02/22-rdf-syntax-ns#", "")
                    object_modified = string_object.replace("http://si-digital-framework.org/SI#", "")
                    object_modified = object_modified.replace("http://si-digital-framework.org/quantities/", "")
                    
                    
                    self.sirp_metadata_triples.append([subject,predicate_modified,object_modified])
            
            for subject in uniqueComponents:
                query = f"""
                    SELECT ?predicate ?object WHERE {{
                        <http://si-digital-framework.org/SI/prefixes/{subject}> ?predicate ?object .
                }}
                """
                
                resultados = g_prefixes.query(query)
                for row in resultados:
                    string_predicate=str(row.predicate)
                    string_object=str(row.object)
                    predicate_modified = string_predicate.replace("http://www.w3.org/2004/02/skos/core#", "")
                    predicate_modified = predicate_modified.replace("http://si-digital-framework.org/SI#", "")
                    predicate_modified = predicate_modified.replace("http://www.w3.org/1999/02/22-rdf-syntax-ns#", "")
                    object_modified = string_object.replace("http://si-digital-framework.org/SI#", "")
                    object_modified = object_modified.replace("http://si-digital-framework.org/quantities/", "")
                    object_modified = object_modified.replace("http://www.w3.org/2001/XMLSchema#", "")
                    object_modified = object_modified.replace("http://si-digital-framework.org/bodies/CGPM#", "")
                    self.sirp_metadata_triples.append([subject,predicate_modified,object_modified])    
        
        except:
            if(not self.output_human_message): self.output_human_message="Error in Sintax"
            return None

class dsiValidator:
    def run(self):
        """
        Offers the options to the user
        """
        
        
        #first_argument = 
        #print()
        if (len(sys.argv) == 2 and sys.argv[1] == "-h"):
            print("\n>>>>This is the HELP from transformation.py<<<< \n")
            print("a) for verbose output DSI unit validation, run: transformation -v \{unit\}")
            print("  e.g.: trasnformation -v \milli\metre\tothe{2}\n")
            print("b) for json output DSI unit validation, run: transformation -json \{unit\}")
            print("  e.g.: trasnformation -v \milli\metre\tothe{2}\n")            
        elif len(sys.argv) == 3:
            parameter = sys.argv[1]
            unit = sys.argv[2]
            if parameter == "-json":
                info=json_compound_unit_validation(unit)
                result=info.json_message_response()
                #print(json.dumps(result))
                pp = pprint.PrettyPrinter(depth=4)
                pp.pprint(result)
            elif parameter == "-v":
                info=verboseCompoundUnitValidation(unit)
                info.verbose_response()                
            elif parameter == "--version":
                print("Version=1.0v")
                print("Writtern by Diego Coppa and Daniel Hutzschenreuter")
            else:
                print("Wrong call of transformation.py please")
                print("for help, run: transformation -h")
        else:
            print("Wrong call of transformation.py please")
            print("for help, run: transformation -h")
            


if __name__ == "__main__":
    validator = dsiValidator()
    validator.run()