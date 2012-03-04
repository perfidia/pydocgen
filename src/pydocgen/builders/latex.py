# -*- coding: utf-8 -*-

from pydocgen.model import *
from pydocgen.builders.common import Builder

class LatexBuilder(Builder):
    def __init__(self):
        pass
    
    def __generate_documentclass_declaration(self, style):
        result = "\\documentclass"
        
        if (style.has_key("font-size")):
            result += "[" + str(style["font-size"]) + "pt]"
            
        result += "{article}"
        
        return result
    
    def __generate_geometry_package_reference(self, style):
        result = "\n\n\\usepackage["
        options = []
        
        if (style.has_key("page-width")):
            option = "paperwidth="
            option += str(style["page-width"])
            option += "mm"
            options.append(option)
            
        if (style.has_key("page-height")):
            option = "paperheight="
            option += str(style["page-height"])
            option += "mm"
            options.append(option)
            
        if (style.has_key("margin-top")):
            option = "top="
            option += str(style["margin-top"])
            option += "mm"
            options.append(option)
            
        if (style.has_key("margin-bottom")):
            option = "bottom="
            option += str(style["margin-bottom"])
            option += "mm"
            options.append(option)
            
        if (style.has_key("margin-left")):
            options.append("asymmetric")
            option = "left="
            option += str(style["margin-left"])
            option += "mm"
            options.append(option)
            
        if (style.has_key("margin-right")):
            if not "asymmetric" in options:
                options.append("asymmetric")
            option = "right="
            option += str(style["margin-right"])
            option += "mm"
            options.append(option)
            
        if (style.has_key("page-numbering")) and (style["page-numbering"] == True):
            options.append("includefoot")
            
        if len(options) > 0:
            result += options[0]
        for i in xrange(1, len(options)):
            result += "," + options[i]
            
        result += "]{geometry}"
        
        return result
    
    def __generate_pagestyle_declaration(self, style):
        result = ""
        
        if (not style.has_key("page-numbering")) or (style["page-numbering"] == False):
            result = "\n\n\pagestyle{empty}"
        
        return result
    
    def generate_document(self, document):
        document.fill_parent_fields()
        
        result = ""
        
        result += self.__generate_documentclass_declaration(document.style) 
        result += self.__generate_geometry_package_reference(document.style)
        result += self.__generate_pagestyle_declaration(document.style)
        result += "\n\n\\begin{document}"
        
        content = ""
        
        for element in document.content:
            content += element.generate()
            
        if len(content) == 0:
            result += "\n\n\\begin{verbatim}\\end{verbatim}"
        else:
            result += content
        
        result += "\n\n\end{document}"
        
        return result
    
    def generate_paragraph(self, paragraph):
        return ""
    
    def generate_span(self, span):
        return ""
    
    def generate_header(self, header):
        return ""
    
    def generate_list(self, lst):
        return ""