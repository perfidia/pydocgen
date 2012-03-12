# -*- coding: utf-8 -*-

from pydocgen.model import Document, Paragraph, Span, Header, List, Image, Table

class Builder(object):
    def generate(self, documentTreeNode):
        if isinstance(documentTreeNode, Document):
            documentTreeNode.fill_parent_fields()
            documentTreeNode.reset_sequences()
            return self.generate_document(documentTreeNode)
        if isinstance(documentTreeNode, Paragraph):
            return self.generate_paragraph(documentTreeNode)
        if isinstance(documentTreeNode, Span):
            return self.generate_span(documentTreeNode)
        if isinstance(documentTreeNode, Header):
            return self.generate_header(documentTreeNode)
        if isinstance(documentTreeNode, List):
            return self.generate_list(documentTreeNode)
        if isinstance(documentTreeNode, Image):
            return self.generate_image(documentTreeNode)
        if isinstance(documentTreeNode, Table):
            return self.generate_table(documentTreeNode)
