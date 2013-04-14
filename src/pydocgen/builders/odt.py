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
        self.__styleManager = OdtStyleManager(document)
        
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
            styleBody = self.__styleManager.getParagraphStyles(paragraph.style)

        if styleBody <> '':
            self.paragraphStyles[self.styleIndex] = styleBody
            result = '        <text:p text:style-name="' + str(self.styleIndex) + '">' + p + '</text:p>\n'
            self.styleIndex += 1
        else:
            result = '        <text:p>' + p + '</text:p>\n'

        return result
    
    def generate_span(self, span):

        resolved = self.__resolveTextStyle(span);

        if resolved:
            result = '<text:span text:style-name="' + str(self.styleIndex) + '">' + span.text + '</text:span>'
            self.styleIndex += 1
        else:
            result = '<text:span>' + span.text + '</text:span>'
        
        return result
    
    def __resolveTextStyle(self, elem):
        if isinstance(elem, str) or isinstance(elem, unicode):
                return ''
        style = elem.style
        
        styleBody = ''
   
        if style is not None:
            styleBody = self.__styleManager.getTextStyles(style)     
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
        
        return '        <text:h text:outline-level="' + seq_number + '">' + seq_number + " " + content + '</text:h>\n'
    
    def generate_list(self, el):
        return ''
    
    def generate_image(self, el):
        return ''
    
    def generate_table(self, el):
        return ''
    
    def __resolveDocumentStyle(self, style):
        return self.__resolvePageLayout(style)
                
    def __resolvePageLayout(self, style):
        if style is not None:
            styleAttributes = ''
            orientation = None
            size = None
            
            styleAttributes = self.__styleManager.getPageLayoutStyles()
 
            if styleAttributes <> '':
                styleStr  = '        <style:page-layout style:name="pm1">\n'
                styleStr += '            <style:page-layout-properties ' + styleAttributes + '/>\n'
                styleStr += '        </style:page-layout>\n'
#                   <style:header-style/> ???
#                   <style:footer-style/> ???
                return styleStr

        return ''

                
#_style[] = PageSizeProperty.A4
#_style[] = PageOrientationProperty.PORTRAIT
#_style[] = 20
# _style[] = 10font_effects = style['font-effect']
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

