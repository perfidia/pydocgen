# -*- coding: utf-8 -*-

from pydocgen.model import List, BulletCharProperty, ListStyleProperty, Image, AlignmentProperty,\
                            FontEffectProperty, Span, PageOrientationProperty
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


        
def _append_content_code(result, element):
        for element in element.content:
            result += element.generate()
            
        return result 

def _generate_rgb_from_hex(color):
    result = {}
    result['r'] = str(_hex2dec(color[1]+color[2]))
    result['g'] = str(_hex2dec(color[3]+color[4]))
    result['b'] = str(_hex2dec(color[5]+color[6]))

    return result

def _hex2dec(s):
    return int(s, 16)   

    
def _compare_rgb_colors(color1, color2):
    if color1['r'] != color2['r']:
        return False
    if color1['g'] != color2['g']:
        return False
    if color1['b'] != color2['b']:
        return False
    return True
# main builder

class LatexBuilder(Builder):
    def __init__(self):
        super(LatexBuilder, self).__init__()
        self.__float_generator = _FloatGenerator(self)
        self.__span_builder = _LatexSpanBuilder()
        self.__paragraph_builder = _LatexParagraphBuilder()
        self.__header_builder = _LatexHeaderBuilder()
        self.__image_builder = _LatexImageBuilder(self.__float_generator)
        self.__list_builder = _LatexListBuilder()
        self.__document_builder = _LatexDocumentBuilder(self.__float_generator)
        
    
    def generate_document(self, document):
        self.__list_builder.reset()
        
        return self.__document_builder.generate(document)
    
    def generate_paragraph(self, paragraph):
        return self.__paragraph_builder.generate(paragraph)

    
    def generate_span(self, span):
        return self.__span_builder.generate(span)
    
    def generate_header(self, header):
        result = "\n\n\section{"
        
        result = _append_content_code(result, header)
        
        result += "}"
        
        return self.__header_builder.generate(header)
    
    def generate_list(self, lst):
        return self.__list_builder.generate(lst)
    
    def generate_image(self, image):
        return self.__image_builder.generate(image)
    
    def generate_table(self, table):
        return ""


#helper builders

class _LatexHeaderBuilder(object):
    
    def generate(self, header):
        result = "\n\n"
        level = 0;
        number = ""
    
        if header.sequence is not None:
            level = header.sequence.get_level()
            if level == 0:
                result += r"\section*{"                
            if level == 1:
                result += r"\subsection*{"
            if level == 2:
                result += r"\subsubsection*{"
            if level == 3:
                result += r"\paragraph*{"
            if level > 3:
                result += r"\subparagraph*{"
            if header.is_style_element_set("header-numbered"):
                if header.effective_style['header-numbered']:

                    if header.is_style_element_set("seq-number-sep"):
                        number = header.sequence.to_str(header.effective_style['seq-number-sep'])
                        result += number
                        result += " \\hspace*{5pt} "
                    else:
                        numbers = header.sequence.get_numbers()
                        result = "\n\n"
                
                        if level == 0:
                            result += r"\setcounter{section}{" + numbers[0]+ r"}"
                            result += '\n'
                            result += r"\section{"                
                        if level == 1:
                            result += r"\setcounter{section}{" + numbers[1]+ r"}"
                            result += '\n'
                            result += r"\setcounter{subsection}{" + numbers[0]+ r"}"
                            result += '\n'
                            result += r"\subsection{"
                        if level == 2:
                            result += r"\setcounter{section}{" + numbers[2]+ r"}"
                            result += '\n'
                            result += r"\setcounter{subsection}{" + numbers[1]+ r"}"
                            result += '\n'
                            result += r"\setcounter{subsubsection}{" + numbers[0]+ r"}"
                            result += '\n'
                            result += r"\subsubsection{"
                        if level == 3:
                            result += r"\setcounter{section}{" + numbers[3]+ r"}"
                            result += '\n'
                            result += r"\setcounter{subsection}{" + numbers[2]+ r"}"
                            result += '\n'
                            result += r"\setcounter{subsubsection}{" + numbers[1]+ r"}"
                            result += '\n'
                            result += r"\setcounter{paragraph}{" + numbers[0]+ r"}"
                            result += '\n'
                            result += r"\paragraph{"
                        if level > 3:
                            result += r"\setcounter{section}{" + numbers[4]+ r"}"
                            result += '\n'
                            result += r"\setcounter{subsection}{" + numbers[3]+ r"}"
                            result += '\n'
                            result += r"\setcounter{subsubsection}{" + numbers[2]+ r"}"
                            result += '\n'
                            result += r"\setcounter{paragraph}{" + numbers[1]+ r"}"
                            result += '\n'
                            result += r"\setcounter{subparagraph}{" + numbers[0]+ r"}"
                            result += '\n'
                            result += r"\subparagraph{"
 
        else:    
            result += r"\section*{"
  
        
        
        for element in header.content:
            result += element.generate()   
        
        result += r"}"
        
        if header.sequence is not None:
            if header.is_style_element_set("header-numbered"):
                if header.effective_style['header-numbered']:
                    header.sequence.advance()
            else:    
                header.sequence.advance()
            
        return result
    

