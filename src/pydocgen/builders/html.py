# -*- coding: utf-8 -*-

from pydocgen.model import ListStyleProperty, AlignmentProperty, FontEffectProperty, Image, Style, Table # wildcard imports are bad :)
from pydocgen.builders.common import Builder

class HtmlBuilder(Builder):
    def __init__(self):
        super(HtmlBuilder, self).__init__()
        self.CSS_STYLE_FN = 'style.css'
    
    def generate_document(self, document):
        body = ''
        for element in document.content:
            body += str(self.generate(element))
        self.generate_style_file(document.effective_style, self.CSS_STYLE_FN)
        result =''
        if 'language' in document.properties:
            result += '<html lang=\"' + document.properties['language'] + '\">'
        else:
            result += '<html>\n'
        result += '<head>\n'
        if 'title' in document.properties:
            result += '\t<title>' + document.properties['title'] + '</title>\n'
        result += '\t<link rel=\"stylesheet\" type=\"text/css\" href=\".\\' + self.CSS_STYLE_FN + '\" />\n'
        result += '</head>\n\n'
        result += '<body>\n' + body + '\n</body>\n</html>'
        return result
    
    def generate_paragraph(self, paragraph):
        p, tmp = '', None
        if paragraph.content:
            for element in paragraph.content:        
                tmp = self.generate(element)
                if tmp :
                    p += tmp
        return '\n<p '+self.__generate_style_from_dict(paragraph)+'>\n\t' + p + '\n</p>\n'
    
    def generate_span(self, span):
        return '<span '+self.__generate_style_from_dict(span)+'>' + span.text + '</span>'
    
    def generate_header(self, header):
        content = ''
        if header.content:
            for element in header.content:
                if element:
                    content += element.generate()
        
        seq_number = ''
        if header.sequence is not None:
            if header.is_style_element_set('header-numbered'):
                if header.effective_style['header-numbered']:
                    if element.is_style_element_set("seq-number-sep"):
                        seq_number = element.sequence.to_str(header.\
                                            effective_style['seq-number-sep'])
                    else:
                        seq_number = str(header.sequence)
                    header.sequence.advance()
            else:
                header.sequence.advance()
        
        return '\n\n<h1 ' + self.__generate_style_from_dict(header) + '>' + seq_number + " " + content + '</h1>\n\n' 
    
    def generate_list(self, lst):
        result, tmp  = '', None
        for item in lst.content:
            tmp = self.generate(item)
            if tmp:
                result += '\n<li '+self.generate_inline_style(tmp)+'>'+ tmp +'</li>\n'
        if 'list-style' in lst.style.keys() and lst.style['list-style'] == ListStyleProperty.NUMBER:
            return '\n<ol '+self.generate_inline_style(lst)+'>\n' + result + '\n</ol>\n'
        elif 'list-style' in lst.style.keys() and lst.style['list-style'] == ListStyleProperty.BULLET:
            return '\n<ul '+self.generate_inline_style(lst)+'>\n' + result + '\n</ul>\n'
        else:
            return '\n<ul '+self.generate_inline_style(lst)+'>\n' + result + '\n</ul>\n'
        #lst.style['list-style'] = ListStyleProperty.NUMBER
        
    def generate_table(self, table):
        result = '\n\n<table border=\"1\" '+self.__generate_style_from_dict(table)+'>'
        for i in xrange(0, table.rows_num ):
            result += '\n<tr>\n' #style? no!
            for j in xrange(0, table.cols_num ):
                result += '\n<td ' + self.__generate_style_from_dict(table.get_cell(i, j)) + '>'
                for k in table.get_cell(i, j).content:
                    result += self.generate( k ) 
                result += '</td>'
            result += '\n</tr>\n'
        return  result  + '\n</table>\n\n'
        
    def generate_style_file(self, style, fn):
        css = 'body {\n'
        if style != None:
            for key in style.keys():
                if key in ('margin-top', 'margin-bottom', 'margin-left', 'margin-right','font-size','font-name','alignment','text-indent','color','background-color','list-_style','item-spacing','item-indent'):
                    if key == 'font-name':
                        css += 'font-family: ' + style[key] + ';\n'
                    elif key == 'alignment':
                        css += 'text-align: '+{AlignmentProperty.LEFT:'left',AlignmentProperty.CENTER:'center',AlignmentProperty.RIGHT:'right',AlignmentProperty.JUSTIFY:'justify'}.get(style[key])+';\n'
                    elif  key == 'list-_style':
                        pass #Using <ul> or <ol> instead
                    elif key == 'font-effect':
                        css += 'font-style: '+{FontEffectProperty.BOLD:'bold',FontEffectProperty.ITALIC:'italic',FontEffectProperty.UNDERLINE:'oblique'}.get(style[key])+';\n'
                    elif key == 'item-spacing':
                        css += 'border-spacing: '+str(style[key])+'pt '+str(style[key])+'pt;\n letter-spacing: '+str(style[key])+'pt;\n word-spacing: '+str(style[key])+'pt;\n';
                    elif key == 'item-indent':
                        pass #css += 'text-indent: ' + str(style[key]) + 'pt;\n'
                    elif key == 'background-color' or key == 'color':
                        css += key + ': ' + style[key] + ';\n'
                    else:
                        css += key + ': ' + str(style[key]) + 'pt;\n'
        css = css[:-2]
        css += '\n}\n'
        
        output_file = open(fn, "w")
        output_file.write(css)
        output_file.close() 
        return None


    def generate_image(self, image):
        image_width_code = image.style.get('width', None) 
        if image_width_code :
            image_width_code = 'width=\"'+str(image_width_code)+'\"'
        else:
            image_width_code = ''
        image_height_code = image.style.get('height')
        if image_height_code : 
            image_height_code = 'height=\"'+str(image_height_code)+'\"'
        else:
            image_height_code = '' 
        return '<div+'+self.__generate_style_from_dict(image)+'><img src=\"' + image.path + '\" '+self.__generate_style_from_dict(image)+' '+image_height_code+' '+image_width_code+'/></div>'
    
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
                            css += 'display: block; margin-left: auto; margin-right: auto; '
                        else:
                            css += 'text-align: '+ {AlignmentProperty.LEFT:'left',AlignmentProperty.CENTER:'center',AlignmentProperty.RIGHT:'right',AlignmentProperty.JUSTIFY:'justify'}.get(style[key])+';'
                    elif  key == 'list-_style':
                        pass #Using <ul> or <ol> instead
                    elif key == 'font-effect':
                        css += {FontEffectProperty.BOLD:'font-weight: bold',FontEffectProperty.ITALIC:'font-style: italic',FontEffectProperty.UNDERLINE:'text-decoration: underline', 'text-decoration': str(style[key])}.get(style[key], 'text-decoration: '+str(style[key]))+';'
                    elif key == 'item-spacing':
                        css += 'border-spacing: '+str(style[key])+'pt '+str(style[key])+'pt; letter-spacing: '+str(style[key])+'pt; word-spacing: '+str(style[key])+'pt;';
                    elif key == 'item-indent':
                        pass #css += 'text-indent: ' + str(style[key]) + 'pt;\n'
                    elif key == 'background-color' or key == 'color':
                        css += key + ': ' + style[key] + ';'
                    elif key == 'border-width' : 
                        css += 'border-style: solid; border-width: ' + str(style[key]) + 'pt;'
                    else:
                        if not isinstance(elem, Table) and key in ('marign-left', 'margin-right'): 
                            css += key + ': ' + str(style[key]) + 'pt;'
            css += '\"'
        return css 
