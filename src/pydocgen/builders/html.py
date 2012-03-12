# -*- coding: utf-8 -*-

from pydocgen.model import ListStyle, Alignment, FontEffect, Style # wildcard imports are bad :)
from pydocgen.builders.common import Builder

class HtmlBuilder(Builder):
    def __init__(self):
        super(HtmlBuilder, self).__init__()
        self.CSS_STYLE_FN = 'style.css'
    
    def generate_document(self, document):
        body = ''
        for element in document.content:
            body += element.generate()
        self.generate_style_file(document.effective_style, self.CSS_STYLE_FN)
        result =''
        if 'lang' in document.properties:
            result += '<html lang=\"'+document.properties['lang']+'\">'
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
        return '\n<p '+self.generate_inline_style(paragraph)+'>\n\t' + p + '\n</p>\n'
    
    def generate_span(self, span):
        return '<span '+self.generate_inline_style(span)+'>' + span.text + '</span>'
    
    def generate_header(self, header):
        content = ''
        if header.content:
            for element in header.content:
                if element:
                    content += element.generate()
        
        seq_number = ''
        if header.sequence is not None:
            seq_number = str(header.sequence)
            header.sequence.advance()
        
        return '\n\n<h1 ' + self.generate_inline_style(header) + '>' + seq_number + " " + content + '</h1>\n\n' 
    
    def generate_list(self, lst):
        result, tmp  = '', None
        for item in lst.content:
            tmp = self.generate(item)
            if tmp:
                result += '\n<li '+self.generate_inline_style(tmp)+'>'+ tmp +'</li>\n'
        if lst.style['list-style'] == ListStyle.BULLET:
            return '\n<ul '+self.generate_inline_style(lst)+'>\n' + result + '\n</ul>\n'
        else:
            return '\n<ol '+self.generate_inline_style(lst)+'>\n' + result + '\n</ol>\n'
        
        def generate_image(self, image):
            return '<img src=\"' + image.path + ' '+self.generate_inline_style(image)+'\" />'
        
    def generate_table(self, table):
        result = '<table border=\"1\">'
        for i in xrange(0, table.rows_num - 1):
            for j in xrange(0, table.cols_num - 1):
                result += self.generate( table.get_cell(i, j) )
        return  result  + '</table>'
        
    def generate_style_file(self, style, fn):
        css = 'body {\n'
        if style != None:
            for key in style.keys():
                if key in ('margin-top', 'margin-bottom', 'margin-left', 'margin-right','font-size','font-name','alignment','text-indent','color','background-color','list-_style','item-spacing','item-indent'):
                    if key == 'font-name':
                        css += 'font-family: ' + style[key] + ';\n'
                    elif key == 'alignment':
                        css += 'text-align: '+{Alignment.LEFT:'left',Alignment.CENTER:'center',Alignment.RIGHT:'right',Alignment.JUSTIFY:'justify'}.get(style[key])+';\n'
                    elif  key == 'list-_style':
                        pass #Using <ul> or <ol> instead
                    elif key == 'font-effect':
                        css += 'font-style: '+{FontEffect.BOLD:'bold',FontEffect.ITALIC:'italic',FontEffect.UNDERLINE:'oblique'}.get(style[key])+';\n'
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

    def generate_inline_style(self, elem):
        result = ''
        try:
            if isinstance(elem.style, Style) :
                if elem.__class__.style != elem.style:
                    result += self.__generate_style_from_dict(elem.style)
        except:
            result = ''
        return result

    def __generate_style_from_dict(self, style):
        css = ''
        if style != None:
            css = 'style = \"'
            for key in style.keys():
                if key in ('margin-top', 'margin-bottom', 'margin-left', 'margin-right','font-size','font-name','alignment','text-indent','color','background-color','list-_style','item-spacing','item-indent'):
                    if key == 'font-name':
                        css += 'font-family: ' + style[key] + ';'
                    elif key == 'alignment':
                        css += 'text-align: '+{Alignment.LEFT:'left',Alignment.CENTER:'center',Alignment.RIGHT:'right',Alignment.JUSTIFY:'justify'}.get(style[key])+';'
                    elif  key == 'list-_style':
                        pass #Using <ul> or <ol> instead
                    elif key == 'font-effect':
                        css += 'font-style: '+{FontEffect.BOLD:'bold',FontEffect.ITALIC:'italic',FontEffect.UNDERLINE:'oblique'}.get(style[key])+';'
                    elif key == 'item-spacing':
                        css += 'border-spacing: '+str(style[key])+'pt '+str(style[key])+'pt; letter-spacing: '+str(style[key])+'pt; word-spacing: '+str(style[key])+'pt;';
                    elif key == 'item-indent':
                        pass #css += 'text-indent: ' + str(style[key]) + 'pt;\n'
                    elif key == 'background-color' or key == 'color':
                        css += key + ': ' + style[key] + ';'
                    else:
                        css += key + ': ' + str(style[key]) + 'pt;'
            css += '\"'
        return css 
