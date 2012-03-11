# -*- coding: utf-8 -*-

from pydocgen.model import List, BulletChar, ListStyle, Image, Alignment,\
                            FontEffect
from pydocgen.builders.common import Builder


# some useful functions

def _generate_parameter_string(dictionary, key):
    result = ""
    
    result += str(key)
    if (dictionary[key] is not None):
        result += "=" + str(dictionary[key])
    
    return result

def _generate_parameters_string(parameters):
    result = ""
    
    keys = parameters.keys()
    
    if len(keys) > 0:
        result += _generate_parameter_string(parameters, keys[0])
        
    if len(keys) > 1:
        for i in xrange(1, len(keys)):
            result += "," \
                    + _generate_parameter_string(parameters, keys[i])
    
    return result

def _generate_parameters_list(dictionary, optional = True):
    result = ""
    
    if len(dictionary) > 0:
        if optional:
            begin_text = "["
            end_text = "]"
        else:
            begin_text = "{"
            end_text = "}"
        
        result += begin_text
        result += _generate_parameters_string(dictionary)            
        result += end_text
    
    return result

def _generate_rgb_from_hex(color):
    result = {}
    result['r'] = _hex2dec(color[1]+color[2])
    result['g'] = _hex2dec(color[3]+color[4])
    result['b'] = _hex2dec(color[5]+color[6])
    return result

def _hex2dec(s):
    n = int(s, 16)
    result = n / 255.00
    return str(result)[:3]
    
def _get_leading(number):
    number = int(number *1.2)
    return str(number)
    
def _get_font_family(font_name):
    if font_name ==  "Times New Roman":
        return r"ptm"
    if font_name == "Arial":
        return r"phv"
    if font_name == "Computer Modern":
        return r"cmr"
    if font_name == "DejaVu Serif":
        return r"dejavu"
        
def _append_content_code(result, element):
        for element in element.content:
            result += element.generate()
        return result 


# main builder

class LatexBuilder(Builder):
    def __init__(self):
        super(LatexBuilder, self).__init__()
        self.__image_builder = _LatexImageBuilder()
        self.__list_builder = _LatexListBuilder()
        self.__document_builder = _LatexDocumentBuilder()
    
    def generate_document(self, document):
        document.fill_parent_fields()
        self.__list_builder.reset()
        
        return self.__document_builder.generate(document)
    
    def generate_paragraph(self, paragraph):
        result = "\n\n"
                
        result = _append_content_code(result, paragraph)
        
        return result
    
    def generate_span(self, span):
        
        result = ""
        counter = 0;
        font_changed = False
        if span.effective_style.has_key('font-name'):
            font_name = span.effective_style['font-name']
            font_changed = True
            counter += 1
            result += r"{"
            result += r"\fontfamily {" + _get_font_family(font_name) + r"} "
        if span.effective_style.has_key('font-size'):
            font_size = span.effective_style['font-size'] 
            if not font_changed:
                result += r"{"
                counter += 1
            result += r"\fontsize {" + str(font_size) + "}{" + _get_leading(font_size) + "}"    
            font_changed = True
        if font_changed:
            result += r"\selectfont "
        if span.effective_style.has_key('background-color'):
            background_color = _generate_rgb_from_hex(span.effective_style['background-color'])
            counter += 1
            result += r"\colorbox [rgb] {";
            result += background_color['r'] + ", "
            result += background_color['g'] + ", "
            result += background_color['b'] + "} {"
            
        if span.effective_style.has_key('color'):
            font_color = _generate_rgb_from_hex(span.effective_style['color']) 
            counter += 1
            result += r"\color [rgb] {";
            result += font_color['r'] + r", "
            result += font_color['g'] + r", "
            result += font_color['b'] + r"} {"
        if span.effective_style.has_key('font-effects'):
            font_effects = span.effective_style['font-effects']
            if font_effects == FontEffect.BOLD:
                counter += 1
                result += r"\textbf {"
            if font_effects == FontEffect.ITALIC:
                counter += 1
                result += r"\textit{"
            if font_effects == FontEffect.UNDERLINE:
                counter += 1
                result += r"\underline{"


        result += span.text
        for _ in xrange(0, counter):
            result += r"}"
        return result

    
    def generate_header(self, header):
        result = "\n\n\section{"
        
        result = _append_content_code(result, header)
        
        result += "}"
        
        return result
    
    def generate_list(self, lst):
        return self.__list_builder.generate(lst)
    
    def generate_image(self, image):
        return self.__image_builder.generate(image)
    
    def generate_table(self, table):
        return ""