class _LatexParagraphBuilder(object):
    __last_indent = -1
    def generate(self, paragraph):
        result = "\n\n"
        alignment = ""
        margin_top = 0
        margin_bottom = 0
        margin_left = 0
        margin_right = 0
        text_indent = 0
        justification_before = ""
        justification_after = ""
        begin_margin = ""
        end_margin = ""
        margins_before = ""
        margins_after = ""
        colorbox = ""
        counter = 0
        
        if paragraph.effective_style.has_key('alignment'):
            alignment = paragraph.effective_style['alignment']
        if paragraph.effective_style.has_key('margin-top'):
            margin_top = paragraph.effective_style['margin-top']
        if paragraph.effective_style.has_key('margin-bottom'):
            margin_bottom = paragraph.effective_style['margin-bottom']
        if paragraph.effective_style.has_key('margin-left'):
            margin_left = paragraph.effective_style['margin-left']
        if paragraph.effective_style.has_key('margin-right'):
            margin_right = paragraph.effective_style['margin-right']
        if paragraph.effective_style.has_key('text-indent'):
            text_indent = paragraph.effective_style['text-indent']
            
        if alignment != "":
            if alignment == AlignmentProperty.LEFT:
                justification_before += r"\begin{flushleft}" + "\n "
                justification_after += "\n" + r"\end{flushleft}" + "\n "
            if alignment == AlignmentProperty.RIGHT:
                justification_before += r"\begin{flushright}" + "\n "
                justification_after += "\n" + r"\end{flushright}" + "\n"
            if alignment == AlignmentProperty.CENTER :
                justification_before += r"\begin{center}" + "\n"
                justification_after += "\n" + r"\end{center}" + "\n"
        if  self.__last_indent != text_indent:
            result += r"\setlength{\parindent}{" + str(text_indent) + r"pt}"
            self.__last_indent = text_indent  
            
        if margin_top != 0:
            margins_before += "\\vspace*{%.2fpt}" % margin_top
        margin_sides = margin_left + margin_right
        begin_margin += r"{"
        if margin_sides != 0:
            begin_margin += r"\addtolength{\textwidth}{-"
            begin_margin += "%.2fpt} "  % margin_sides
        begin_margin += r"\begingroup "
            
        end_margin += r"\par"
        end_margin += "\n"
        end_margin += r"\endgroup} "
        if margin_left != 0:
            begin_margin += "\leftskip "
            begin_margin += "%.2fpt " % margin_left
        begin_margin += r" \noindent " 
        if margin_bottom != 0:
            margins_after += "\\vspace*{%.2fpt}" % margin_bottom
            
        if paragraph.effective_style.has_key('background-color'):
            background_color = _generate_rgb_from_hex(paragraph.effective_style['background-color'])
            counter += 1
            colorbox += r"{\colorbox [RGB] {"
            colorbox += background_color['r'] + ", "
            colorbox += background_color['g'] + ", "
            colorbox += background_color['b'] + "} "
                      
        result += margins_before
        result += begin_margin
        result += colorbox
        result += r"{\parbox {\textwidth}"
        result += r"{"
        result += justification_before
        for element in paragraph.content:
            result += element.generate()
        result += justification_after
        result += r"}"
        result += r"}"
        for _ in xrange(0, counter):
            result += r"}"   
        result += end_margin
        result += margins_after
        
        
        return result
        


