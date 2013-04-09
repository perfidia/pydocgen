# -*- coding: utf-8 -*-

from pydocgen.model import ListStyleProperty, AlignmentProperty, FontEffectProperty, Image, Style, Table

from pydocgen.builders.common import Builder


class OdtBuilder(Builder):

    def __init__(self):
        super(OdtBuilder, self).__init__()

        self.extension = "fodt"

    def generate_document(self, document):
        
        body = ''

        for element in document.content:
            body += self.generate(element)
        
        result =  '<?xml version="1.0" encoding="UTF-8"?>\n'
        result += '\n'
        result += '<office:document\n'
        result += '    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" \n'
        result += '    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"\n'
        result += '    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" \n'
        result += '    office:version="1.2" \n'
        result += '    office:mimetype="application/vnd.oasis.opendocument.text">\n'
        result += '\n'
        result += '<office:meta>\n'
        result += '        <meta:creation-date>2013-04-09T22:26:39</meta:creation-date>\n'
        result += '        <meta:generator>pydocgen 0.0.3</meta:generator>\n'
        result += '</office:meta>\n'
        result += '<office:body>\n'
        result += '       <office:text>\n'
        result += body
        #result += '                <text:p text:style-name="Standard">test</text:p>\n'
        result += '        </office:text>\n'
        result += '</office:body>\n'
        result += '</office:document>\n'
        return result;
    
    def generate_paragraph(self, paragraph):        
        p, tmp = '', None
        if paragraph.content:

            for element in paragraph.content:
                tmp = self.generate(element)
                if tmp:
                    p += tmp

        result = '        <text:p text:style-name="Standard">' + p + '</text:p>\n'

        return result
    
    def generate_span(self, span):

        result = '<text:span>' + span.text + '</text:span>'
        return result
    
    
    def generate_header(self, el):
        return ''
    
    def generate_list(self, el):
        return ''
    
    def generate_image(self, el):
        return ''
    
    def generate_table(self, el):
        return ''
