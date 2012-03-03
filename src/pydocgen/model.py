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
        self.content = list() # of DocumentTreeNode
        
    def __get_builder(self):
        builder = None
        node = self
        while node is not None:
            try:
                builder = node.builder
                break
            except AttributeError:
                node = node.parent    
        return builder
    
    def __get_effective_style(self):
        #TODO
        return Style()
    
    builder = property(__get_builder, None)
    effective_style = property(__get_effective_style, None)
    
    def fill_parent_fields(self):
        #TODO
        pass
    
    def generate(self):
        return self.builder.generate(self)
    

class Document(DocumentTreeNode):
    builder = None
    
    def __init__(self):
        super(Document, self).__init__()
        self.style = Style() # TODO assign default document style from StyleManager
        self.properties = DocumentProperties()
        self.builder = None
        
        
class Paragraph(DocumentTreeNode):
    def __init__(self):
        super(Paragraph, self).__init__()


class Span(DocumentTreeNode):
    def __init__(self):
        super(Span, self).__init__()
        self.text = None
        

class List(DocumentTreeNode):
    def __init__(self):
        super(List, self).__init__()


class Sequence(object):
    def __init__(self, start_value = 1):
        self.value = start_value - 1
        self.subsequence = None
        
    def next_value(self):
        self.value += 1
        return self.value
    

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
    JUSTIFY = 4


class StyleManager(object):
    #TODO
    pass
  

    