# -*- coding: utf-8 -*-

class DocumentProperties(dict):
    """Class used for storing document properties. The common property names 
    are: "title", "keywords", "language".
    """
    
    pass

class Style(dict):
    """Class representing the element style.
    """
    
    def __init__(self, other=None):
        if other is not None:
            self.update(other)
        
    def __iadd__(self, other):
        if isinstance(other, ListStyleProperty):
            self['list-style'] = other
        elif isinstance(other, AlignmentProperty):
            self['alignment'] = other
        elif isinstance(other, PageOrientationProperty):
            self['page-orientation'] = other
        elif isinstance(other, FontEffectProperty):
            if ("font-effect"  not in self) or (self['font-effect'] is None):
                self['font-effect'] = other
            else:
                self['font-effect'] += other
        elif isinstance(other, BulletCharProperty):
            self['bullet-char'] = other
        elif isinstance(other, PageSizeProperty):
            self['page-size'] = other
        else:
            raise TypeError("Adding the property of this type is not \
                            supported!")
        
        return self
    
    def __isub__(self, other):
        if isinstance(other, FontEffectProperty):
            if ("font-effect" in self) and (self['font-effect'] is not None):
                self['font-effect'] -= other
        else:
            raise TypeError("Subtracting the property of this type is not \
                            supported!")

class DocumentTreeNode(object):
    """An abstract class containing the functionality common to all 
    document tree nodes (elements).
    """
    
    def __init__(self, content=None):
        if content is None:
            content = []
        self.parent = None
        self.style = Style()
        try:
            self.content = content
            if isinstance(self.content, str) or\
                                    isinstance(self.content, unicode):
                span = Span()
                span.text = self.content
                self.content = span
            if isinstance(self.content, DocumentTreeNode):
                self.content = [self.content]
        except AttributeError:
            pass
        
    def __iadd__(self, other):
        self.content.append(other)
        return self
        
    def __get_builder(self):
        return self.get_root().builder
    
    def get_root(self):
        """Get root of the document tree (document)."""
        
        node = self
        while node.parent is not None:
            node = node.parent  
        return node
            
    def __get_effective_style(self):        
        path = []
        node = self
        while node is not None:
            path = [node] + path
            node = node.parent
        style = Style()
        for node in path:
            if node.style is not None:
                style.update(node.style)   
        return style
    
    builder = property(__get_builder, None)
    effective_style = property(__get_effective_style, None)
    
    def fill_parent_fields(self):
        """Set "parent" attribute for every node in the document tree
        except from the root (document).
        """
        
        stack = []
        visited = {}
        curr_node = self
        
        stack.append(curr_node)
        
        while len(stack) > 0:
            first_child_not_visited = None
            for i in xrange(0, len(curr_node.content)):
                if (not visited.has_key(curr_node.content[i])):
                    first_child_not_visited = curr_node.content[i]
                    break
                
            if (first_child_not_visited is not None):
                first_child_not_visited.parent = curr_node
                visited[first_child_not_visited] = True
                stack.append(first_child_not_visited)
                curr_node = first_child_not_visited
            else:
                try:
                    for span in curr_node.caption:
                        span.parent = curr_node
                except AttributeError:
                    pass
                stack.pop()
                if (len(stack) > 0):
                    curr_node = stack[-1]
                    
    def successor_isinstance(self, req_type):
        """Determine whether one of the node successors is instance of
        req_type and return bool value.
        """
        
        result = False
        stack = []
        visited = {}
        curr_node = self
        
        stack.append(curr_node)
        
        while len(stack) > 0:
            first_child_not_visited = None
            for i in xrange(0, len(curr_node.content)):
                if (not visited.has_key(curr_node.content[i])):
                    first_child_not_visited = curr_node.content[i]
                    break
             
            if (first_child_not_visited is not None):
                visited[first_child_not_visited] = True
                stack.append(first_child_not_visited)
                curr_node = first_child_not_visited
            else:
                if isinstance(curr_node, req_type):
                    result = True
                    break
                stack.pop()
                if (len(stack) > 0):
                    curr_node = stack[-1]
                    
        return result
    
    def reset_sequences(self):
        """Reset sequence for every element in the document tree."""
        
        stack = []
        visited = {}
        curr_node = self
        
        stack.append(curr_node)
        
        while len(stack) > 0:
            first_child_not_visited = None
            for i in xrange(0, len(curr_node.content)):
                if (not visited.has_key(curr_node.content[i])):
                    first_child_not_visited = curr_node.content[i]
                    break
             
            if (first_child_not_visited is not None):
                visited[first_child_not_visited] = True
                stack.append(first_child_not_visited)
                curr_node = first_child_not_visited
            else:
                if isinstance(curr_node, NumberedObject) and\
                                curr_node.sequence is not None:
                    curr_node.sequence.reset()
                stack.pop()
                if (len(stack) > 0):
                    curr_node = stack[-1]
                
    def generate(self):
        """Generate output code and return is as a string"""
        
        return self.builder.generate(self)
    
    def is_style_property_set(self, style_property):
        """Check whether the element's effective style has defined
        style_property style property and return bool result.
        """
        
        return (self.effective_style.has_key(style_property)) and\
                (self.effective_style[style_property] is not None)

