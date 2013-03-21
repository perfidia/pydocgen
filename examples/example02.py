#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../src')

from pydocgen.model import *
from pydocgen.builders import LatexBuilder
from pydocgen.builders import HtmlBuilder
from pydocgen.builders import DitaBuilder

#creating document with specific properties and styles
document = Document("output2", path="../output")
document.properties['language'] = "pl"
document.style['font-name'] = "Times New Roman"
document.style['font-size'] = 11
document.style['page-size'] = PageSizeProperty.A4
document.style['page-numbering'] = True
document.style['margin-top'] = 40
document.style['margin-bottom'] = 20
document.style['margin-left'] = 20
document.style['margin-right'] = 20

document.title = "doc_example01"

#creating sequences
headers_seq = Sequence()

#sequence starting with number 96, being a child of headers_seq
subheaders_seq = Sequence(96, headers_seq)
subsubheaders_seq = Sequence(7, subheaders_seq)
par_seq = Sequence(1, subsubheaders_seq)

#header 1
span = Span("First header")
span.style['font-name'] = "Computer Modern"
span.style['font-size'] = 14
span.style['font-effect'] = FontEffectProperty.ITALIC
span.style['color'] = "#1243ff"
span.style['background-color'] = "#00ff00"

header = Header()
header.sequence = headers_seq
header += span

document += header

#paragraph with two spans
paragraph = Paragraph()
paragraph.style['alignment'] =  AlignmentProperty.LEFT
paragraph.style['text-indent'] = 8
span = Span("Sed in purus dolor. Ut id mauris vel urna fringilla blandit. Phasellus non risus dolor.")
span.style['font-name'] = "Computer Modern"
span.style['font-size'] = 9
span.style['font-effect'] = FontEffectProperty.UNDERLINE
span.style['color'] = "#1243ff"

paragraph += span

span = Span(" Times New Roman 17")
span.style['font-name'] = "Times New Roman"
span.style['font-size'] = 17
span.style['color'] = "#1243ff"
span.style['background-color'] = "#0fb099"

paragraph += span
document += paragraph

#header 2
header = Header()
header.sequence = headers_seq
span = Span("Second header")
header += span
document += header

image = Image("example01_img.png")
image.style['alignment'] = AlignmentProperty.CENTER
image.style['width'] = 66
image.caption = u"To jest rysunek na środku"
document += image

#paragraph centered with margins set
span = Span("Aliquam vehicula sem ut pede. Cras purus lectus, egestas eu, vehicula at, imperdiet sed, nibh. Morbi consectetuer luctus felis. Donec vitae nisi. Aliquam tincidunt feugiat elit. Duis sed elit ut turpis ullamcorper feugiat. Praesent pretium, mauris sed fermentum hendrerit, nulla lorem iaculis magna, pulvinar scelerisque urna tellus a justo. Suspendisse pulvinar massa in metus. Duis quis quam. Proin justo. Curabitur ac sapien. Nam erat. Praesent ut quam.")
paragraph = Paragraph()
paragraph.style['alignment'] = AlignmentProperty.CENTER
paragraph.style['margin-top'] = 30
paragraph.style['margin-bottom'] = 30
paragraph.style['margin-left'] =  250
paragraph.style['margin-right'] = 70
paragraph += span
document += paragraph

#simple list
number_list = List()
number_list.style['list-style'] = ListStyleProperty.NUMBER
span = Span("inside1")
number_list += span

span = Span("inside2")
number_list += span


lst = List()
lst.style['list-style'] = ListStyleProperty.BULLET
span = Span("item1")
lst += span

span = Span("item2")

lst += span

span = Span("item3")
lst += span
lst += number_list


span = Span("item4")

lst += span


document += lst


#a not numbered header
header = Header()
header.style['header-numbered'] = False
header.sequence = headers_seq
span = Span("And this is a not numbered header")
header += span
document += header

#header 3
header = Header()
header.sequence = headers_seq
span = Span("And another header")
header += span
document += header

#subheader 3.96
header = Header()
header.sequence = subheaders_seq
span = Span("Subheader")
header += span
document += header

#subheader 3.96.7
header = Header()
header.sequence = subsubheaders_seq
span = Span("Subsubheader")
header += span
document += header

#subheader 3.96.8
header = Header()
header.sequence = subsubheaders_seq
span = Span("Subsubheader")
header += span
document += header

#subheader 3.96.8.1
header = Header()
header.sequence = par_seq
span = Span("Subsubheader")
header += span
document += header

