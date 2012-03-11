# -*- coding: utf-8 -*-

class DocumentProperties(dict):
    pass


class Style(dict):
    def __init__(self):
        self.name = None
        

class DocumentTreeNode(object):
    def __init__(self):
        self.parent = None
        self.style = None
        try:
            self.content = [] # of DocumentTreeNode
        except AttributeError:
            pass
        
    def __iadd__(self, other):
        self.content.append(other)
        return self
        
    def __get_builder(self):
        return self.get_root().builder
    
    def get_root(self):
        node = self
        while node.parent is not None:
            node = node.parent  
        return node
            
    def __get_effective_style(self):        
# THIS DOESN'T WORK !!!
#        parent_style = Style()
#        if self.parent == None: # doc tree root
#            return self.style if self.style else StyleManager().get_style('doc-default')
#        else:
#            parent_style = self.parent.get_effective_style().copy()
#        parent_style.update(self.style) #Do not trying do this in one line
#        return parent_style        #dict's update method returns void!

# IT WAS THAT SIMPLE
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
                stack.pop()
                if (len(stack) > 0):
                    curr_node = stack[-1]
                    
    def successor_isinstance(self, req_type):
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
                
    def generate(self):
        return self.builder.generate(self)
    
    def is_style_element_set(self, style_element):
        return (self.effective_style.has_key(style_element)) and\
                (self.effective_style[style_element] is not None)
    

class Document(DocumentTreeNode):
    builder = None
    
    def __init__(self):
        super(Document, self).__init__()
        self.style = StyleManager().get_style('doc-default')
        self.properties = DocumentProperties()
        self.builder = None
        
    def generate_file(self, path):
        if self.builder is not None:
            output = self.generate()
            output_file = open(path, "w")
            output_file.write(output)
            output_file.close()
        else:
            raise Exception("The document has no builder!")
        
        
class Paragraph(DocumentTreeNode):
    def __init__(self):
        super(Paragraph, self).__init__()
        self.style = StyleManager().get_style('par-default')


class Span(DocumentTreeNode):
    def __init__(self, text = None):
        super(Span, self).__init__()
        self.text = text
        

class List(DocumentTreeNode):
    def __init__(self):
        super(List, self).__init__()
        self.style = StyleManager().get_style('list-default')


class Sequence(object):
    def __init__(self, start_value = 1, parent = None):
        self.value = start_value
        self.parent = parent
        
    def advance(self):
        self.value += 1
        return self.value
    
    def to_str(self, separator = "."):
        seq = self
        result = str(seq.value)
        
        while seq.parent is not None:
            seq = seq.parent
            result = str(seq.value) + separator + result
     
        return result
    
    def __str__(self):
        return self.to_str()
    

class NumberedObject(DocumentTreeNode):
    def __init__(self):
        super(NumberedObject, self).__init__()
        self.sequence = None
        
        
class Header(NumberedObject):
    def __init__(self):
        super(Header, self).__init__()


class Image(NumberedObject):
    def __init__(self):
        super(Image, self).__init__()
        self.path = None
        
    def __get_caption(self):
        return self.content
    
    def __set_caption(self, caption):
        if caption is None:
            caption = []
        elif (not isinstance(caption, list)) and\
                    (not isinstance(caption, Span)) and\
                    (not isinstance(caption, str)):
            raise TypeError("Caption needs to be a string, \
                                        Span or list of Span!")
        if isinstance(caption, list):
            self.content = caption
        if isinstance(caption, str):
            self.content = [Span(caption)]
        else:
            self.content = [caption]
        
    caption = property(__get_caption, __set_caption)


class TCell(DocumentTreeNode):
    def __init__(self):
        super(TCell, self).__init__()
        self.rowspan = 1
        self.colspan = 1


