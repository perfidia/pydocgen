# -*- coding: utf-8 -*-

from pydocgen.model import *
from pydocgen.builders.latex import LatexBuilder
from pydocgen.builders.html import HtmlBuilder

document = Document()
document.properties['lang'] = "pl"
document.style['font-name'] = "DejaVu Serif"
document.style['font-size'] = 11

headers_seq = Sequence()

span = Span("Phasellus tempor risus eget.")
header = Header()
header.sequence = headers_seq
header += span

document += header

span = Span("Sed in purus dolor. Ut id mauris vel urna fringilla blandit. Phasellus non risus dolor. Curabitur convallis dolor ac massa sollicitudin dapibus. Phasellus nulla neque, vestibulum eget gravida vel,euismod eget lacus. Sed in purus dolor. Ut id mauris vel urna fringilla blandit. Phasellus non risus dolor. Curabitur convallis dolor ac massa sollicitudin dapibus. Phasellus nulla neque, vestibulum eget gravida vel, euismod eget lacus.")
paragraph = Paragraph()
paragraph += span

document += paragraph

#...
#TODO


# here we generate the document

if __name__ == '__main__':
    document.builder = LatexBuilder()
    document.generate_file("doc_example01.tex")
    
    document.builder = HtmlBuilder()
    document.generate_file("doc_example01.htm")