class _LatexSpanBuilder(object):
    def generate(self, span):
        result = ""
        highlight = ""
        counter = 0;
        font_changed = False
        if span.effective_style.has_key('background-color'):
            background_color = _generate_rgb_from_hex(span.effective_style['background-color'])
            counter += 2
            result += r"{\protect\definecolor {spancolor}{RGB}{"
            result += background_color['r'] + ", "
            result += background_color['g'] + ", "
            result += background_color['b'] + "} "
            result += r"\protect\sethlcolor {spancolor}"
            highlight += r"\texthl{"
        if span.effective_style.has_key('font-name'):
            font_name = span.effective_style['font-name']
            font_changed = True
            counter += 1
            result += r"{"
            font_family = self.__get_font_family(font_name)
            if font_family is not None:
                result += r"\fontfamily {" + font_family + r"} "
        if span.effective_style.has_key('font-size'):
            font_size = span.effective_style['font-size'] 
            if not font_changed:
                result += r"{"
                counter += 1
            result += r"\fontsize {" + str(font_size) + "}{" + self.__get_leading(font_size) + "}"
            font_changed = True
        if font_changed:
            result += r"\selectfont "
        if span.effective_style.has_key('color'):
            font_color = _generate_rgb_from_hex(span.effective_style['color']) 
            counter += 1
            result += r"\color [RGB] {";
            result += font_color['r'] + r", "
            result += font_color['g'] + r", "
            result += font_color['b'] + r"} {"
        if span.effective_style.has_key('font-effect'):
            font_effects = span.effective_style['font-effect']
            if FontEffectProperty.BOLD in font_effects:
                counter += 1
                result += r"\textbf {"
            if FontEffectProperty.ITALIC in font_effects:
                counter += 1
                result += r"\textit{"
            if FontEffectProperty.UNDERLINE in font_effects:
                counter += 1
                result += r"\underline{"
        
        result += highlight
        result += span.text
        for _ in xrange(0, counter):
            result += r"}"
        return result
       
    def __get_leading(self, number):
        number = int(number *1.2)
        return str(number)
    
    def __get_font_family(self, font_name):
        if font_name ==  "Times New Roman":
            return r"ptm"
        if font_name == "Arial":
            return r"phv"
        if font_name == "Computer Modern":
            return r"cmr"

       
    def __get_leading(self, number):
        number = int(number *1.2)
        return str(number)
    
    def __get_font_family(self, font_name):
        if font_name ==  "Times New Roman":
            return r"ptm"
        if font_name == "Arial":
            return r"phv"
        if font_name == "Computer Modern":
            return r"cmr"