class Document(DocumentTreeNode):
    """Class representing the document.
    """
    
    builder = None
    
    def __init__(self, content=None):
        if content is None:
            content = []
        super(Document, self).__init__(content)
        self.style = StyleManager().get_style('doc-default')
        self.properties = DocumentProperties()
        self.builder = None
        
    def generate_file(self, path):
        """Generate output code and save it to file.
        """
        
        if self.builder is not None:
            output = self.generate()
            output_file = open(path, "w")            
            output_file.write(output.encode("utf-8"))
            output_file.close()
        else:
            raise Exception("The document has no builder!")
        
    def __iadd__(self, other):
        if isinstance(other, str) or isinstance(other, unicode):
            other = Span(other)
        if isinstance(other, Span):
            other = Paragraph(other)

        return super(Document, self).__iadd__(other)
        

class Paragraph(DocumentTreeNode):
    """Class representing the paragraph.
    """
    
    def __init__(self, content=None):
        if content is None:
            content = []
        super(Paragraph, self).__init__(content)
        self.style = StyleManager().get_style('paragraph-default')
        
    def __iadd__(self, other):
        if isinstance(other, str) or isinstance(other, unicode):
            other = Span(other)

        return super(Paragraph, self).__iadd__(other)

class Span(DocumentTreeNode):
    """Class representing the span.
    """
    
    def __init__(self, text=None):
        super(Span, self).__init__()
        self.text = text

class List(DocumentTreeNode):
    """Class representing the list.
    """
    
    def __init__(self, content=None):
        if content is None:
            content = []
        super(List, self).__init__(content)
        self.style = StyleManager().get_style('list-default')
        
    def __iadd__(self, other):
        if isinstance(other, str) or isinstance(other, unicode):
            other = Span(other)

        return super(List, self).__iadd__(other)

class Sequence(object):
    """Class representing the sequence.
    """
    
    def __init__(self, start_value=1, parent=None):
        self.__start_value = start_value
        self.__value = start_value
        self.parent = parent
        
    def advance(self):
        """Increase sequence value by 1.
        """
        
        self.__value += 1
        return self.__value
    
    def to_str(self, separator="."):
        """Convert sequence value to string, taking into account parent
        sequences.
        """
        
        seq = self
        result = str(seq.value)
        
        while seq.parent is not None:
            seq = seq.parent
            result = str(seq.value - 1) + separator + result
        return result
    
    def __set_value(self, value):
        self.__start_value = value;
        self.__value = value
        
    def __get_value(self):
        return self.__value
    
    def reset(self):
        """Reset the sequence to the initial value."""
        
        self.__value = self.__start_value
    
    def get_numbers(self):
        """Return a list of sequence values starting from the least 
        significant.
        """
        
        seq = self
        numbers = [str(seq.value - 1)]
        
        while seq.parent is not None:
            seq = seq.parent
            numbers.append(str(seq.value - 1))
         
        return numbers
    
    def get_level(self):
        """Return level of the sequence.
        """
        
        seq = self
        level = 0
        
        while seq.parent is not None:
            seq = seq.parent
            level += 1
         
        return level
        
    def __str__(self):
        return self.to_str()
    
    value = property(__get_value, __set_value)

