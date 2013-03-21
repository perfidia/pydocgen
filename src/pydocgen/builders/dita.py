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
        """Class constructor. Calls base class constructor.
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
        result += '\t<shortdisc>' + title + '</shortdisc>\n'
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
        
        css=self.fontType(span)
        open1='';
        close1='';
        if css=='b':
            open1='<b>'
            close1='</b>'
        if css=='u':
            open1='<u>'
            close1='</u>'
        if css=='i':
            open1='<u>'
            close1='</u>'
        if css=='sdel':
            open1='<u><del>'
            close1='</del></u>'
	if css=='del':
	    open1='<del>'
            close1='</del>'
			
        return open1+span.text+close1

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
        #h_lvl = header.sequence.get_level()+1 if header.sequence.get_level() < 5 else 6
        #h_lvl = 'h'+str(h_lvl);
		
        return '<section>\n\t<title>'+seq_number+' '+content+'</title>\n</section>'
        #return '\n\n<'+h_lvl+' '+self.__generate_style_from_dict(header) + '>' + \
           # seq_number + " " +  + '</'+h_lvl+'>\n\n'

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
        
        result = '\n\n<table'\
         + self.__generate_style_from_dict(table) + '>'
        caption = ''
        if table.sequence != None:
            caption += table.sequence + ' '
        for c in table.caption:
            caption += self.generate(c)
        result+='\n<title>'+caption+'</title>\n'
        colCount=0;
        for j in xrange(0, table.cols_num):
            colCount+=1
        result+='<tgroup cols=\"'+str(colCount)+'\">\n'
        for j in xrange(0, table.cols_num):
            result+='<colspec colnum=\"'+str(j+1)+'\" colname=\"col'+str(j+1)+'\"/>'
        i=0
        skip_cols=0
        result +=  '\n<thead>\n<row>'
       
        for j in xrange(0, table.cols_num):
            if skip_cols > 0:
               skip_cols -= 1
               continue
            colspan_code = ''
            if table.get_cell(i, j).colspan is not None and table.get_cell(i, j).colspan > 1:
               skip_cols = table.get_cell(i, j).colspan - 1
               colspan_code = ' namest=\"col' +str(j+1)+'\" nameend=\"col'+ str(j+table.get_cell(i, j).colspan) + '\" ';
            result+='\n<entry '+colspan_code + self.alignmentFun(table.get_cell(i, j))+'>'
            for k in table.get_cell(i, j).content:
                 result += self.generate(k)
            result += '</entry>'
        result +=  '\n</row>\n</thead>\n<tbody>'
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
                    colspan_code = ' namest=\"col' + str(j+1)+'\" nameend=\"col'+ str(j+table.get_cell(i, j).colspan) + '\" ';
                result+='\n<entry '+colspan_code + self.alignmentFun(table.get_cell(i, j))+'>'
                for k in table.get_cell(i, j).content:
                    result += self.generate(k)
                result += '</entry>'
            result += '\n</row>\n'
        return  result + '\n</tbody>\n</tgroup>\n</table>\n\n'

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
        """Generates a style for an element.
        
        Args:
            elem (Paragraph): Stores information about content of a paragraph. 
        
        """
        
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
	
    def alignmentFun(self,elem):
        style = elem.style
        css = ''
        if style != None:
            for key in style.keys():
                if key == 'alignment':
                    css+='align=\" '+{AlignmentProperty.LEFT:'left\"'\
                              ,AlignmentProperty.CENTER:'center\"', \
                              AlignmentProperty.RIGHT:'right\"', \
                              AlignmentProperty.JUSTIFY:'justify\"'\
                              }.get(style[key])
        return css;

    def fontType(self,elem):
        if isinstance(elem, str) or isinstance(elem, unicode):
            return ''
        style = elem.style
        css = ''
        if style != None:
            for key in style.keys():
                if key == 'font-effect':
                    font_effects = style['font-effect']
                    if FontEffectProperty.BOLD in font_effects:
                        css = 'b'
                    if FontEffectProperty.ITALIC in font_effects:
                        css = 'i'
                    if FontEffectProperty.UNDERLINE in font_effects \
                        and FontEffectProperty.STRIKE in font_effects:
                        css = 'sdel'
                    elif FontEffectProperty.UNDERLINE in font_effects:
                        css = 'u'
                    elif FontEffectProperty.STRIKE in font_effects:
                        css = 'del'
        return css	
