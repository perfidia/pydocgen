# -*- coding: utf-8 -*-

from pydocgen.model import *
from pydocgen.builders.latex import LatexBuilder
from pydocgen.builders.html import HtmlBuilder

document = Document()
document.properties['lang'] = "pl"
document.style['font-name'] = "DejaVu Serif"
document.style['font-size'] = 11
document.style['page-width'] = 200
document.style['page-height'] = 300
document.style['page-numbering'] = True
document.style['margin-top'] = 40
document.style['margin-bottom'] = 20
document.style['margin-left'] = 20
document.style['margin-right'] = 20

document.title = "doc_example01"

headers_seq = Sequence()
tables_seq = Sequence()

#header
span = Span("First header")
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

#paragraph with two spans
paragraph = Paragraph()
paragraph.style = Style()
paragraph.style['alignment'] =  Alignment.LEFT
paragraph.style['text-indent'] = 8
span = Span("Sed in purus dolor. Ut id mauris vel urna fringilla blandit. Phasellus non risus dolor.")
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

#header
header = Header()
header.sequence = headers_seq
span = Span("Second header")
header += span
document += header

#paragraph
span = Span("Aliquam vehicula sem ut pede. Cras purus lectus, egestas eu, vehicula at, imperdiet sed, nibh. Morbi consectetuer luctus felis. Donec vitae nisi. Aliquam tincidunt feugiat elit. Duis sed elit ut turpis ullamcorper feugiat. Praesent pretium, mauris sed fermentum hendrerit, nulla lorem iaculis magna, pulvinar scelerisque urna tellus a justo. Suspendisse pulvinar massa in metus. Duis quis quam. Proin justo. Curabitur ac sapien. Nam erat. Praesent ut quam.")
paragraph = Paragraph()
paragraph.style = Style()
paragraph.style['alignment'] = Alignment.CENTER
paragraph.style['margin-top'] = 30
paragraph.style['margin-bottom'] = 30
paragraph.style['margin-left'] =  250
paragraph.style['margin-right'] = 70
paragraph += span
document += paragraph

#simple list
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

#header 3
header = Header()
header.sequence = headers_seq
span = Span("And another header")
header += span
document += header

#paragraph right alignment
span = Span("Text Text text 1234567890 asdg kjjsnfb ekrhgrmfg tr grt gtrw e gtwtr  ergt")
span.style = Style()
span.style['font-name'] = "Times New Roman"
span.style['font-size'] = 11
span.style['color'] = "#ffff00"
span.style['background-color'] = "#0fb099"
paragraph = Paragraph()
paragraph.style = Style()
paragraph.style['alignment'] = Alignment.RIGHT
paragraph.style['margin-top'] = 30
paragraph.style['margin-bottom'] = 30
paragraph.style['margin-left'] =  50
paragraph.style['margin-right'] = 70
paragraph += span
document += paragraph


#document += table
#...
#TODO


# here we generate the document

if __name__ == '__main__':
    document.builder = LatexBuilder()
    document.generate_file("doc_example01.tex")
    
    #document.builder = HtmlBuilder()
    #document.generate_file("doc_example01.htm")