#helper builders

class _LatexImageBuilder(object):
    def generate(self, image):
        result = ""
        
        parameters = {}
        
        pre = ""
        post = ""
        tab_indent_level = 1
        margins_before = ""
        margins_after = ""
        hspace_after = ""
        caption = ""
        captionsetup_parameters = {}
        captionsetup = ""
        
        # handling the "width" style 
        if image.is_style_element_set("width"):
            parameters['width'] = "%.2fmm" % image.effective_style['width']
            
        # handling the "height" style 
        if image.is_style_element_set("height"):
            parameters['height'] = "%.2fmm" % image.effective_style['height']
        
        # handling the "alignment" style 
        if image.is_style_element_set("alignment"):
            align_env = None 
            if image.effective_style['alignment'] == Alignment.LEFT\
                    or image.effective_style['alignment'] == Alignment.JUSTIFY:
                align_env = "flushleft"
                captionsetup_parameters['justification'] = "raggedright"
            elif image.effective_style['alignment'] == Alignment.CENTER:
                align_env = "center"
                captionsetup_parameters['justification'] = "centering"
            elif image.effective_style['alignment'] == Alignment.RIGHT:
                align_env = "flushright"
                captionsetup_parameters['justification'] = "raggedleft"
            
            if align_env is not None:
                tabs = "\t" * tab_indent_level
                pre += "\n%s\\begin{%s}" % (tabs, align_env)
                post = ("\n%s\\end{%s}" % (tabs, align_env)) + post
                tab_indent_level += 1
                captionsetup_parameters['singlelinecheck'] = "false"
        
        # handling the margins
        if image.is_style_element_set("margin-top")\
                    or image.is_style_element_set("margin-bottom")\
                    or image.is_style_element_set("margin-left")\
                    or image.is_style_element_set("margin-right"):
            margin_top = 0
            margin_bottom = 0
            margin_left = 0
            margin_right = 0
            
            if image.is_style_element_set("margin-top"):
                margin_top = image.effective_style['margin-top']
                
            if image.is_style_element_set("margin-bottom"):
                margin_bottom = image.effective_style['margin-bottom']
                
            if image.is_style_element_set("margin-left"):
                margin_left = image.effective_style['margin-left']
                
            if image.is_style_element_set("margin-right"):
                margin_right = image.effective_style['margin-right']
                
            if margin_top != 0:
                margins_before += "\\vspace*{%.2fpt}" % margin_top
            if margin_left != 0:
                margins_before += "\\hspace*{%.2fpt}" % margin_left
            if margin_right != 0:
                hspace_after += "\\hspace*{%.2fpt}" % margin_right
            if margin_bottom != 0:
                margins_after += "\\vspace*{%.2fpt}" % margin_bottom
                
            if (margin_left != 0) or (margin_right != 0):
                captionsetup_parameters['margin'] = "{%.2fpt,%.2fpt}" %\
                                (margin_left, margin_right)
                captionsetup_parameters['oneside'] = None
            
        if len(margins_before) > 0:
            margins_before += "\n" + ("\t" * tab_indent_level)
        if len(hspace_after) > 0:
            hspace_after = "\n" + ("\t" * tab_indent_level) + hspace_after
        if len(margins_after) > 0:
            margins_after = "\n" + ("\t" * tab_indent_level) + margins_after
        
        # putting the caption
        if len(image.caption) > 0:
            caption_content = ""
            for span in image.caption:
                caption_content += span.generate()
                
            caption = "\n%s\caption{%s}" % ("\t" * tab_indent_level,\
                                                         caption_content)
            captionsetup = "\n%s\\captionsetup%s" %\
                    (("\t" * (tab_indent_level - 1)),\
                    _generate_parameters_list(captionsetup_parameters, False))
            
        result += "\n\n"
        result += "\\begin{figure}[ht!]"
        result += captionsetup
        result += pre
        result += "\n%s%s\\noindent\includegraphics%s{%s}%s%s%s" %\
                    ("\t" * tab_indent_level,
                     margins_before,
                     _generate_parameters_list(parameters),
                     image.path,
                     hspace_after,
                     caption,
                     margins_after)
        result += post
        result += "\n\\end{figure}"
        
        return result