class NumberedObject(DocumentTreeNode):
    """An abstract class which is a base for all document elements that are 
    numbered by using a sequence.
    """
    
    def __init__(self, content=None, sequence=None):
        if content is None:
            content = []
        super(NumberedObject, self).__init__(content)
        self.sequence = sequence

class Header(NumberedObject):
    """Class representing the header.
    """
    
    def __init__(self, content=None, sequence=None):
        if content is None:
            content = []
        super(Header, self).__init__(content, sequence)
        self.style = StyleManager().get_style('header-default')
        self.sequence 
        
class CaptionedObject(NumberedObject):
    def __init__(self, sequence=None):
        super(CaptionedObject, self).__init__(sequence=sequence)
        self.__caption = []
    
    def __get_caption(self):
        return self.__caption
    
    def __set_caption(self, caption):
        if caption is None:
            caption = []
        else:
            if (not isinstance(caption, list)) and\
                        (not isinstance(caption, Span)) and\
                        (not isinstance(caption, str)) and\
                        (not isinstance(caption, unicode)):
                raise TypeError("Caption needs to be a string, \
                                            Span or list of Span!")
            if isinstance(caption, list):
                self.__caption = caption
            if isinstance(caption, str) or isinstance(caption, unicode):
                self.__caption = [Span(caption)]
            else:
                self.__caption = [caption]
        
    caption = property(__get_caption, __set_caption)

class Image(CaptionedObject):
    """Class representing the image.
    """
    
    def __init__(self, path=None, sequence=None):
        super(Image, self).__init__(sequence=sequence)
        self.path = path
        self.style = StyleManager().get_style("image-default")
        
class TableCell(DocumentTreeNode):
    """Class representing a cell of the table. It is used internally by the
    Table class.
    """
    
    def __init__(self):
        super(TableCell, self).__init__()
        self.rowspan = 1
        self.colspan = 1
        
    def __iadd__(self, other):
        if isinstance(other, str) or isinstance(other, unicode):
            other = Span(other)

        return super(TableCell, self).__iadd__(other)

