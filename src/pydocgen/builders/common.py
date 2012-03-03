# -*- coding: utf-8 -*-

from pydocgen.model import *

class Builder(object):
    def generate(self, documentTreeNode):
        if isinstance(documentTreeNode, Document):
            return self.generate_document(documentTreeNode)
        if isinstance(documentTreeNode, Paragraph):
            return self.generate_paragraph(documentTreeNode)
        if isinstance(documentTreeNode, Span):
            return self.generate_span(documentTreeNode)
        if isinstance(documentTreeNode, Header):
            return self.generate_header(documentTreeNode)
        if isinstance(documentTreeNode, List):
            return self.generate_list(documentTreeNode)