class _FloatGenerator(object):
    def __init__(self, main_builder):
        self.__format_numbers = {}
        self.main_builder = main_builder
        
    def generate_float(self, element, float_name, number_command, inner_part):
        result = ""
        
        pre = ""
        post = ""
        tab_indent_level = 1
        margins_before = ""
        margins_after = ""
        hspace_after = ""
        caption = ""
        captionsetup_parameters = {}
        captionsetup = ""
        number_declaration = ""
            
        # handling the "alignment" style 
        if element.is_style_element_set("alignment"):
            align_env = None 
            if element.effective_style['alignment'] == AlignmentProperty.LEFT\
                    or element.effective_style['alignment'] == AlignmentProperty.JUSTIFY:
                align_env = "flushleft"
                captionsetup_parameters['justification'] = "raggedright"
            elif element.effective_style['alignment'] == AlignmentProperty.CENTER:
                align_env = "center"
                captionsetup_parameters['justification'] = "centering"
            elif element.effective_style['alignment'] == AlignmentProperty.RIGHT:
                align_env = "flushright"
                captionsetup_parameters['justification'] = "raggedleft"
            
            if align_env is not None:
                tabs = "\t" * tab_indent_level
                pre += "\n%s\\begin{%s}" % (tabs, align_env)
                post = ("\n%s\\end{%s}" % (tabs, align_env)) + post
                tab_indent_level += 1
                captionsetup_parameters['singlelinecheck'] = "false"
        
        # handling the margins
        if element.is_style_element_set("margin-top")\
                    or element.is_style_element_set("margin-bottom")\
                    or element.is_style_element_set("margin-left")\
                    or element.is_style_element_set("margin-right"):
            margin_top = 0
            margin_bottom = 0
            margin_left = 0
            margin_right = 0
            
            if element.is_style_element_set("margin-top"):
                margin_top = element.effective_style['margin-top']
                
            if element.is_style_element_set("margin-bottom"):
                margin_bottom = element.effective_style['margin-bottom']
                
            if element.is_style_element_set("margin-left"):
                margin_left = element.effective_style['margin-left']
                
            if element.is_style_element_set("margin-right"):
                margin_right = element.effective_style['margin-right']
                
            if margin_top != 0:
                margins_before += "\\vspace*{%.2fpt}" % margin_top
            if margin_left != 0:
                margins_before += "\\hspace*{%.2fpt}" % margin_left
            if margin_right != 0:
                hspace_after += "\\hspace*{%.2fpt}" % margin_right
            if margin_bottom != 0:
                margins_after += "\\vspace*{%.2fpt}" % margin_bottom
                
            if (margin_left != 0) or (margin_right != 0):
                captionsetup_parameters['margin'] = "{%.2fpt,%.2fpt}" % \
                                (margin_left, margin_right)
                captionsetup_parameters['oneside'] = None
            
        if len(margins_before) > 0:
            margins_before += "\n" + ("\t" * tab_indent_level)
        if len(hspace_after) > 0:
            hspace_after = "\n" + ("\t" * tab_indent_level) + hspace_after
        if len(margins_after) > 0:
            margins_after = "\n" + ("\t" * tab_indent_level) + margins_after
        
        # putting the caption
        if len(element.caption) > 0:
            caption_content = ""
            for span in element.caption:
                caption_content += span.generate()
                
            caption = "\n%s\caption{%s}" % ("\t" * tab_indent_level, \
                                                         caption_content)

            # handling the sequence
            if element.sequence is not None:
                if element.is_style_element_set("seq-number-sep"):
                    number = element.sequence.to_str(element.\
                                            effective_style['seq-number-sep'])
                else:
                    number = str(element.sequence)
                    
                number_declaration = "\n%s\\renewcommand{\\%s}{%s}" % \
                            ("\t" * (tab_indent_level - 1), number_command, \
                             number)
                            
            if element.is_style_element_set("caption-title"):
                captionsetup_parameters['format'] = element.caption_format_name
                
            captionsetup = "\n%s\\captionsetup%s" % \
                    (("\t" * (tab_indent_level - 1)), \
                    _generate_parameters_list(captionsetup_parameters, False))
        
        # advancing the sequence, if defined
        if element.sequence is not None:
            element.sequence.advance()
            
        result += "\n\n"
        result += "\\begin{%s}[ht!]" % float_name
        result += number_declaration
        result += captionsetup
        result += pre
        result += "\n" + ("\t" * tab_indent_level)
        result += margins_before
        result += inner_part
        result += hspace_after
        result += caption 
        result += margins_after
        result += post
        result += "\n\\end{%s}" % float_name
        
        return result
        
    def __generate_new_format_name(self, format_prefix):
        if format_prefix not in self.__format_numbers:
            self.__format_numbers[format_prefix] = 0
        
        result = "%s%06d" % (format_prefix, self.__format_numbers[format_prefix])
        self.__format_numbers[format_prefix] += 1
        return result
    
    def __generate_caption_format(self, caption_title_style, number_command):
        result = ""
        caption_title = caption_title_style
        if isinstance(caption_title, str):
            caption_title = Span(caption_title)
        if isinstance(caption_title, Span):
            caption_title = [caption_title]
        
        thefigure_inserted = False
        
        for span in caption_title:
            span.text = span.text.replace("\n", r"\\")
            span.text = span.text.replace(" ", "\\ ")
            if not thefigure_inserted:
                try:
                    span.text = span.text % "\\%s " % number_command
                    thefigure_inserted = True
                except TypeError:
                    pass
            
            result += self.main_builder.generate_span(span)
            
        result += "#3"
            
        return result
    
    def __generate_caption_formats_dict(self, document, number_command, \
                                         format_prefix, dest_type):
        result = {}
        stack = []
        visited = {}
        curr_node = document
        formats = {} # key: image, value: caption format
        
        stack.append(curr_node)
        
        while len(stack) > 0:
            first_child_not_visited = None
            for i in xrange(0, len(curr_node.content)):
                if (not visited.has_key(curr_node.content[i])):
                    first_child_not_visited = curr_node.content[i]
                    break
             
            if (first_child_not_visited is not None):
                visited[first_child_not_visited] = True
                stack.append(first_child_not_visited)
                curr_node = first_child_not_visited
            else:
                if (isinstance(curr_node, dest_type) and\
                            (curr_node.is_style_element_set("caption-title"))):
                    formats[curr_node] = self.__generate_caption_format(\
                                curr_node.effective_style['caption-title'], \
                                number_command)
                stack.pop()
                if (len(stack) > 0):
                    curr_node = stack[-1]
        
        format_names = {} # key: caption format, value: caption format name
        
        for image in formats.keys():
            caption_format = formats[image]
            if not format_names.has_key(caption_format):
                image.caption_format_name = self.__generate_new_format_name(\
                                                                format_prefix)
                format_names[caption_format] = image.caption_format_name
            else:
                image.caption_format_name = format_names[caption_format]
                
        for item in format_names.items():
            result[item[1]] = item[0]
                    
        return result
    
    def generate_custom_format_declarations(self, document, number_command, \
                                             caption_prefix, dest_type):
        result = ""
        formats_dict = self.__generate_caption_formats_dict(document,
                                    number_command, caption_prefix, dest_type)
        
        if len(formats_dict) > 0:
            result += "\n"
            
        for format_kv in formats_dict.items():
            result += "\n\\DeclareCaptionFormat{%s}{%s}" % format_kv
        
        return result