class OdtStyleManager(object):
    def __init__(self, document):
        self.__effective_style = document.effective_style
        
        self.__defaultTextIndent = None
        self.__defaultFontSize = None
        self.__defaultFontName = None
        self.__defaultAlignment = None
        self.__defaultColor = None
        self.__defaultBackgroundColor = None
        self.__defaultListStyle = None
        self.__defaultItemSpacing = None
        self.__defaultItemIndent = None
        self.__defaultBorderWidth = None
        
        self.__pageSize = self.__getStyleValue(self.__effective_style, 'page-size')
        self.__orientation = self.__getStyleValue(self.__effective_style, 'page-orientation')
        self.__defaultAlignment = self.__getStyleValue(self.__effective_style, 'alignment')
        
        self.__defaultTextIndent = self.getTextIndent(self.__effective_style)
        self.__defaultFontSize = self.getFontSize(self.__effective_style)
        self.__defaultFontName = self.getFontName(self.__effective_style)
        self.__defaultColor = self.getColor(self.__effective_style)
        self.__defaultBackgroundColor = self.getBackgroundColor(self.__effective_style)
        self.__defaultListStyle = self.getListStyle(self.__effective_style)
        self.__defaultItemSpacing = self.getItemSpacing(self.__effective_style)
        self.__defaultItemIndent = self.getItemIndent(self.__effective_style)
        self.__defaultBorderWidth = self.getBorderWidth(self.__effective_style)
        
    def getMarginTop(self, style):
        return self.__getAttributeMM(style, 'margin-top', 'fo:margin-top');
    
    def getMarginBottom(self, style):
        return self.__getAttributeMM(style, 'margin-bottom', 'fo:margin-bottom');
    
    def getMarginLeft(self, style):
        return self.__getAttributeMM(style, 'margin-left', 'fo:margin-left');
    
    def getMarginRight(self, style):
        return self.__getAttributeMM(style, 'margin-right', 'fo:margin-right');
    
    def getTextIndent(self, style):
        return self.__getAttributeMMOrDefault(style, 'text-indent', 'fo:text-indent', self.__defaultTextIndent)
    
    def getFontSize(self, style):
        return self.__getAttributePTOrDefault(style, 'font-size', 'TODO', self.__defaultFontSize)

    def getFontName(self, style):
        return self.__getAttributeOrDefault(style, 'font-name', 'TODO', self.__defaultFontName)
    
    def getAlignment(self, style):
        alignment = self.__getStyleValueOrDefault(style, 'alignment', self.__defaultAlignment)
        if alignment is None:
            return ''
        else:
            if alignment == AlignmentProperty.LEFT:
                return '' # left is default
            elif alignment == AlignmentProperty.CENTER:
                return 'fo:text-align="center" '
            elif alignment == AlignmentProperty.RIGHT:
                return 'fo:text-align="end" '
            elif alignment == AlignmentProperty.JUSTIFY:
                return 'fo:text-align="justify" '
            else:
                return ''
    
    def getColor(self, style):
        return self.__getAttributeOrDefault(style, 'color', 'TODO', self.__defaultColor)
    
    def getBackgroundColor(self, style):
        return self.__getAttributeOrDefault(style, 'background-color', 'TODO', self.__defaultBackgroundColor)
    
    def getListStyle(self, style):
        return self.__getAttributeOrDefault(style, 'list-style', 'TODO', self.__defaultListStyle)
    
    def getItemSpacing(self, style):
        return self.__getAttributeMMOrDefault(style, 'item-spacing', 'TODO', self.__defaultItemSpacing)
    
    def getItemIndent(self, style):
        return self.__getAttributeMMOrDefault(style, 'item-indent', 'TODO', self.__defaultItemIndent)
    
    def getHeaderNumbered(self, style):
        return self.__getStyleValue(style, 'header-numbered')
    
    def getBorderWidth(self, style):
        return self.__getAttributeOrDefault(style, 'border-width', 'TODO', self.__defaultBorderWidth)
    
    def getPageNumbering(self, style):
        return self.__getAttribute(style, 'page-numbering', 'TODO', 'TODO')
    
    def getFontEffect(self, style):
        font_effects = self.__getStyleValue(style, 'font-effect')
        styleBody = ''
        if font_effects is not None:
            if FontEffectProperty.BOLD in font_effects:
                styleBody += 'fo:font-weight="bold" style:font-weight-asian="bold" style:font-weight-complex="bold" '
            if FontEffectProperty.ITALIC in font_effects:
                styleBody += 'fo:font-style="italic" style:font-style-asian="italic" style:font-style-complex="italic" '
            elif FontEffectProperty.UNDERLINE in font_effects:
                styleBody += 'style:text-underline-style="solid" style:text-underline-width="auto" style:text-underline-color="font-color" '
        return styleBody
    
    def getPageSize(self, style):
        styleAttributes = ''
        if self.__orientation == PageOrientationProperty.PORTRAIT:
            styleAttributes += 'fo:page-width="' + str(self.__pageSize.value[0]) + 'mm" '
            styleAttributes += 'fo:page-height="' + str(self.__pageSize.value[1]) + 'mm" ' 
        else:
            styleAttributes += 'fo:page-width="' + str(self.__pageSize.value[1]) + 'mm" '
            styleAttributes += 'fo:page-height="' + str(self.__pageSize.value[0]) + 'mm" ' 
            
        return styleAttributes
    
    def getPageOrientation(self, style):
        if self.__orientation == PageOrientationProperty.PORTRAIT:
            return 'style:print-orientation="portrait" '
        else:
            return 'style:print-orientation="landscape" '
        
    def getParagraphStyles(self, style):
        return self.getTextIndent(style) + self.getMarginBottom(style) \
                + self.getMarginLeft(style) + self.getMarginRight(style) \
                + self.getMarginTop(style) + self.getAlignment(style)
    
    def getTextStyles(self, style):
        return self.getFontEffect(style)
    
    def getPageLayoutStyles(self):
        style = self.__effective_style
        return self.getPageNumbering(style) + self.getPageSize(style) \
                + self.getPageOrientation(style) + self.getMarginTop(style)\
                + self.getMarginBottom(style) + self.getMarginLeft(style)\
                + self.getMarginRight(style)
    
    def __getAttributeOrDefault(self, style, name, nativeName, default):
        return self.__getAttributeWithSuffixOrDefault(style, name, nativeName, default, '')
    
    def __getAttributePTOrDefault(self, style, name, nativeName, default):
        return self.__getAttributeWithSuffixOrDefault(style, name, nativeName, default, 'pt')
    
    def __getAttributeMMOrDefault(self, style, name, nativeName, default):
        return self.__getAttributeWithSuffixOrDefault(style, name, nativeName, default, 'mm')
    
    def __getAttributeWithSuffixOrDefault(self, style, name, nativeName, default, valueSuffix):
        att = self.__getAttribute(style, name, nativeName, valueSuffix)
        if att == '':
            if default is None:
                return ''
            else:
                return default
        else:
            return att
    
    def __getStyleValueOrDefault(self, style, name, default):
        value = self.__getStyleValue(style, name)
        if value is None:
            if default is None:
                return ''
            else:
                return default
        else:
            return value
    
    def __getStyleValue(self, style, name):
        value = None
        if style.has_key(name):
            value = style[name]
        return value
        
    def __getAttributeMM(self, style, name, nativeName):
        return self.__getAttribute(style, name, nativeName, 'mm')
    
    def __getAttribute(self, style, name, nativeName, valueSuffix):
        att = ''
        if style.has_key(name):
            value = str(style[name]) + valueSuffix
            att = nativeName + '="' + value + '" '
        return att