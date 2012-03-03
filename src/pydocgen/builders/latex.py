# -*- coding: utf-8 -*-

from pydocgen.model import *
from pydocgen.builders.common import Builder

class LatexBuilder(Builder):
    def __init__(self):
        pass
    
    def generate_document(self, document):
        result = ""
        
        #TODO generate document beginning
        
        for element in document.content:
            result += element.generate()
        
        #TODO generate document ending
        
        return result
    
    def generate_paragraph(self, paragraph):
        return ""
    
    def generate_span(self, span):
        return ""
    
    def generate_header(self, header):
        return ""
    
    def generate_list(self, lst):
        return ""