class _LatexImageBuilder(object):
    def __init__(self, float_generator):
        self.__float_generator = float_generator
    
    def generate(self, image):
        result = ""
        
        parameters = {}
        
        # handling the "width" style 
        if image.is_style_element_set("width"):
            parameters['width'] = "%.2fmm" % image.effective_style['width']
            
        # handling the "height" style 
        if image.is_style_element_set("height"):
            parameters['height'] = "%.2fmm" % image.effective_style['height']
       
        inner_part = "\\includegraphics%s{%s}" % \
                    (_generate_parameters_list(parameters),
                     image.path)
        result += self.__float_generator.generate_float(image, "figure",
                                                        "thefigure", inner_part)
        
        return result    

class _LatexDocumentBuilder(object):
    def __init__(self, float_generator):
        self.__float_generator = float_generator
        
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
        
        if (not prop.has_key("language")) or (not prop['language'].startswith('en-US')):
            optional_parameters["a4paper"] = None
        
        result += _generate_parameters_list(optional_parameters)
            
        result += "{article}"
        
        return result
    
    def __generate_geometry_package_reference(self, style):
        result = ""
        
        options = {}
        
        if style.has_key("page-size"):
            width = style['page-size'].value[0]
            height = style['page-size'].value[1]
            options["paperwidth"] = ("%.2f" % width) + "mm"
            options["paperheight"] = ("%.2f" % height) + "mm"
            

        if style.has_key('page-orientation') and style['page-orientation'] == \
                        PageOrientationProperty.LANDSCAPE:
            options['landscape'] = None
            
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
        
        if document_properties.has_key("language"):
            lang = document_properties["language"]
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
        result += "\n\\usepackage{soul}"
        
        result += self.__float_generator.generate_custom_format_declarations(\
                            document, "thefigure", "img", Image)
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
        bullet_char_dict[BulletCharProperty.ASTERISK] = r"$\ast$"
        bullet_char_dict[BulletCharProperty.BULLET] = r"$\bullet$"
        bullet_char_dict[BulletCharProperty.CDOT] = r"$\cdot$"
        bullet_char_dict[BulletCharProperty.CIRCLE] = r"$\circ$"
        bullet_char_dict[BulletCharProperty.DIAMOND] = r"$\diamond$"
        bullet_char_dict[BulletCharProperty.MEDIUM_HYPHEN] = r"\textbf{--}"
        bullet_char_dict[BulletCharProperty.LONG_HYPHEN] = r"\textbf{---}"
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
        default_bullet_chars = [BulletCharProperty.BULLET, BulletCharProperty.MEDIUM_HYPHEN,\
                                BulletCharProperty.ASTERISK, BulletCharProperty.CDOT]
        
        level = self.__get_list_level(lst)
        
        return self.__generate_bullet_char_declaration(\
                    self.__get_bullet_command(lst),\
                    self.__get_bullet_char(default_bullet_chars[level]), level)
    
    def generate(self, lst):
        result = ""
        
        if lst.is_style_element_set('list-style'):
            style = lst.effective_style['list-style']
        else:
            style = ListStyleProperty.BULLET
            
        environment = ""
        if style == ListStyleProperty.BULLET:
            environment = "itemize"
        elif style == ListStyleProperty.NUMBER:
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

            for i in xrange(0, len(lst.content)):
                element = lst.content[i]
                item = ""
                newline = ""
                newline_beforeitem = ""
                if not isinstance(element, List):
                    if i > 0 and lst.content[i-1].successor_isinstance(List):
                        newline_beforeitem += "\n"
                    item = "%s\\item" % newline_beforeitem
                    newline = "\n"
                result += "%s\t%s%s %s" % (newline, "\t" * level, item,\
                            element.generate())
            
            result += "\n%s\\end{%s}" % ("\t" * level, environment)
            
            if margin_correction != 0:
                    result += "\n%s\\vspace{%dpt}" % ("\t" * level,\
                            margin_correction)
        
        return result

