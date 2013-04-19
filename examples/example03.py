#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../src')

from pydocgen.model import *
from pydocgen.builders import LatexBuilder
from pydocgen.builders import HtmlBuilder
from pydocgen.builders import DitaBuilder
from pydocgen.builders import DitaMapBuilder
from pydocgen.builders import OdtBuilder

#creating document with specific properties and styles
document = Document("output3", path="../output")
document.properties['language'] = "pl"
document.style['font-name'] = "Times New Roman"
document.style['font-size'] = 11
document.style['page-size'] = PageSizeProperty.A4
document.style['page-numbering'] = True
document.style['margin-top'] = 40
document.style['margin-bottom'] = 20
document.style['margin-left'] = 20
document.style['margin-right'] = 20

document.title = "Zabawa z ogonkami - śćńźż"

#creating sequences
headers_seq = Sequence()

#sequence starting with number 96, being a child of headers_seq
subheaders_seq = Sequence(96, headers_seq)
subsubheaders_seq = Sequence(7, subheaders_seq)
par_seq = Sequence(1, subsubheaders_seq)

#header 1
span = Span("Grzegrzółka")
span.style['font-name'] = "Computer Modern"
span.style['font-size'] = 14
span.style['font-effect'] = FontEffectProperty.ITALIC
span.style['color'] = "#1243ff"
span.style['background-color'] = "#00ff00"

header = Header()
header.sequence = headers_seq
header += span

document += header

paragraph = Paragraph()
paragraph.style['alignment'] =  AlignmentProperty.LEFT
paragraph.style['text-indent'] = 8
span = Span("Jakiś fajny tekst z polskimi znaczkami.")
span.style['font-name'] = "Computer Modern"
span.style['font-size'] = 9
span.style['font-effect'] = FontEffectProperty.UNDERLINE
span.style['color'] = "#1243ff"

paragraph += span

span = Span("Paragrafik z jaskółami.")
span.style['font-name'] = "Times New Roman"
span.style['font-size'] = 17
span.style['color'] = "#1243ff"
span.style['background-color'] = "#0fb099"

paragraph += span
document += paragraph

#header 2
header = Header()
header.sequence = headers_seq
span = Span("O książce")
header += span
document += header

span = Span("A teraz bąki i inne owady.")
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
number_list += Span("ą")
number_list += Span("ń")

document += number_list

#table
table = Table(5, 2)
cellstyle = Style()
cellstyle['background-color'] = "#ff00ce"
cellstyle['font-effect'] = FontEffectProperty.ITALIC

cell = table.get_cell(0, 0)
cell.colspan = 2
span = Span("śŚ")
span.style['font-effect'] = (FontEffectProperty.UNDERLINE + FontEffectProperty.BOLD)
span.style['background-color'] = "#ffffff"
cell.content += [span]
cell.style['alignment'] = AlignmentProperty.CENTER
cell.style.update(cellstyle)

cell = table.get_cell(1, 0)
cell.style['alignment'] = AlignmentProperty.JUSTIFY
cell.colspan = 2
span = Span("Ćć")
span.style['background-color'] = "#00ff00"
cell.content += [span]
cell.style.update(cellstyle)

cell = table.get_cell(2, 0)
span = Span("óÓ")
span.style['background-color'] = "#1111cc"
cell.content += [span]
cell.style.update(cellstyle)

cell = table.get_cell(3, 0)
span = Span("łŁ")
cell.content += [span]
cell.style.update(cellstyle)

cell = table.get_cell(3, 1)
span = Span("ęĘ")
cell.content += [span]
cell.style.update(cellstyle)

cell = table.get_cell(4, 0)
span = Span("Ćć")
cell.content += [span]
cell.style.update(cellstyle)

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

ditamap = DitaMapBuilder()
s = ditamap.generate_document(document,'output2.dita')
viewsFile = open('../output/output2.ditamap', 'w')
viewsFile.write(s)
viewsFile.close()

document.builder = OdtBuilder()
document.generate()
