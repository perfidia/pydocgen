# -*- coding: utf-8 -*-

from pydocgen.model import ListStyleProperty, AlignmentProperty, FontEffectProperty, Image, Style, Table

from pydocgen.builders.common import Builder

from pydocgen.model import PageOrientationProperty


class OdtBuilder(Builder):

    def __init__(self):
        super(OdtBuilder, self).__init__()

        self.extension = "fodt"

    def generate_document(self, document):
        
        self.spanStyles = dict()
        self.paragraphStyles = dict()
        self.styleIndex = 0
        
        body = ''
        meta= ''

        for element in document.content:
            body += self.generate(element)
            
        # styles.xml file
         
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
        styles += self.__resolveDocumentStyle(document.effective_style)
        styles += '    </office:automatic-styles>\n'
        styles += '    <office:master-styles>\n'
        styles += '        <style:master-page style:name="Standard" style:page-layout-name="pm1"/>\n'
        styles += '    </office:master-styles>'
        
        
        
        #<style:style style:name="P1" style:family="paragraph" style:parent-style-name="Standard">
   #<style:paragraph-properties fo:margin-left="0.4in" fo:margin-right="0in" fo:text-indent="0in" style:auto-text-indent="false"/>
  #</style:style>

        
        # meta.xml file
        
        meta += '<office:document-meta>\n'
        meta += '        <meta:creation-date>2013-04-09T22:26:39</meta:creation-date>\n'
        meta += '        <meta:generator>pydocgen 0.0.3</meta:generator>\n'
        meta += '</office:document-meta>\n'
        
        # content.xml file
        
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
        result += styles
        result += '<office:body>\n'
        result += '       <office:text>\n'
        result += body
        #result += '                <text:p text:style-name="Standard">test</text:p>\n'
        result += '        </office:text>\n'
        result += '</office:body>\n'
        result += '</office:document-content>\n'
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
            styleBody += self.__addAttributeMM(paragraph.style, 'text-indent', 'fo:text-indent')
            styleBody += self.__addAttributeMM(paragraph.style, 'margin-top', 'fo:margin-top')
            styleBody += self.__addAttributeMM(paragraph.style, 'margin-bottom', 'fo:margin-bottom')
            styleBody += self.__addAttributeMM(paragraph.style, 'margin-left', 'fo:margin-left')
            styleBody += self.__addAttributeMM(paragraph.style, 'margin-right', 'fo:margin-right')

        if styleBody <> '':
            self.paragraphStyles[self.styleIndex] = styleBody
            result = '        <text:p text:style-name="' + str(self.styleIndex) + '">' + p + '</text:p>\n'
            self.styleIndex += 1
        else:
            result = '        <text:p>' + p + '</text:p>\n'

        return result
    
    def __addAttributeMM(self, style, name, nativeName):
        return self.__addAttribute(style, name, nativeName, 'mm')
    
    def __addAttribute(self, style, name, nativeName, valueSuffix):
        att = ''
        if style.has_key(name):
            value = str(style[name]) + valueSuffix
            att = nativeName + '="' + value + '" '
        return att
    
    def generate_span(self, span):

        resolved = self.__resolveStyle(span);

        if resolved:
            result = '<text:span text:style-name="' + str(self.styleIndex) + '">' + span.text + '</text:span>'
            self.styleIndex += 1
        else:
            result = '<text:span>' + span.text + '</text:span>'
        
        return result
    
    def __resolveStyle(self, elem):
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
    
    def __resolveDocumentStyle(self, style):
        return self.__resolvePageLayout(style)
#        if style != None:
#            for key in style.keys():
#                if key == 'font-size':
#                    pass
#                elif key == 'font-name':
#                    pass
#                elif key == 'alignment':
#                    pass
#                elif key == 'text-indent':
#                    pass
#                elif key == 'color':
#                    pass
#                elif key == 'background-color':
#                    pass
#                elif key == 'list-style':
#                    pass
#                elif key == 'item-spacing':
#                    pass
#                elif key == 'item-indent':
#                    pass
#                elif key == 'header-numbered':
#                    pass
#                elif key == 'border-width':
#                    pass
                
    def __resolvePageLayout(self, style):
        if style != None:
            styleAttributes = ''
            orientation = None
            size = None
            
            if style.has_key('page-numbering'):
                pass # TODO
            if style.has_key('page-size'):
                size = style['page-size']
                if orientation is not None and size is not None:
                    styleAttributes = self.__getPageSize()
            if style.has_key('page-orientation'):
                orientation = style['page-orientation']
                if orientation == PageOrientationProperty.PORTRAIT:
                    styleAttributes += 'style:print-orientation="portrait" '
                else:
                    styleAttributes += 'style:print-orientation="landscape" '
                if size is not None and size is not None:
                    styleAttributes += self.__getPageSize(size, orientation)
            styleAttributes += self.__addAttributeMM(style, 'margin-top', 'fo:margin-top')
            styleAttributes += self.__addAttributeMM(style, 'margin-bottom', 'fo:margin-bottom')
            styleAttributes += self.__addAttributeMM(style, 'margin-left', 'fo:margin-left')
            styleAttributes += self.__addAttributeMM(style, 'margin-right', 'fo:margin-right')
 
            if styleAttributes <> '':
                styleStr = '<style:page-layout style:name="pm1">\n'
                styleStr += '<style:page-layout-properties ' + styleAttributes + '/>\n'
                styleStr += '</style:page-layout>\n'
#                   <style:header-style/> ???
#                   <style:footer-style/> ???
                return styleStr
    
    def __getPageSize(self, size, orientation):
        styleAttributes = ''
        if orientation == PageOrientationProperty.PORTRAIT:
            styleAttributes += 'fo:page-width="' + str(size.value[0]) + 'mm" '
            styleAttributes += 'fo:page-height="' + str(size.value[1]) + 'mm" ' 
        else:
            styleAttributes += 'fo:page-width="' + str(size.value[1]) + 'mm" '
            styleAttributes += 'fo:page-height="' + str(size.value[0]) + 'mm" ' 
            
        return styleAttributes
    
#    <style:page-layout-properties 
#    fo:page-width="9.9217in" 
#    fo:page-height="6.9291in" 
#    style:num-format="1" 
#    style:print-orientation="portrait" 
#    style:shadow="none" 
#    style:writing-mode="lr-tb" 
#    style:footnote-max-height="0in">
#   </style:page-layout-properties>

                
#_style[] = PageSizeProperty.A4
#_style[] = PageOrientationProperty.PORTRAIT
#_style[] = 20
# _style[] = 10
# _style[] = 20
# _style[] = 20
# _style[] = 12
# _style[] = "Times New Roman"
# _style[] = AlignmentProperty.LEFT
# _style[] = 0
# _style[] = "#000000"
# _style[] = "#ffffff"
# _style[] = ListStyleProperty.BULLET
# _style[] = 2
# _style[] = 12
# _style[] = True
# _style[] = 1
