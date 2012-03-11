# -*- coding: utf-8 -*-

from pydocgen.model import *
from pydocgen.builders.common import Builder

class HtmlBuilder(Builder):
    def __init__(self):
        super(HtmlBuilder, self).__init__()
    
    def generate_document(self, document):
    	MAIN_STYLE_FILENAME = 'style.css'
    	title = ''
	body = ''
	if 'title' in document.properties:
		title = document.properties['title']
	for element in document:
		body += generate(element)
	self.generate_main_style(MAIN_STYLE_FILENAME)
        return '<html><head>\n\t<link rel=\"stylesheet\" type=\"text/css\" href=\"' + MAIN_STYLE_FILENAME + '\" />\n<title>'+ title +'</title>\n\t</head>\n\t<body>\n'+ body  +'\n\t</body>\n</html>'
    
    def generate_paragraph(self, paragraph):
	p = generate(p)
        return '<p>' + p + '</p>'
    
    def generate_span(self, span):
        return '<span>' + s.text + '</span>'
    
    def generate_header(self, header):
        return '<h1>' + header.sequence.value + '</h1>' 
    
    def generate_list(self, lst):
	result  = ''
	for item in lest.content:
	    result += generate(lst.content)
	if lst.style['list-style'] == ListStyle.BULLET:
	    return '<ul>' + result + '</ul>'
	else:
	    return '<ol>' + result + '</ol>'
    
    def generate_image(self, image):
        return '<a src=\"'+ image.path + '\" alt=\"' + image.sequence.to_str() + '\" />'
    
    def generate_table(self, table):
        return ""
        
    def generate_main_style(self, filename):
    	pass