class Table(NumberedObject):
    __default_row_height = 20
    __default_column_width = 100
    
    def __init__(self):
        super(Table, self).__init__()
        self.__rows = [[TCell()]]
        self.__rowHeights = [self.__default_row_height]
        self.__columnWidths = [self.__default_column_width]
        self.border_width = 1
        self.caption = None
            
    def __get_rows_num(self):
        return len(self.__rows)
        
    def __get_cols_num(self):
        return len(self.__rows[0])
    
    def __create_row(self):
        row = []
        for _ in xrange(0, self.cols_num):
            row.append(TCell())
        return row
    
    def get_cell(self, row, column):
        return (self.__rows[row])[column]
        
    def insert_row(self, index):
        row = self.__create_row()
        self.__rows.insert(index, row)
        self.__rowHeights.insert(index, self.__default_row_height)
        
    def append_row(self):
        self.insert_row(self.rows_num)
        
    def delete_row(self, index):
        if (self.rows_num > 1):
            del self.__rows[index]
            del self.__rowHeights[index]
        else:
            self.__rows[0] = self.__create_row()
            self.__rowHeights[0] = self.__default_row_height
        
    def insert_column(self, index):
        for row in self.__rows:
            row.insert(index, TCell())
        self.__columnWidths.insert(index, self.__default_column_width)
            
    def append_column(self):
        self.insert_column(self.cols_num)
        
    def delete_column(self, index):
        if (self.cols_num > 1):
            for row in self.__rows:
                del row[index]
            del self.__columnWidths[index]
        else:
            for row in self.__rows:
                row[0] = TCell()
            self.__columnWidths[0] = self.__default_column_width
            
    def get_row_height(self, index):
        return self.__rowHeights[index]
    
    def set_row_height(self, index, height):
        self.__rowHeights[index] = height
        
    def get_column_width(self, index):
        return self.__columnWidths[index]
    
    def set_column_width(self, index, width):
        self.__columnWidths[index] = width
    
    def __get_content(self):
        content = []
        for i in xrange(0, self.rows_num - 1):
            content.extend(self.__rows[i])
        return content
        
    rows_num = property(__get_rows_num, None)
    cols_num = property(__get_cols_num, None)
    content = property(__get_content, None)

class ListStyle(object):
    BULLET = 0
    NUMBER = 1
    
    
class Alignment(object):
    LEFT = 0
    CENTER = 1
    RIGHT = 2
    JUSTIFY = 3
    
    
class PageOrientation(object):
    PORTRAIT = 0
    LANDSCAPE = 1
    
    
class FontEffect(object):
    BOLD = 1
    ITALIC = 2
    UNDERLINE = 4
    

class BulletChar(object):
    BULLET = 0
    CDOT = 1
    DIAMOND = 2
    ASTERISK = 3
    CIRCLE = 4
    MEDIUM_HYPHEN = 5
    LONG_HYPHEN = 6


class StyleManager(object):
    __shared_state = {}
    __styles = {}
    
    def __init__(self):
        self.__dict__ = self.__shared_state
        
    def set_style(self, style_name, _style):
        self.__styles[style_name] = _style
        
    def get_style(self, style_name):
        return self.__styles[style_name].copy()
        
        
_style_manager = StyleManager()

# default document _style
_style = Style()
_style['page-numbering'] = True
_style['page-width'] = 213
_style['page-height'] = 297
_style['margin-top'] = 20
_style['margin-bottom'] = 10
_style['margin-left'] = 20
_style['margin-right'] = 20
_style['font-size'] = 12
_style['font-name'] = "Times New Roman"
_style['alignment'] = Alignment.LEFT
_style['text-indent'] = 20
_style['color'] = "#000000"
_style['background-color'] = "#ffffff"
_style['list-_style'] = ListStyle.BULLET
_style['item-spacing'] = 2
_style['item-indent'] = 12
_style_manager.set_style('doc-default', _style)

#default paragraph _style
_style = Style()
_style['margin-top'] = 0
_style['margin-bottom'] = 0
_style['margin-left'] = 0
_style['margin-right'] = 0
_style_manager.set_style('par-default', _style)

#default list _style
_style = Style()
_style['margin-top'] = 0
_style['margin-bottom'] = 2
_style['margin-left'] = 30
_style['margin-right'] = 0
_style_manager.set_style('list-default', _style)
    