class Table(CaptionedObject):
    """Class representing the table.
    """
    
    __default_row_height = 20
    __default_column_width = 100
    
    def __init__(self, rows_num=1, cols_num=1, sequence=None):
        super(Table, self).__init__(sequence=sequence)
        self.__rows = [[TableCell()]]
        self.__rowHeights = [self.__default_row_height]
        self.__columnWidths = [self.__default_column_width]
        self.caption = None
        self.style = StyleManager().get_style("table-default")
        
        if rows_num > 1:
            self.append_row(rows_num - 1)
            
        if cols_num > 1:
            self.append_column(cols_num - 1)
            
    def __get_rows_num(self):
        return len(self.__rows)
        
    def __get_cols_num(self):
        return len(self.__rows[0])
    
    def __create_row(self):
        row = []
        for _ in xrange(0, self.cols_num):
            row.append(TableCell())
        return row
    
    def get_cell(self, row, column):
        """Get cell in given row and column."""
        
        return (self.__rows[row])[column]
        
    def insert_row(self, index, count=1):
        """Insert a row at the index position."""
        
        for _ in xrange(0, count):
            row = self.__create_row()
            self.__rows.insert(index, row)
            self.__rowHeights.insert(index, self.__default_row_height)
        
    def append_row(self, count=1):
        """Insert a row at the end of the table."""
        
        self.insert_row(self.rows_num, count)
        
    def delete_row(self, index, count=1):
        """Delete the row at the index position."""
        
        for _ in xrange(0, count):
            if (self.rows_num > 1):
                del self.__rows[index]
                del self.__rowHeights[index]
            else:
                self.__rows[0] = self.__create_row()
                self.__rowHeights[0] = self.__default_row_height
        
    def insert_column(self, index, count=1):
        """Insert a column at the index position."""
        
        for _ in xrange(0, count):
            for row in self.__rows:
                row.insert(index, TableCell())
            self.__columnWidths.insert(index, self.__default_column_width)
            
    def append_column(self, count=1):
        """Insert a column at the end of the table."""
        
        self.insert_column(self.cols_num, count)
        
    def delete_column(self, index, count=1):
        """Delete the column at the index position."""
        
        for _ in xrange(0, count):
            if (self.cols_num > 1):
                for row in self.__rows:
                    del row[index]
                del self.__columnWidths[index]
            else:
                for row in self.__rows:
                    row[0] = TableCell()
                self.__columnWidths[0] = self.__default_column_width
            
    def get_row_height(self, index):
        """Return row height"""
        
        return self.__rowHeights[index]
    
    def set_row_height(self, index, height):
        """Set row height."""
        
        self.__rowHeights[index] = height
        
    def get_column_width(self, index):
        """Return column width."""
        
        return self.__columnWidths[index]
    
    def set_column_width(self, index, width):
        """Set column width."""
        
        self.__columnWidths[index] = width
    
    def __get_content(self):
        content = []
        for i in xrange(0, self.rows_num):
            content.extend(self.__rows[i])
        return content
        
    rows_num = property(__get_rows_num, None)
    cols_num = property(__get_cols_num, None)
    content = property(__get_content, None)

class Property(object):
    """An abstract class which is a base for some special, predefined properties
    of document elements stored in a style.
    """
    
    def __init__(self, value):
        self.value = value
        
    def __eq__(self, other):
        return self.value == other.value
    
    def __hash__(self):
        return hash(self.value)

class ListStyleProperty(Property):
    """Class representing the "list-style" property of the list style.
    """
    
    BULLET = None
    NUMBER = None
        
ListStyleProperty.BULLET = ListStyleProperty(0)
ListStyleProperty.NUMBER = ListStyleProperty(1)

class AlignmentProperty(Property):
    """Class representing the "alignment" property of the document element 
    style.
    """
    
    LEFT = None
    CENTER = None
    RIGHT = None
    JUSTIFY = None

AlignmentProperty.LEFT = AlignmentProperty(0)
AlignmentProperty.CENTER = AlignmentProperty(1)
AlignmentProperty.RIGHT = AlignmentProperty(2)
AlignmentProperty.JUSTIFY = AlignmentProperty(3)

class PageOrientationProperty(Property):
    """Class representing the "page-orientation" property of the document 
    style.
    """
    
    PORTRAIT = None
    LANDSCAPE = None

PageOrientationProperty.PORTRAIT = PageOrientationProperty(0)
PageOrientationProperty.LANDSCAPE = PageOrientationProperty(1)

class FontEffectProperty(Property):
    """Class representing the font effect of the span which is set by the
    "font-effect" style property. A few style effects can be combined and 
    assigned to the style by adding few FontEffectProperty objects 
    ("+" operator).
    """
    
    BOLD = None
    ITALIC = None
    UNDERLINE = None
    
    def __add__(self, other):
        return FontEffectProperty(self.value | other.value)
    
    def __iadd__(self, other):
        self.value |= other.value
        return self
    
    def __isub__(self, other):
        self.value &= ~(other.value)
        
    def __contains__(self, font_effect):
        return bool(self.value & font_effect.value)
    
FontEffectProperty.BOLD = FontEffectProperty(1)
FontEffectProperty.ITALIC = FontEffectProperty(2)
FontEffectProperty.UNDERLINE = FontEffectProperty(4)

