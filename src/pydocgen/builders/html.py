# -*- coding: utf-8 -*-

from pydocgen.model import *
from pydocgen.builders.common import Builder

class HtmlBuilder(Builder):
    def __init__(self):
        super(HtmlBuilder, self).__init__()
    
    def generate_document(self, document):
        return ""
    
    def generate_paragraph(self, paragraph):
        return ""
    
    def generate_span(self, span):
        return ""
    
    def generate_header(self, header):
        return ""
    
    def generate_list(self, lst):
        return ""
    
    def generate_image(self, image):
        return ""
    
    def generate_table(self, table):
        return ""