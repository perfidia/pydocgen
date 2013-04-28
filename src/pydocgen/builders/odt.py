# -*- coding: utf-8 -*-

from pydocgen.model import ListStyleProperty, AlignmentProperty, FontEffectProperty, Image, Style, Table
from pydocgen.builders.common import Builder
from pydocgen.model import PageOrientationProperty
from pydocgen.model import Property


class OdtBuilder(Builder):

    def __init__(self):
        super(OdtBuilder, self).__init__()

        self.extension = "fodt"

    def generate_document(self, document):
        self.styles = dict()
        self.styleIndex = 0
        self.tableNameIndex = 0
        self.__styleManager = OdtStyleManager(document)
        
        body = ''
        meta= ''

        for element in document.content:
            body += self.generate(element)
            
        # styles.xml file
         
        styles = '    <office:automatic-styles>\n'
        if self.styles is not None:
            for key in self.styles.keys():
                if type(self.styles[key]) == OdtStyle :               
                    styles += self.styles[key].toString()
                else: 
                    styles += self.styles[key]
        styles += self.__resolveDocumentStyle(document.effective_style)
        styles += '    </office:automatic-styles>\n'
        styles += '    <office:master-styles>\n'
        styles += '        <style:master-page style:name="Standard" style:page-layout-name="pm1"/>\n'
        styles += '    </office:master-styles>' 

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
        result += '    xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0\"\n'
        result += '    xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"\n'
        result += '    xmlns:xlink="http://www.w3.org/1999/xlink"\n'
        result += '    xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"\n'
        result += '    xmlns:tableooo="http://openoffice.org/2009/table"\n'
        result += '    office:version="1.2" \n'
        result += '    office:mimetype="application/vnd.oasis.opendocument.text">\n' 
        result += styles
        result += '<office:body>\n'
        result += '       <office:text>\n'
        result += body
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
            styleObj = OdtStyle(str(self.styleIndex), OdtStyleFamily.PARAGRAPH, styleBody, None)
            self.styles[self.styleIndex] = styleObj
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
            styleObj = OdtStyle(str(self.styleIndex), OdtStyleFamily.TEXT, None, styleBody)  
            self.styles[self.styleIndex] = styleObj
                    
        if styleBody <> '':
            return True
        else:
            return False;
    
    def generate_header(self, header):
        content = ''
        # assume header has no inner elements, just text
        element = header.content[0]
        content = element.text
#        if header.content:~    
#            for element in header.content:
#                if element:
#                    content += element.generate()

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
        
        styleObj = None
        if header.style is not None:
            textStyle = self.__styleManager.getTextStyles(header.style)
            paragraphStyle = self.__styleManager.getParagraphStyles(header.style)
            styleObj = OdtStyle(str(self.styleIndex), OdtStyleFamily.PARAGRAPH, paragraphStyle, textStyle)  
            self.styles[self.styleIndex] = styleObj
        
        if styleObj is None:
            result = '        <text:h text:outline-level="' + seq_number \
                    + '">' + seq_number + " " + content + '</text:h>\n'
        else:
            result = '        <text:h text:outline-level="' + seq_number \
                    + '" text:style-name="' + str(self.styleIndex) + '">' \
                    + seq_number + " " + content + '</text:h>\n'
            self.styleIndex += 1
        
        return result
    
    def generate_list(self, list):
        styleObj = self.__styleManager.getListStyles(list.style, self.styleIndex)
        self.styles[self.styleIndex] = styleObj           
        
        result = ''
        result += '<text:list text:style-name="' + str(self.styleIndex) + '">\n'
        
        self.styleIndex += 1
        
        for item in list.content:
            result += '<text:list-item>\n'
            result += '<text:p text:style-name="P1">'
            result += self.generate(item)
            result += '</text:p>\n'
            result += '</text:list-item>\n'    
            
        result += '</text:list>\n\n'   
   
        return result
    
    def generate_image(self, image):
        
        f = open(image.path, "rb")
        line = f.readline()
        bytes = ''
        while line <> '':
            bytes += line
            line = f.readline()
        
        styles = self.__styleManager.getImageStyles(image.style)

        imageStr  = '            <draw:frame text:anchor-type="as-char" ' + styles + '>\n'
        imageStr += '                <draw:image xlink:href="' + image.path + '" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad" />\n'
        imageStr += '            </draw:frame>\n'
        
        styleBody = ''
        
        if image.style is not None:
            styleBody = self.__styleManager.getParagraphStyles(image.style)

        if styleBody <> '':
            styleObj = OdtStyle(str(self.styleIndex), OdtStyleFamily.PARAGRAPH, styleBody, None)
            self.styles[self.styleIndex] = styleObj
            result = '        <text:p text:style-name="' + str(self.styleIndex) + '">\n' + imageStr + '</text:p>\n'
            self.styleIndex += 1
        else:
            result = '        <text:p>\n' + imageStr + '</text:p>\n'

        return result
    
    def generate_table(self, table):
        result = '\n<table:table table:name="Tabela' + str(self.tableNameIndex) +'" table:style-name="Tabela1">'
        result += '<table:table-column table:style-name="Tabela1" table:number-columns-repeated="2"/>'
        for i in xrange(0, table.rows_num):
            result += '\n<table:table-row office:value-type="string">'
            for j in xrange(0, table.cols_num):
                result += '\n<table:table-cell table:style-name="Tabela1">'
                result += '<text:p text:style-name="P1">'
                for k in table.get_cell(i, j).content:
                    result += self.generate(k)
                result += '</text:p>'
                result += '</table:table-cell>'                
            result += '\n</table:table-row>\n'
            
        result += '\n</table:table>'
        
        self.tableNameIndex += 1
        
        return  result
    
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
#_style[] = 20y
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

