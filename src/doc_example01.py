# -*- coding: utf-8 -*-

from pydocgen.model import *
from pydocgen.builders.latex import LatexBuilder
from pydocgen.builders.html import HtmlBuilder

document = Document()
document.properties['lang'] = "pl"
document.style['font-name'] = "DejaVu Serif"
document.style['font-size'] = 11
document.style['page-width'] = 120
document.style['page-height'] = 180
document.style['page-numbering'] = True
document.style['margin-top'] = 40
document.style['margin-bottom'] = 20
document.style['margin-left'] = 20
document.style['margin-right'] = 20

document.title = "doc_example01"

headers_seq = Sequence()
tables_seq = Sequence()

#first paragraph
span = Span("Phasellus tempor risus eget.")
span.style = Style()
span.style['font-name'] = "Computer Modern"
span.style['font-size'] = 14
span.style['font-effects'] = FontEffect.ITALIC
span.style['color'] = "#1243ff"
span.style['background-color'] = "#00ff00"
	
header = Header()
header.sequence = headers_seq
header += span

document += header

paragraph = Paragraph()
span = Span("Sed in purus dolor. Ut id mauris vel urna fringilla blandit. Phasellus non risus dolor. Curabitur convallis dolor ac massa sollicitudin dapibus. Phasellus nulla neque, vestibulum eget gravida vel,euismod eget lacus. Sed in purus dolor. Ut id mauris vel urna fringilla blandit. Phasellus non risus dolor. Curabitur convallis dolor ac massa sollicitudin dapibus. Phasellus nulla neque, vestibulum eget gravida vel, euismod eget lacus.")
span.style = Style()
span.style['font-name'] = "Computer Modern"
span.style['font-size'] = 9
span.style['font-effects'] = FontEffect.UNDERLINE
span.style['color'] = "#1243ff"

paragraph += span

span = Span(" Times New Roman 17")
span.style = Style()
span.style['font-name'] = "Times New Roman"
span.style['font-size'] = 17
span.style['color'] = "#1243ff"
span.style['background-color'] = "#0fb099"

paragraph += span
document += paragraph

#second paragraph with a bullet list and a numeric list inside
header = Header()
header.sequence = headers_seq
span = Span("Second paragraph")
header += span
document += header

span = Span("Text")
paragraph = Paragraph()
paragraph += span
document += paragraph

number_list = List()
number_list.style = Style()
number_list.style['list-style'] = ListStyle.NUMBER
span = Span("inside1")
paragraph = Paragraph()
paragraph += span
number_list += paragraph

span = Span("inside2")
paragraph = Paragraph()
paragraph += span
number_list += paragraph


list = List()
list.style = Style()
list.style['list-style'] = ListStyle.BULLET
span = Span("item1")
paragraph = Paragraph()
paragraph += span
list += paragraph

span = Span("item2")
paragraph = Paragraph()
paragraph += span
list += paragraph

span = Span("item3")
paragraph = Paragraph()
paragraph += span
paragraph += number_list
list += paragraph

span = Span("item4")
paragraph = Paragraph()
paragraph += span
list += paragraph


document += list

#TODO image
#image = Image()
#image.path = "image.png"
#image.caption = "This is an image."
#
#document += image

#third paragraph with a table
header = Header()
header.sequence = headers_seq
span = Span("And another paragraph")
header += span
document += header


#document += table
#...
#TODO


# here we generate the document

if __name__ == '__main__':
    document.builder = LatexBuilder()
    document.generate_file("doc_example01.tex")
    
    document.builder = HtmlBuilder()
    document.generate_file("doc_example01.htm")
