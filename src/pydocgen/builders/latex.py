# -*- coding: utf-8 -*-

from pydocgen.model import *
from pydocgen.builders.common import Builder

class LatexBuilder(Builder):
    def __init__(self):
        super(LatexBuilder, self).__init__()
        
    def __append_content_code(self, result, element):
        for element in element.content:
            result += element.generate()
        return result
    
    def __generate_parameter_string(self, dictionary, key):
        result = ""
        
        result += str(key)
        if (dictionary[key] is not None):
            result += "=" + str(dictionary[key])
        
        return result
    
    def __generate_parameters_string(self, parameters):
        result = ""
        
        keys = parameters.keys()
        
        if len(keys) > 0:
            result += self.__generate_parameter_string(parameters, keys[0])
            
        if len(keys) > 1:
            for i in xrange(1, len(keys)):
                result += "," \
                        + self.__generate_parameter_string(parameters, keys[i])
        
        return result
    
    def __generate_parameters_list(self, dictionary, optional = True):
        result = ""
        
        if optional:
            begin_text = "["
            end_text = "]"
        else:
            begin_text = "{"
            end_text = "}"
        
        if (len(dictionary.keys()) > 0):
            result += begin_text
            result += self.__generate_parameters_string(dictionary)            
            result += end_text
        
        return result
    
    def __generate_documentclass_declaration(self, document):
        result = "\\documentclass"
        
        optional_parameters = {}
        
        style = document.style
        prop = document.properties
        
        if (style.has_key("font-size")):
            optional_parameters[str(style["font-size"]) + "pt"] = None
        
        if (not prop.has_key("lang")) or (not prop['lang'].startswith('en-US')):
            optional_parameters["a4paper"] = None
        
        result += self.__generate_parameters_list(optional_parameters)
            
        result += "{article}"
        
        return result
    
    def __generate_geometry_package_reference(self, style):
        result = ""
        
        options = {}
        
        if (style.has_key("page-width")):
            options["paperwidth"] = str(style["page-width"]) + "mm"
            
        if (style.has_key("page-height")):
            options["paperheight"] = str(style["page-height"]) + "mm"
            
        if (style.has_key("margin-top")):
            options["top"] = str(style["margin-top"]) + "mm"
            
        if (style.has_key("margin-bottom")):
            options["bottom"] = str(style["margin-bottom"]) + "mm"
            
        if (style.has_key("margin-left")):
            options["asymmetric"] = None
            options["left"] = str(style["margin-left"]) + "mm"
            
        if (style.has_key("margin-right")):
            if not options.has_key("asymmetric"):
                options["asymmetric"] = None
            options["right"] = str(style["margin-right"]) + "mm"
            
        if (style.has_key("page-numbering")) \
                    and (style["page-numbering"] == True):
            options["includefoot"] = None
        
        if (len(options) > 0):
            result = "\n\\usepackage"
            result += self.__generate_parameters_list(options)
            result += "{geometry}"
        
        return result
    
    def __generate_pagestyle_declaration(self, style):
        result = ""
        
        if (not style.has_key("page-numbering")) \
                    or (style["page-numbering"] == False):
            result = "\n\n\pagestyle{empty}"
        
        return result
    
    def __generate_language_package_reference(self, document_properties):
        result = ""
        
        if (document_properties.has_key("lang")):
            lang = document_properties["lang"]
            if lang.startswith("pl"):
                result += "\n\usepackage{polski}"
        
        return result
    
    def generate_document(self, document):
        document.fill_parent_fields()
        
        result = ""
        
        result += self.__generate_documentclass_declaration(document) 
        result += "\n"
        result += self.__generate_geometry_package_reference(document.style)
        result += self.__generate_language_package_reference(
                    document.properties)
        
        result += "\n\usepackage[utf8]{inputenc}"
        
        result += self.__generate_pagestyle_declaration(document.style)
        result += "\n\n\\begin{document}"
        
        content = ""
        content = self.__append_content_code(content, document)
            
        if len(content) == 0:
            result += "\n\n\\begin{verbatim}\\end{verbatim}"
        else:
            result += content
        
        result += "\n\n\end{document}"
        
        return result
    
    def generate_paragraph(self, paragraph):
        result = "\n\n"
        
        result = self.__append_content_code(result, paragraph)
        
        return result
    
    def generate_span(self, span):
        result = ""
        result += span.text
        
        return result
    
    def generate_header(self, header):
        result = "\n\n\section{"
        
        result = self.__append_content_code(result, header)
        
        result += "}"
        
        return result
    
    def generate_list(self, lst):
        return ""
    
    def generate_image(self, image):
        return ""
    
    def generate_table(self, table):
        return ""