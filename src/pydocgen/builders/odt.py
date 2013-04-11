# -*- coding: utf-8 -*-

from pydocgen.model import ListStyleProperty, AlignmentProperty, FontEffectProperty, Image, Style, Table

from pydocgen.builders.common import Builder


class OdtBuilder(Builder):

    def __init__(self):
        super(OdtBuilder, self).__init__()

        self.extension = "fodt"

    def generate_document(self, document):
        
        self.styles = dict()
        self.styleIndex = 0
        
        body = ''

        for element in document.content:
            body += self.generate(element)
         
        styles = '    <office:document-styles>\n'
        if self.styles is not None:
            for key in self.styles.keys():
                styles += '        <style:style style:name="T' + str(key) + '" style:family="text">\n'
                styles += '            <style:text-properties ' + self.styles[key] + '/>\n'
                styles += '        </style:style>\n'
        styles += '    </office:document-styles>\n'
        
        result =  '<?xml version="1.0" encoding="UTF-8"?>\n'
        result += '\n'
        result += '<office:document-content\n'
        result += '    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" \n'
        result += '    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"\n'
        result += '    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" \n'
        result += '    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"\n'
        result += '    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"\n'
        result += '    office:version="1.2" \n'
        result += '    office:mimetype="application/vnd.oasis.opendocument.text">\n'
        result += '</office:document-content>\n'
        result += '\n'
        result += '<office:document-meta>\n'
        result += '        <meta:creation-date>2013-04-09T22:26:39</meta:creation-date>\n'
        result += '        <meta:generator>pydocgen 0.0.3</meta:generator>\n'
        result += '</office:document-meta>\n'
        result += styles
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

        resolved = self.resolveStyle(span);

        if resolved:
            result = '<text:span text:style-name="T' + str(self.styleIndex) + '">' + span.text + '</text:span>'
        else:
            result = '<text:span>' + span.text + '</text:span>'
        
        return result
    
    def resolveStyle(self, elem):
        if isinstance(elem, str) or isinstance(elem, unicode):
                return ''
        style = elem.style
        
        self.styleIndex += 1
        styleBody = ''
        
        if style is not None:
            for key in style.keys():
                if key == 'font-effect':
                    font_effects = style['font-effect']
                    if FontEffectProperty.BOLD in font_effects:
                        styleBody += 'fo:font-weight="bold" style:font-weight-asian="bold" style:font-weight-complex="bold" '
                    if FontEffectProperty.ITALIC in font_effects:
                        styleBody += 'fo:font-style="italic" style:font-style-asian="italic" style:font-style-complex="italic" '
                    elif FontEffectProperty.UNDERLINE in font_effects:
                        styleBody += 'style:text-underline-style="solid" style:text-underline-width="auto" style:text-underline-color="font-color" '
                        
                    self.styles[self.styleIndex] = styleBody
                    
        if styleBody <> '':
            return True
        else:
            return False;
    
    def generate_header(self, header):
        
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
        
        return '        <text:h text:outline-level="' + seq_number + '">' + content + '</text:h>\n'
    
    def generate_list(self, el):
        return ''
    
    def generate_image(self, el):
        return ''
    
    def generate_table(self, el):
        return ''
