# -*- coding: utf-8 -*-

import os

from pydocgen.model import ListStyleProperty, AlignmentProperty, \
                                    FontEffectProperty, Image, Style, Table

from pydocgen.builders.common import Builder

class DitaBuilder(Builder):
    """Class responsible for creating a DITA document.
    It inherits from base Builder class shared between all builder classes.
    """
    def __init__(self):
        """Class constructor. 
        """
        super(DitaBuilder, self).__init__()
        self.CSS_STYLE_FN = 'style.css'

        self.extension = "dita"

    def generate_document(self, document):
        """Main method for generating DITA document. Generates DITA frame for content and fills that frame with data.
        
        Args:
            document (Document): Stores a document representation independent of a particular builder class.
        """
        body = ''
        for element in document.content:
            body += self.generate(element)
        self.generate_style_file(document, self.CSS_STYLE_FN)
        result = '';
        result += '<?xml version="1.0" encoding="utf-8"?>\n';
        result += '<!DOCTYPE map PUBLIC "-//OASIS//DTD DITA Map//EN" "../dtd/map.dtd">\n';
        if 'language' in document.properties:
            result += '<topic xml:lang=\"' + document.properties['language'] + '\" id="main_topic" >'
        else:
            result += '<topic xml:lang="en" id="main_topic">\n'
        title = ''
        if 'title' in document.properties:
            title = document.properties['title']
        result += '\t<title>' + title + '</title>\n'
        result += '\t<shortdesc>' + title + '</shortdesc>\n'
        result += '<body>\n' + body + '\n</body>\n</topic>\n'
        return result

    def generate_paragraph(self, paragraph):
        """Generates a DITA paragraph and fills it with data.
        
        Args:
            paragraph (Paragraph): Stores information about the paragraph. Information is independent of the output file format.
        """
        p, tmp = '', None
        if paragraph.content:
            for element in paragraph.content:
                tmp = self.generate(element)
                if tmp :
                    p += tmp
        return '\n<p' + self.__generate_style_from_dict(paragraph) + \
             '>\n\t' + p + '\n</p>\n'

    def generate_span(self, span):
        """Generates a DITA span.
        
        Args:
            span (Span): stores information about span. Information is independent of the output file format.
        """
        return '<span' + self.__generate_style_from_dict(span) + '>' + \
            span.text + '</span>'

    def generate_header(self, header):
        """Generates a DITA header and fills it with data.
        
        Args:
        header (Header): Stores information about the header. Information is independent of the output file format.
        """
        content = ''
        if header.content:
            for element in header.content:
                if element:
                    content += element.generate()

        seq_number = ''
        if header.sequence is not None:
            if header.is_style_property_set('header-numbered'):
                if header.effective_style['header-numbered']:
                    if element.is_style_property_set("seq-number-sep"):
                        seq_number = element.sequence.to_str(header.\
                                            effective_style['seq-number-sep'])
                    else:
                        seq_number = str(header.sequence)
                    header.sequence.advance()
            else:
                header.sequence.advance()
        h_lvl = header.sequence.get_level()+1 if header.sequence.get_level() < 5 else 6
        h_lvl = 'h'+str(h_lvl);
        return '\n\n<'+h_lvl+' '+self.__generate_style_from_dict(header) + '>' + \
            seq_number + " " + content + '</'+h_lvl+'>\n\n'

    def generate_list(self, lst):
        """Generates a DITA list and fills it with content.
        
        Args:
            lst(List): Stores information about the list. Information is independent of the output file format.
        """
        result, tmp = '', None
        for item in lst.content:
            tmp = self.generate(item)
            if tmp:
                result += '\n<li' + self.__generate_style_from_dict(tmp) + '>' + tmp + '</li>\n'
        if 'list-style' in lst.style.keys() and lst.style['list-style'] == ListStyleProperty.NUMBER:
            return '\n<ol' + self.__generate_style_from_dict(lst) + '>\n' + result + '\n</ol>\n'
        elif 'list-style' in lst.style.keys() and lst.style['list-style'] == ListStyleProperty.BULLET:
            return '\n<ul' + self.__generate_style_from_dict(lst) + '>\n' + result + '\n</ul>\n'
        else:
            return '\n<ul' + self.__generate_style_from_dict(lst) + '>\n' + result + '\n</ul>\n'

    def generate_table(self, table):
        """Generates a DITA table and fills the table with content.
        
        Args:
            table (Table): Stores information about the table. Information is independent of the output file format.
        
        """
        result = '\n\n<simpletable '\
         + self.__generate_style_from_dict(table) + '>'
        caption = ''
        if table.sequence != None:
            caption += table.sequence + ' '
        for c in table.caption:
            caption += self.generate(c)
        result +=  '<sthead>'+caption+'</sthead>'
        skip_cols = 0
        for i in xrange(0, table.rows_num):
            result += '\n<strow>\n' #style? no!
            for j in xrange(0, table.cols_num):
                if skip_cols > 0:
                    skip_cols -= 1
                    continue
                colspan_code = ''
                if table.get_cell(i, j).colspan is not None and table.get_cell(i, j).colspan > 1:
                    skip_cols = table.get_cell(i, j).colspan - 1
                    colspan_code = ' colspan=\"' + str(table.get_cell(i, j).colspan) + '\" ';
                result+='\n<stentry '+colspan_code + self.__generate_style_from_dict(table.get_cell(i, j))+'>'
                for k in table.get_cell(i, j).content:
                    result += self.generate(k)
                result += '</stentry>'
            result += '\n</strow>\n'
        return  result + '\n</simpletable>\n\n'

    def generate_style_file(self, document, fn):
        """Generates a css style
            
        Args:
            document (Document): stores information about the document.
            fn (str): file path.
        
        """
        style = document.effective_style

        css = 'body {\n'
        if style != None:
            for key in style.keys():
                if key in ('margin-top', 'margin-bottom', 'margin-left', 'margin-right', 'font-size', 'font-name', 'alignment', 'text-indent', \
                           'color', 'background-color', 'list-_style', 'item-spacing', 'item-indent'):
                    if key == 'font-name':
                        css += 'font-family: ' + style[key] + ';\n'
                    elif key == 'alignment':
                        css += 'text-align: ' + {AlignmentProperty.LEFT:'left', AlignmentProperty.CENTER:'center',AlignmentProperty.RIGHT:'right', \
                                                 AlignmentProperty.JUSTIFY:'justify'}.get(style[key]) + ';\n'
                    elif  key == 'list-_style':
                        pass #Using <ul> or <ol> instead
                    elif key == 'font-effect':
                        css += 'font-style: '+{FontEffectProperty.BOLD:'bold', FontEffectProperty.ITALIC:'italic', FontEffectProperty.UNDERLINE:'oblique'}.get(style[key])+';\n'
                    elif key == 'item-spacing':
                        css += 'border-spacing: ' + str(style[key]) + 'pt ' + str(style[key]) + 'pt;\n';
                    elif key == 'item-indent':
                        pass #css += 'text-indent: ' + str(style[key]) + 'pt;\n'
                    elif key == 'background-color' or key == 'color':
                        css += key + ': ' + style[key] + ';\n'
                    else:
                        css += key + ': ' + str(style[key]) + 'pt;\n'
        css = css[:-2]
        css += '\n}\n'

        fn = os.path.join(document.path, fn)

        output_file = open(fn, "w")
        output_file.write(css)
        output_file.close()
        return None


    def generate_image(self, image):
        """Generates a DITA image.
        
        Args:
            image (Image): Stores information about the image. Information is independent of the output file format.
        """
        image_caption = ''
        if image.sequence != None:
            image_caption += image.sequence + ' '
        for c in image.caption:
            image_caption += self.generate(c)
        return '<div><image href=\"' + image.path + '\" placement=\"break\"' + self.__generate_style_from_dict(image) + '>\n<alt>alternative </alt>\n</image>\n</div>'

    def generate_inline_style(self, elem):
        result = ''
        try:
            if isinstance(elem.style, Style) :
                #if elem.__class__.style != elem.style:
                result += self.__generate_style_from_dict(elem)
        except:
            result = ''
        return result


    def __generate_style_from_dict(self, elem):
	return ''
	
	"""
        if isinstance(elem, str) or isinstance(elem, unicode):
            return ''
        style = elem.style
        css = ''
        if style != None:
            css = 'style = \"'
            for key in style.keys():
                #if key in ('margin-top', 'margin-bottom', 'margin-left', 'margin-right','font-size','font-name','alignment','text-indent','color','background-color','list-_style','item-spacing','item-indent'):
                    if key == 'font-name':
                        css += 'font-family: ' + style[key] + ';'
                    elif key == 'alignment':
                        if isinstance(elem, Image) or isinstance(elem, Table):
                            css+='display: block; margin-left: auto; margin-right: auto; '
                        else:
                            css+='text-align: '+{AlignmentProperty.LEFT:'left'\
                              ,AlignmentProperty.CENTER:'center', \
                              AlignmentProperty.RIGHT:'right', \
                              AlignmentProperty.JUSTIFY:'justify'\
                              }.get(style[key]) + ';'
                    elif  key == 'list-_style':
                        pass #Using <ul> or <ol> instead
                    elif key == 'font-effect':
                        font_effects = style['font-effect']
                        if FontEffectProperty.BOLD in font_effects:
                            css += 'font-weight: bold;'
                        if FontEffectProperty.ITALIC in font_effects:
                            css += 'font-style: italic;'
                        if FontEffectProperty.UNDERLINE in font_effects \
                        and FontEffectProperty.STRIKE in font_effects:
                            css += 'text-decoration: underline line-through;'
                        elif FontEffectProperty.UNDERLINE in font_effects:
                            css += 'text-decoration: underline;'
                        elif FontEffectProperty.STRIKE in font_effects:
                            css += 'text-decoration: line-through;'
                    elif key == 'item-spacing':
                        css += 'border-spacing: ' + str(style[key]) + 'pt ' + str(style[key]) + 'pt;';
                    elif key == 'item-indent':
                        pass #css += 'text-indent: ' + str(style[key]) + 'pt;\n'
                    elif key == 'background-color' or key == 'color':
                        css += key + ': ' + style[key] + ';'
                    elif key == 'border-width' :
                        css += 'border-style: solid; border-width: ' + str(style[key]) + 'pt;'
                    elif key == 'width' :
                        css += 'width: ' + str(style[key]) + 'mm;'
                    elif key == 'height' :
                        css += 'height: ' + str(style[key]) + 'mm;'
                    else:
                        if not isinstance(elem, Table) and key in ('marign-left', 'margin-right'):
                            css += key + ': ' + str(style[key]) + 'pt;'
            css += '\"'

        return css
   
"""
