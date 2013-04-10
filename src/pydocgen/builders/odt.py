# -*- coding: utf-8 -*-

from pydocgen.model import ListStyleProperty, AlignmentProperty, FontEffectProperty, Image, Style, Table

from pydocgen.builders.common import Builder


class OdtBuilder(Builder):

    def __init__(self):
        super(OdtBuilder, self).__init__()

        self.extension = "fodt"

    def generate_document(self, document):
        
        self.spanStyles = dict()
        self.paragraphStyles = dict()
        self.styleIndex = 0
        
        body = ''

        for element in document.content:
            body += self.generate(element)
         
        styles = '    <office:automatic-styles>\n'
        if self.spanStyles is not None:
            for key in self.spanStyles.keys():
                styles += '        <style:style style:name="' + str(key) + '" style:family="text">\n'
                styles += '            <style:text-properties ' + self.spanStyles[key] + '/>\n'
                styles += '        </style:style>\n'
        if self.paragraphStyles is not None:
            for key in self.paragraphStyles.keys():
                styles += '        <style:style style:name="' + str(key) + '" style:family="paragraph">\n'
                styles += '            <style:paragraph-properties ' + self.paragraphStyles[key] + '/>\n'
                styles += '        </style:style>\n'
        styles += '    </office:automatic-styles>\n'
        
        #<style:style style:name="P1" style:family="paragraph" style:parent-style-name="Standard">
   #<style:paragraph-properties fo:margin-left="0.4in" fo:margin-right="0in" fo:text-indent="0in" style:auto-text-indent="false"/>
  #</style:style>

        
        result =  '<?xml version="1.0" encoding="UTF-8"?>\n'
        result += '\n'
        result += '<office:document\n'
        result += '    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" \n'
        result += '    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"\n'
        result += '    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" \n'
        result += '    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"\n'
        result += '    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"\n'
        result += '    office:version="1.2" \n'
        result += '    office:mimetype="application/vnd.oasis.opendocument.text">\n'
        result += '\n'
        result += '<office:meta>\n'
        result += '        <meta:creation-date>2013-04-09T22:26:39</meta:creation-date>\n'
        result += '        <meta:generator>pydocgen 0.0.3</meta:generator>\n'
        result += '</office:meta>\n'
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
                    
        styleBody = ''
        
        if paragraph.style is not None:
            if paragraph.style.has_key('text-indent'):
                indent = paragraph.style['text-indent']
                styleBody += 'fo:margin-left="' + str(indent) + 'pt" fo:margin-right="0in" fo:text-indent="0in" style:auto-text-indent="false" '
            if paragraph.style.has_key('margin-top'):
                pass

        if styleBody <> '':
            self.paragraphStyles[self.styleIndex] = styleBody
            result = '        <text:p text:style-name="' + str(self.styleIndex) + '">' + p + '</text:p>\n'
            self.styleIndex += 1
        else:
            result = '        <text:p>' + p + '</text:p>\n'

        return result
    
    def generate_span(self, span):

        resolved = self.resolveStyle(span);

        if resolved:
            result = '<text:span text:style-name="' + str(self.styleIndex) + '">' + span.text + '</text:span>'
            self.styleIndex += 1
        else:
            result = '<text:span>' + span.text + '</text:span>'
        
        return result
    
    def resolveStyle(self, elem):
        if isinstance(elem, str) or isinstance(elem, unicode):
                return ''
        style = elem.style
        
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
                        
                    self.spanStyles[self.styleIndex] = styleBody
                    
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