class _LatexDocumentBuilder(object):
    def __generate_package_reference(self, package_name, parameter_dict = {}):
        parameters = _generate_parameters_list(parameter_dict)
        return "\n\\usepackage%s{%s}" % (parameters, package_name)
    
    def __generate_documentclass_declaration(self, document):
        result = "\\documentclass"
        
        optional_parameters = {}
        
        style = document.effective_style
        prop = document.properties
        
        if (style.has_key("font-size")):
            optional_parameters[str(style["font-size"]) + "pt"] = None
        
        if (not prop.has_key("lang")) or (not prop['lang'].startswith('en-US')):
            optional_parameters["a4paper"] = None
        
        result += _generate_parameters_list(optional_parameters)
            
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
            _generate_parameters_list(options)
        
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
                result += self.__generate_package_reference("polski")
        
        return result
    
    def __generate_font_packages_reference(self, document_style):
        result = ""
        
        if (document_style.has_key("font-name")):
            font_name = document_style['font-name'].strip().lower()
            
            if font_name == "times new roman":
                result += self.__generate_package_reference("mathptmx")
                result += self.__generate_package_reference(\
                                                "fontenc", {"T1": None})
                
            if font_name == "arial":
                result += self.__generate_package_reference(\
                                                "uarial", {"scaled": None})
                result += "\n\\renewcommand*\\familydefault{\\sfdefault}\n"
                result += self.__generate_package_reference(\
                                                "fontenc", {"T1": None})
                
            if font_name == "computer modern":
                result += self.__generate_package_reference(\
                                                "fontenc", {"T1": None})
                
            if font_name == "dejavu serif":
                result += self.__generate_package_reference("DejaVuSerif")
                result += self.__generate_package_reference(\
                                                "fontenc", {"T1": None})
        
        return result
    
    def __generate_enumitem_package_reference(self, document):
        result = ""
        
        if document.successor_isinstance(List):
            result += self.__generate_package_reference("enumitem")
        
        return result
    
    def __generate_graphicx_package_reference(self, document):
        result = ""
        
        if document.successor_isinstance(Image):
            result += self.__generate_package_reference("graphicx")
            result += self.__generate_package_reference("caption")
        
        return result
    
    def generate(self, document):     
        result = ""
        
        result += self.__generate_documentclass_declaration(document) 
        result += "\n"
        result += self.__generate_package_reference(\
                                                "inputenc", {"utf8": None})
        result += self.__generate_geometry_package_reference(\
                        document.effective_style)
        result += self.__generate_language_package_reference(
                    document.properties)
        result += self.__generate_font_packages_reference(\
                        document.effective_style)
        result += self.__generate_enumitem_package_reference(document)
        result += self.__generate_graphicx_package_reference(document)
        result += "\n\\usepackage{color}"
        result += self.__generate_pagestyle_declaration(\
                        document.effective_style)
        
        result += "\n\n\\begin{document}"
        
        content = ""
        content = _append_content_code(content, document)
        
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


