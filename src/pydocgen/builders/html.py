# -*- coding: utf-8 -*-

from pydocgen.model import *
from pydocgen.builders.common import Builder

class HtmlBuilder(Builder):
    def __init__(self):
        super(HtmlBuilder, self).__init__()
    
    def generate_document(self, document):
    	title = ''
	body = ''
	if 'title' in document.properties:
		title = document.properties['title']
	for element in document:
		body += generate(element)
	
        return "<html><title>"+ title +"</title><body>"+ body  +"</body></html>"
    
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
        return ""
    
    def generate_table(self, table):
        return ""
