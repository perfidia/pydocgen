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
        
        if len(dictionary) > 0:
            if optional:
                begin_text = "["
                end_text = "]"
            else:
                begin_text = "{"
                end_text = "}"
            
            result += begin_text
            result += self.__generate_parameters_string(dictionary)            
            result += end_text
        
        return result
    
    def __generate_documentclass_declaration(self, document):
        result = "\\documentclass"
        
        optional_parameters = {}
        
        style = document.effective_style
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
            result = "\n\\usepackage%s{geometry}" %\
            self.__generate_parameters_list(options)
        
        return result
    
    def __generate_pagestyle_declaration(self, style):
        result = ""
        
        if (not style.has_key("page-numbering")) \
                    or (style["page-numbering"] == False):
            result = "\n\n\pagestyle{empty}"
        
        return result
    
    def __generate_language_package_reference(self, document_properties):
        result = ""
        
        if document_properties.has_key("lang"):
            lang = document_properties["lang"]
            if lang.startswith("pl"):
                result += "\n\usepackage{polski}"
        
        return result
    
    def __generate_font_packages_reference(self, document_style):
        result = ""
        
        if (document_style.has_key("font-name")):
            font_name = document_style['font-name'].strip().lower()
            
            if font_name == "times new roman":
                result += "\n\\usepackage{mathptmx}\n\\usepackage[T1]{fontenc}"
                
            if font_name == "arial":
                result += "\n\\usepackage[scaled]{uarial}\n" +\
                "\\renewcommand*\\familydefault{\\sfdefault}\n" +\
                "\\usepackage[T1]{fontenc}"
                
            if font_name == "computer modern":
                result += "\n\\usepackage[T1]{fontenc}"
                
            if font_name == "dejavu serif":
                result += "\n\usepackage{DejaVuSerif}\n" +\
                "\\usepackage[T1]{fontenc}"
        
        return result
    
    def __generate_enumitem_package_reference(self, document):
        result = ""
        
        if document.successor_isinstance(List):
            result += "\n\\usepackage{enumitem}"
        
        return result
    
    def generate_document(self, document):
        document.fill_parent_fields()
        
        result = ""
        
        result += self.__generate_documentclass_declaration(document) 
        result += "\n"
        result += "\n\\usepackage[utf8]{inputenc}"
        result += self.__generate_geometry_package_reference(\
                        document.effective_style)
        result += self.__generate_language_package_reference(
                    document.properties)
        result += self.__generate_font_packages_reference(\
                        document.effective_style)
        result += self.__generate_enumitem_package_reference(document)
        
        result += self.__generate_pagestyle_declaration(\
                        document.effective_style)
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
    
    def __get_list_level(self, lst):
        level = 0
        elem = lst
        while elem.parent is not None:
            elem = elem.parent
            if isinstance(elem, List):
                level += 1
                
        return level
    
    def __get_bullet_char_dict(self):
        bullet_char_dict = {}
        bullet_char_dict[BulletChar.ASTERISK] = r"$\ast$"
        bullet_char_dict[BulletChar.BULLET] = r"$\bullet$"
        bullet_char_dict[BulletChar.CDOT] = r"$\cdot$"
        bullet_char_dict[BulletChar.CIRCLE] = r"$\circ$"
        bullet_char_dict[BulletChar.DIAMOND] = r"$\diamond$"
        bullet_char_dict[BulletChar.MEDIUM_HYPHEN] = r"--"
        bullet_char_dict[BulletChar.LONG_HYPHEN] = r"---"
        bullet_char_dict['#'] = r"\#"
        bullet_char_dict['$'] = r"\$"
        bullet_char_dict['%'] = r"\%"
        bullet_char_dict['&'] = r"\&"
        bullet_char_dict['~'] = r"\textasciitilde"
        bullet_char_dict['_'] = r"\_"
        bullet_char_dict['^'] = r"\textasciicircum"
        bullet_char_dict['\\'] = r"\textbackslash"
        bullet_char_dict['{'] = r"\{"
        bullet_char_dict['}'] = r"\}"
        return bullet_char_dict
    
    def __get_bullet_command(self, lst):
        level = self.__get_list_level(lst)
        
        bullet_commands = ["labelitemi", "labelitemii", "labelitemii",\
                           "labelitemiv"]
        
        result = None
        if level < len(bullet_commands):
            result = bullet_commands[level]
            
        return result
    
    def generate_list(self, lst):
        result = ""
        
        if lst.effective_style.has_key('list-style'):
            style = lst.effective_style['list-style']
        else:
            style = ListStyle.BULLET
            
        environment = ""
        if style == ListStyle.BULLET:
            environment = "itemize"
        elif style == ListStyle.NUMBER:
            environment = "enumerate"
            
        if len(environment) > 0:
            parameters = {}
            
            result += "\n"
            
            #handling the "item-spacing" style
            if lst.effective_style.has_key("item-spacing"):
                parameters['itemsep'] = "%dpt" %\
                        lst.effective_style['item-spacing']
                parameters['parsep'] = "0pt"
                
            #handling the "item-indent" style
            if lst.effective_style.has_key("item-indent"):
                parameters['itemindent'] = "%dpt" %\
                        lst.effective_style['item-indent']
                
            #handling the "margin-top" style
            if lst.effective_style.has_key("margin-top"):
                margin_top = max(lst.effective_style['margin-top'], 0)
                parameters['topsep'] = "%dpt" % margin_top
            else:
                margin_top = 0
                        
            #handling the "margin-bottom" style
            margin_correction = 0
            if lst.effective_style.has_key("margin-bottom"):
                margin_bottom = max(lst.effective_style['margin-bottom'], 0)
                margin_correction = margin_bottom - margin_top
                
            #handling the "margin-left" style
            if lst.effective_style.has_key("margin-left"):
                parameters['leftmargin'] = "%dpt" %\
                        lst.effective_style['margin-left']
                
            #handling the "margin-right" style
            if lst.effective_style.has_key("margin-right"):
                parameters['rightmargin'] = "%dpt" %\
                        lst.effective_style['margin-right']
            
            #handling the "bullet-char" style
            if lst.effective_style.has_key("bullet-char"):
                bullet_char_command = self.__get_bullet_command(lst)
                
                if bullet_char_command is not None:
                    bullet_char = None
                    
                    bullet_char_dict = self.__get_bullet_char_dict()
                    bullet_char_style_val = lst.effective_style['bullet-char']
                    
                    if bullet_char_dict.has_key(bullet_char_style_val):
                        bullet_char =  bullet_char_dict[bullet_char_style_val]
                    elif isinstance(bullet_char_style_val, str):
                        bullet_char = bullet_char_style_val
                        
                    if (bullet_char is not None):
                        result += "\n\\renewcommand{%s}{%s}" %\
                                ("\\" + bullet_char_command, bullet_char)
   
            result += "\n\\begin{%s}%s" % (environment,\
                        self.__generate_parameters_list(parameters))

            for element in lst.content:
                result += "\n\t\\item %s" % element.generate()
            
            result += "\n\\end{%s}" % environment
            
            if margin_correction != 0:
                    result += "\n\\vspace{%dpt}" % margin_correction
        
        return result
    
    def generate_image(self, image):
        return ""
    
    def generate_table(self, table):
        return ""