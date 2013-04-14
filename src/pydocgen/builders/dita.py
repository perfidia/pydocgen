# -*- coding: utf-8 -*-

import os

from pydocgen.model import ListStyleProperty, AlignmentProperty, FontEffectProperty, Image, Style, Table

from pydocgen.builders.common import Builder


class DitaBuilder(Builder):
    """Class responsible for creating a DITA V1.1 document.
    It inherits from base Builder class shared between all builder classes.
    """
    
    def __init__(self):
        super(DitaBuilder, self).__init__()
        self.extension = "dita"

    def generate_document(self, document):
        """Main method for generating DITA document. Generates DITA frame for content and fills that frame with data.
        
        Args:
            document (Document): Stores a document representation independent of a particular builder class.
        """
        
        body = ''

        for element in document.content:
            body += self.generate(element)


        result = ''
        result += '<?xml version="1.0" encoding="utf-8"?>\n'
        result += '<!DOCTYPE topic PUBLIC "-//OASIS//DTD DITA Composite//EN" "http://docs.oasis-open.org/dita/v1.1/CD01/dtd/ditabase.dtd">\n'
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
                if tmp:
                    p += tmp

        return '\n<p' + \
               '>\n\t' + p + '\n</p>\n'

    def generate_span(self, span):
        """Generates a DITA span.
        
        Args:
            span (Span): stores information about span. Information is independent of the output file format.
        """

        css = self.fontType(span)
        open1 = ''
        close1 = ''
        if css == 'b':
            open1 = '<b>'
            close1 = '</b>'
        if css == 'u':
            open1 = '<u>'
            close1 = '</u>'
        if css == 'i':
            open1 = '<u>'
            close1 = '</u>'
        

        return open1 + span.text + close1

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
                        seq_number = element.sequence.to_str(header.effective_style['seq-number-sep'])
                    else:
                        seq_number = str(header.sequence)
                    header.sequence.advance()
            else:
                header.sequence.advance()

        return '<section>\n\t<title>' + seq_number + ' ' + content + '</title>\n</section>'

    def generate_list(self, lst):
        """Generates a DITA list and fills it with content.
        
        Args:
            lst(List): Stores information about the list. Information is independent of the output file format.
        """
        
        result, tmp = '', None

        for item in lst.content:
            tmp = self.generate(item)
            if tmp:
                result += '\n<li' + '>' + tmp + '</li>\n'

        if 'list-style' in lst.style.keys() and lst.style['list-style'] == ListStyleProperty.NUMBER:
            return '\n<ol' + '>\n' + result + '\n</ol>\n'
        elif 'list-style' in lst.style.keys() and lst.style['list-style'] == ListStyleProperty.BULLET:
            return '\n<ul' + '>\n' + result + '\n</ul>\n'
        else:
            return '\n<ul' + '>\n' + result + '\n</ul>\n'

    def generate_table(self, table):                
        """Generates a DITA table and fills the table with content.
        
        Args:
            table (Table): Stores information about the table. Information is independent of the output file format.        
        """
        result = '\n\n<table' + '>'
        caption = ''
        if table.sequence is not None:
            caption += table.sequence + ' '

        for c in table.caption:
            caption += self.generate(c)

        result += '\n<title>' + caption + '</title>\n'
        colCount = 0

        for j in xrange(0, table.cols_num):
            colCount += 1

        result += '<tgroup cols=\"' + str(colCount) + '\">\n'

        for j in xrange(0, table.cols_num):
            result += '<colspec colnum=\"' + str(j + 1) + '\" colname=\"col' + str(j + 1) + '\" />'

        i = 0
        skip_cols = 0
        result += '\n<thead>\n<row>'

        for j in xrange(0, table.cols_num):
            if skip_cols > 0:
                skip_cols -= 1
                continue
            colspan_code = ''
            if table.get_cell(i, j).colspan is not None and table.get_cell(i, j).colspan > 1:
                skip_cols = table.get_cell(i, j).colspan - 1
                colspan_code = ' namest=\"col' + str(j + 1) + '\" nameend=\"col' + str(
                    j + table.get_cell(i, j).colspan) + '\" '
            result += '\n<entry ' + colspan_code + self.alignmentFun(table.get_cell(i, j)) + '>'

            for k in table.get_cell(i, j).content:
                result += self.generate(k)

            result += '</entry>'
        result += '\n</row>\n</thead>\n<tbody>'
        skip_cols = 0

        for i in xrange(1, table.rows_num):
            result += '\n<row>\n' #style? no!

            for j in xrange(0, table.cols_num):
                if skip_cols > 0:
                    skip_cols -= 1
                    continue
                colspan_code = ''
                if table.get_cell(i, j).colspan is not None and table.get_cell(i, j).colspan > 1:
                    skip_cols = table.get_cell(i, j).colspan - 1
                    colspan_code = ' namest=\"col' + str(j + 1) + '\" nameend=\"col' + str(
                        j + table.get_cell(i, j).colspan) + '\" '
                result += '\n<entry ' + colspan_code + self.alignmentFun(table.get_cell(i, j)) + '>'

                for k in table.get_cell(i, j).content:
                    result += self.generate(k)

                result += '</entry>'
            result += '\n</row>\n'
        return result + '\n</tbody>\n</tgroup>\n</table>\n\n'



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

        return '<image href=\"' + image.path + '\" placement=\"break\" ' + self.alignmentFun(
            image) + '></image>\n'


    def alignmentFun(self, elem):
        """Sets text alignment for the element. Alignment is among left, center, right and justify.
        
        Args:
            elem (Element): Stores information about content of particular part of text.
        """
        
        style = elem.style
        css = ''
        if style != None:
            for key in style.keys():
                if key == 'alignment':
                    css += 'align=\"' + {AlignmentProperty.LEFT: 'left\"', \
                                         AlignmentProperty.CENTER: 'center\"', \
                                         AlignmentProperty.RIGHT: 'right\"', \
                                         AlignmentProperty.JUSTIFY: 'justify\"' \
                        }.get(style[key])
        return css

    def widthFun(self, elem):
        """Sets width and height for part of text stored in elem.
        
        Args:
            elem (Element): Stores information about content of particular part of text.        
        """
        
        style = elem.style
        css = ''
        if style is not None:
            for key in style.keys():
                if key == 'width':
                    css += 'colwidth=\" ' + str(style[key]) + '*\"'
                elif key == 'height':
                    css += 'colheight=\"' + str(style[key]) + '*\"'
        return css

    def fontType(self, elem):
        """Sets font effect such as bold, italic underline and strike for the element.
        
        Args:
            elem (Element): Stores information about particular part of text.              
        """
        
        if isinstance(elem, str) or isinstance(elem, unicode):
            return ''
        style = elem.style
        css = ''
        if style is not None:

            for key in style.keys():

                if key == 'font-effect':
                    font_effects = style['font-effect']
                    if FontEffectProperty.BOLD in font_effects:
                        css = 'b'
                    if FontEffectProperty.ITALIC in font_effects:
                        css = 'i'
                    elif FontEffectProperty.UNDERLINE in font_effects:
                        css = 'u'
                    
        return css