#subheader 3.97
header = Header()
header.sequence = subheaders_seq
span = Span("Next subheader")
span.style['color'] = "#ff0000"
span.style['background-color'] = "#0fb099"

header += span
document += header

#paragraph right alignment
span = Span("Text Text text 1234567890 asdg kjjsnfb ekrhgrmfg tr grt gtrw e gtwtr  ergt")
span.style['font-name'] = "Times New Roman"
span.style['font-size'] = 11
span.style['color'] = "#ffff00"
span.style['background-color'] = "#0fb099"
paragraph = Paragraph()
paragraph.style['alignment'] = AlignmentProperty.RIGHT
paragraph.style['margin-top'] = 30
paragraph.style['margin-bottom'] = 30
paragraph.style['margin-left'] =  50
paragraph.style['margin-right'] = 70
paragraph += span
document += paragraph


#paragraph right alignment
span = Span("Text Text text 1234567890 asdg kjjsnfb ekrhgrmfg tr grt gtrw e gtwtr  ergt")
span.style['font-name'] = "Times New Roman"
span.style['font-size'] = 11
span.style['color'] = "#ffff00"
paragraph = Paragraph()
paragraph.style['alignment'] = AlignmentProperty.RIGHT
paragraph.style['background-color'] = "#ff0000"
paragraph += span
document += paragraph


image = Image("example01_img.png")
image.style['alignment'] = AlignmentProperty.RIGHT
image.style['width'] = 66
image.caption = "To jest rysunek"
document += image


table = Table(5, 2)
cellstyle = Style()
cellstyle['background-color'] = "#ff00ce"
cellstyle['font-effect'] = FontEffectProperty.ITALIC

cell = table.get_cell(0, 0)
cell.colspan = 2
span = Span("cell")
span.style['font-effect'] = (FontEffectProperty.UNDERLINE + FontEffectProperty.BOLD)
span.style['background-color'] = "#ffffff"
cell.content += [span]
cell.style['alignment'] = AlignmentProperty.CENTER
cell.style.update(cellstyle)

cell = table.get_cell(1, 0)
cell.style['alignment'] = AlignmentProperty.JUSTIFY
cell.colspan = 2
span = Span("In suscipit elit tincidunt arcu placerat ac commodo arcu adipiscing. Nunc sagittis suscipit diam, ut lacinia justo hendrerit quis. Sed vitae ante facilisis enim feugiat ultrices in nec libero. Quisque ligula velit, pellentesque a consectetur non, bibendum eleifend nibh. Nam non tincidunt orci. Nunc ultricies neque nec magna vestibulum malesuada. Cras mollis feugiat turpis, eu mollis magna laoreet eu. Vivamus pharetra imperdiet libero, nec bibendum sapien adipiscing at. Nunc dictum facilisis est sed ultricies.")
span.style['background-color'] = "#00ff00"
cell.content += [span]
cell.style.update(cellstyle)

cell = table.get_cell(2, 0)
span = Span("In suscipit elit tincidunt arcu placerat ac commodo arcu adipiscing. Nunc sagittis suscipit diam, ut lacinia justo hendrerit quis. Sed vitae ante facilisis enim feugiat ultrices in nec libero. Quisque ligula velit, pellentesque a consectetur non, bibendum eleifend nibh. Nam non tincidunt orci. Nunc ultricies neque nec magna vestibulum malesuada. Cras mollis feugiat turpis, eu mollis magna laoreet eu. Vivamus pharetra imperdiet libero, nec bibendum sapien adipiscing at. Nunc dictum facilisis est sed ultricies.")
span.style['background-color'] = "#1111cc"
cell.content += [span]
cell.style.update(cellstyle)


cell = table.get_cell(3, 0)
span = Span("CeLL")
cell.content += [span]
cell.style.update(cellstyle)

cell = table.get_cell(3, 1)
span = Span("123455.98")
cell.content += [span]
cell.style.update(cellstyle)

cell = table.get_cell(4, 0)
span = Span("table cell")
cell.content += [span]
cell.style.update(cellstyle)
cell.style['font-name'] = "Computer Modern"





table.set_column_width(0, 120)
table.set_column_width(1, 30)

document += table


#############################################################
#                    GENERATE THE DOCUMENT                  #
#############################################################

document.builder = LatexBuilder()
document.generate()

document.builder = HtmlBuilder();
document.generate()

document.builder = DitaBuilder();
document.generate()