class _LatexListBuilder(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.__default_bullet_chars = [True, True, True, True]
    
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
        bullet_char_dict[BulletChar.MEDIUM_HYPHEN] = r"\textbf{--}"
        bullet_char_dict[BulletChar.LONG_HYPHEN] = r"\textbf{---}"
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
    
    def __get_bullet_char(self, bullet_char_style_val):
        bullet_char = None
        
        bullet_char_dict = self.__get_bullet_char_dict()
        if bullet_char_dict.has_key(bullet_char_style_val):
            bullet_char =  bullet_char_dict[bullet_char_style_val]
        elif isinstance(bullet_char_style_val, str):
            bullet_char = bullet_char_style_val
            
        return bullet_char
    
    def __get_bullet_command(self, lst):
        level = self.__get_list_level(lst)
        
        bullet_commands = ["labelitemi", "labelitemii", "labelitemiii",\
                           "labelitemiv"]
        
        result = None
        if level < len(bullet_commands):
            result = bullet_commands[level]
            
        return result
    
    def __generate_bullet_char_declaration(self, command, char, level):
        return "\n%s\\renewcommand{%s}{%s}" % ("\t" * level,\
                                "\\" + command, char)
    
    def __generate_default_bullet_char_declaration(self, lst):
        default_bullet_chars = [BulletChar.BULLET, BulletChar.MEDIUM_HYPHEN,\
                                BulletChar.ASTERISK, BulletChar.CDOT]
        
        level = self.__get_list_level(lst)
        
        return self.__generate_bullet_char_declaration(\
                    self.__get_bullet_command(lst),\
                    self.__get_bullet_char(default_bullet_chars[level]), level)
    
    def generate(self, lst):
        result = ""
        
        if lst.is_style_element_set('list-style'):
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
            
            level = self.__get_list_level(lst)
            
            if level == 0:
                result += "\n"
            
            #handling the "item-spacing" style
            if lst.is_style_element_set("item-spacing"):
                parameters['itemsep'] = "%dpt" %\
                        lst.effective_style['item-spacing']
                parameters['parsep'] = "0pt"
                
            #handling the "item-indent" style
            if lst.is_style_element_set("item-indent"):
                parameters['itemindent'] = "%dpt" %\
                        lst.effective_style['item-indent']
                
            #handling the "margin-top" style
            if lst.is_style_element_set("margin-top"):
                margin_top = max(lst.effective_style['margin-top'], 0)
                parameters['topsep'] = "%dpt" % margin_top
            else:
                margin_top = 0
                        
            #handling the "margin-bottom" style
            margin_correction = 0
            if lst.is_style_element_set("margin-bottom"):
                margin_bottom = max(lst.effective_style['margin-bottom'], 0)
                margin_correction = margin_bottom - margin_top
                
            #handling the "margin-left" style
            if lst.is_style_element_set("margin-left"):
                parameters['leftmargin'] = "%dpt" %\
                        lst.effective_style['margin-left']
                
            #handling the "margin-right" style
            if lst.is_style_element_set("margin-right"):
                parameters['rightmargin'] = "%dpt" %\
                        lst.effective_style['margin-right']
            
            #handling the "bullet-char" style
            if lst.is_style_element_set("bullet-char"):
                bullet_char_command = self.__get_bullet_command(lst)
                
                if bullet_char_command is not None:                    
                    bullet_char = self.__get_bullet_char(\
                                        lst.effective_style['bullet-char'])
                        
                    if (bullet_char is not None):
                        self.__default_bullet_chars[level] = False
                        result += self.__generate_bullet_char_declaration(\
                                        bullet_char_command, bullet_char, level)
                        
            elif not self.__default_bullet_chars[level]:
                result += self.__generate_default_bullet_char_declaration(lst)
                self.__default_bullet_chars[level] = True
   
            result += "\n%s\\begin{%s}%s" % ("\t" * level, environment,\
                        _generate_parameters_list(parameters))

            for element in lst.content:
                item = ""
                newline = ""
                if not isinstance(element, List):
                    item = "\\item"
                    newline = "\n"
                result += "%s\t%s%s %s" % (newline, "\t" * level, item,\
                            element.generate())
            
            result += "\n%s\\end{%s}" % ("\t" * level, environment)
            
            if margin_correction != 0:
                    result += "\n%s\\vspace{%dpt}" % ("\t" * level,\
                            margin_correction)
        
        return result
    