class BulletCharProperty(Property):
    """Class representing a special value of the "bullet-char" property of 
    the list style.
    """
    
    BULLET = None
    CDOT = None
    DIAMOND = None
    ASTERISK = None
    CIRCLE = None
    MEDIUM_HYPHEN = None
    LONG_HYPHEN = None

BulletCharProperty.BULLET = BulletCharProperty(0)
BulletCharProperty.CDOT = BulletCharProperty(1)
BulletCharProperty.DIAMOND = BulletCharProperty(2)
BulletCharProperty.ASTERISK = BulletCharProperty(3)
BulletCharProperty.CIRCLE = BulletCharProperty(4)
BulletCharProperty.MEDIUM_HYPHEN = BulletCharProperty(5)
BulletCharProperty.LONG_HYPHEN = BulletCharProperty(6)

class PageSizeProperty(Property):
    """Class containing some predefined values of the "page-size" property of 
    the document style.    
    """
    
    A4 = None
    A5 = None
    B4 = None
    B5 = None
    LETTER = None

PageSizeProperty.A4 = PageSizeProperty((210, 297))
PageSizeProperty.A5 = PageSizeProperty((148, 210))
PageSizeProperty.B4 = PageSizeProperty((250, 353))
PageSizeProperty.B5 = PageSizeProperty((176, 250))
PageSizeProperty.LETTER = PageSizeProperty((215.9, 279.4))

class StyleManager(object):
    """A style manager class which uses the Borg pattern to preserve its 
    state. 
    
    The style manager is used to store a dictionary of standard, predefined 
    styles identified by their name. 
    """
    
    __shared_state = {}
    __styles = {}
    
    def __init__(self):
        self.__dict__ = self.__shared_state
        
    def set_style(self, style_name, style):
        self.__styles[style_name] = style
        
    def get_style(self, style_name):
        return Style(self.__styles[style_name])

# Below there are standard styles defined.

_style_manager = StyleManager()

# default document style
_style = Style()
_style['page-numbering'] = True
_style['page-size'] = PageSizeProperty.A4
_style['page-orientation'] = PageOrientationProperty.PORTRAIT
_style['margin-top'] = 20
_style['margin-bottom'] = 10
_style['margin-left'] = 20
_style['margin-right'] = 20
_style['font-size'] = 12
_style['font-name'] = "Times New Roman"
_style['alignment'] = AlignmentProperty.LEFT
_style['text-indent'] = 0
_style['color'] = "#000000"
_style['background-color'] = "#ffffff"
_style['list-style'] = ListStyleProperty.BULLET
_style['item-spacing'] = 2
_style['item-indent'] = 12
_style['header-numbered'] = True
_style['border-width'] = 1
_style_manager.set_style('doc-default', _style)

#default header style
_style = Style()
_style['border-width'] = 0
_style['margin-top'] = 10
_style['margin-bottom'] = 10
_style['margin-left'] = 0
_style['margin-right'] = 0
_style['font-size'] = 14
_style_manager.set_style('header-default', _style)

#default paragraph style
_style = Style()
_style['margin-top'] = 0
_style['margin-bottom'] = 0
_style['margin-left'] = 0
_style['margin-right'] = 0
_style_manager.set_style('paragraph-default', _style)

#default image style
_style = Style()
_style['margin-top'] = 0
_style['margin-bottom'] = 0
_style['margin-left'] = 0
_style['margin-right'] = 0
_style_manager.set_style('image-default', _style)

#default table style
_style = Style()
_style['margin-top'] = 0
_style['margin-bottom'] = 0
_style['margin-left'] = 0
_style['margin-right'] = 0
_style_manager.set_style('table-default', _style)

#default list style
_style = Style()
_style['margin-top'] = 0
_style['margin-bottom'] = 2
_style['margin-left'] = 30
_style['margin-right'] = 0
_style_manager.set_style('list-default', _style)
    