# <style:style style:name="Tabela1" style:family="table"><style:table-properties style:width="16.999cm" table:align="margins"/></style:style>

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
        return self.__getAttributePTOrDefault(style, 'font-size', 'fo:font-size', self.__defaultFontSize)

    def getFontName(self, style):
        return self.__getAttributeOrDefault(style, 'font-name', 'style:font-name', self.__defaultFontName)
    
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
        return self.__getAttributeOrDefault(style, 'color', 'fo:color', self.__defaultColor)
    
    def getBackgroundColor(self, style):
        return self.__getAttributeOrDefault(style, 'background-color', 'fo:background-color', self.__defaultBackgroundColor)
    
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
            if FontEffectProperty.UNDERLINE in font_effects:
                styleBody += 'style:text-underline-style="solid" style:text-underline-width="auto" style:text-underline-color="font-color" '
            if FontEffectProperty.STRIKE in font_effects:
                styleBody += 'style:text-line-through-style="solid" '
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
        
    def getWidth(self, style):
        return self.__getAttributeMM(style, "width", "svg:width")
    
    def getHeight(self, style):
        return self.__getAttributeMM(style, "height", "svg:height")
        
    def getParagraphStyles(self, style):
        return self.getTextIndent(style) + self.getMarginBottom(style) \
                + self.getMarginLeft(style) + self.getMarginRight(style) \
                + self.getMarginTop(style) + self.getAlignment(style) \
                + self.getFontSize(style)
                
    def getListStyles(self, style, number):    
        elmStart = ''
        elmEnd = ''   
        textLevel = 1    
        stopPosition = 1.27
        
        result = ''
        result += '<text:list-style style:name="' + str(number) + '">\n'
        
        if 'list-style' in style.keys() and style['list-style'] == ListStyleProperty.NUMBER:
            for styleObj in style.keys():
                result += '<text:list-level-style-number text:level="' + str(textLevel) + '" style:num-suffix="." style:num-format="1">\n'
                result += '<style:list-level-properties text:list-level-position-and-space-mode="label-alignment">\n'
                result += '<style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="' + str(stopPosition) + \
                            'cm" fo:text-indent="-0.635cm" fo:margin-left="' + str(stopPosition) +'cm"/>\n'
                result += '</style:list-level-properties>\n'
                result += '</text:list-level-style-number>\n'
                
                textLevel += 1
                stopPosition += 0.635
        else:
            for styleObj in style.keys():
                result += '<text:list-level-style-bullet text:level="' + str(textLevel) +'" text:style-name="Bullet_20_Symbols" text:bullet-char="•">\n'
                result += '<style:list-level-properties text:list-level-position-and-space-mode="label-alignment">\n'
                result += '<style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="' + str(stopPosition) + \
                            'cm" fo:text-indent="-0.635cm" fo:margin-left="' + str(stopPosition) +'cm"/>\n'
                result += '</style:list-level-properties>\n'
                result += '<style:text-properties fo:font-family="StarSymbol" style:font-charset="x-symbol"/>\n'
                result += '</text:list-level-style-bullet>\n'
                
                textLevel += 1
                stopPosition += 0.635
                
        result += '</text:list-style>\n'
                
        return result
    
    def getTextStyles(self, style):
        return self.getFontEffect(style) + self.getFontSize(style) \
                + self.getFontName(style) + self.getColor(style) \
                + self.getBackgroundColor(style)
    
    def getPageLayoutStyles(self):
        style = self.__effective_style
        return self.getPageNumbering(style) + self.getPageSize(style) \
                + self.getPageOrientation(style) + self.getMarginTop(style)\
                + self.getMarginBottom(style) + self.getMarginLeft(style)\
                + self.getMarginRight(style)
                
    def getImageStyles(self, style):
        return self.getWidth(style) + self.getHeight(style);
    
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
    
class OdtStyle(object):
    def __init__(self, name, family, paragraphAttributes, textAttributes):
        self.name = name
        self.family = family
        self.paragraphAttributes = paragraphAttributes
        self.textAttributes = textAttributes
        
    def toString(self):
        style  = '        <style:style style:name="' + str(self.name) + '" style:family="' + str(self.family.value) + '">\n'
        if self.textAttributes is not None:
            style += '            <style:text-properties ' + self.textAttributes + '/>\n'
        if self.paragraphAttributes is not None:
            style += '            <style:paragraph-properties ' + self.paragraphAttributes + '/>\n'
        style += '        </style:style>\n'
        return style
        
class OdtStyleFamily(Property):
    TEXT = None
    PARAGRAPH = None

OdtStyleFamily.TEXT = OdtStyleFamily('text')
OdtStyleFamily.PARAGRAPH = OdtStyleFamily('paragraph')
    
        