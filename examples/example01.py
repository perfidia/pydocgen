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

hdrstyle = StyleManager().get_style('header-default')
hdrstyle['margin-top'] = 0
hdrstyle['margin-bottom'] = 0

StyleManager().set_style('header-default', hdrstyle)

document = Document("output1", path="../output")
document.style += AlignmentProperty.JUSTIFY
document.style['font-name'] = "Times New Roman"

section_seq = Sequence()

document += Header("Phasellus tempor risus eget.", section_seq)

paragraph = Paragraph("Sed in purus dolor. Ut id mauris vel urna fringilla blandit. Phasellus non risus dolor. Curabitur convallis dolor ac massa sollicitudin dapibus. Phasellus nulla neque, vestibulum eget gravida vel, euismod eget lacus. Sed in purus dolor. Ut id mauris vel urna fringilla blandit. Phasellus non risus dolor. Curabitur convallis dolor ac massa sollicitudin dapibus. Phasellus nulla neque, vestibulum eget gravida vel, euismod eget lacus.")
paragraph.style += AlignmentProperty.LEFT
document += paragraph

document += Header("Phasellus tempor risus eget.", section_seq)

paragraph = Paragraph("Sed in purus dolor. Ut id mauris vel urna fringilla blandit. Phasellus non risus dolor. Curabitur convallis dolor ac massa sollicitudin dapibus. Phasellus nulla neque, vestibulum eget gravida vel, euismod eget lacus.")
paragraph.style['text-indent'] = 18

document += paragraph

span = Span("Lorem ipsum:")
span.style += FontEffectProperty.BOLD
paragraph = Paragraph(span)
paragraph.style['margin-top'] = 12

document += paragraph

paragraph = Paragraph()

span = Span("In suscipit")
span.style += FontEffectProperty.UNDERLINE
paragraph += span

paragraph += " elit tincidunt arcu placerat ac "

span = Span("commodo")
span.style['font-effect']  = (FontEffectProperty.BOLD + FontEffectProperty.STRIKE \
    + FontEffectProperty.ITALIC + FontEffectProperty.UNDERLINE)
paragraph += span

paragraph += " arcu adipiscing. Nunc sagittis suscipit diam, ut lacinia justo hendrerit quis. Sed vitae ante facilisis enim feugiat ultrices in nec libero."

document += paragraph

paragraph = Paragraph()

span = Span("Nam orci")
span.style += FontEffectProperty.UNDERLINE
paragraph += span

paragraph += u" odio, sollicitudin quis vehicula eu, pulvinar at risus. Ut sed lacus libero, vitae eleifend nulla. Vivamus sed enim odio, eu "

span = Span("sodales")
span.style += FontEffectProperty.BOLD

paragraph += span

paragraph += " nulla. Vestibulum urna felis, mattis eget aliquet et, dictum quis risus."

document += paragraph

subsection_seq = Sequence(parent=section_seq)

header = Header("Lorem ipsum", subsection_seq)
header.style['background-color'] = "#cccccc"
header.style['border-width'] = 1

document += header

paragraph = Paragraph("In suspicit")
paragraph.content[0].style['font-name'] = "Courier"
paragraph += " elit tincidunt arcu placerat ac commodo arcu adipiscing:"

document += paragraph

image = Image("example01_img.png")
image.style['alignment'] = AlignmentProperty.CENTER
image.style['width'] = 66
image.style['height'] = 33

document += image

document += "Nulla hendrerit mauris a leo ultricies viverra. Suspendisse a ligula nec elit mattis placerat. Aliquam porttitor leo quis tortor gravida ultrices."

table = Table(6, 2)

style = Style()
style['font-size'] = 11

span = Span("Phasellus")
span.style = style
table.get_cell(0, 0).content += [span]

span = Span("Suspendisse? (Nunc)")
span.style = style
table.get_cell(0, 1).content += [span]

style = Style()
style['font-name'] = "Courier"
style['font-size'] = 10

span = Span("pellentesque hendrerit")
span.style = style
table.get_cell(1, 0).content += [span]

span = Span("amet")
span.style = style
table.get_cell(1, 1).content += [span]

span = Span("enim sit")
span.style = style
table.get_cell(2, 0).content += [span]

span = Span("amet")
span.style = style
table.get_cell(2, 1).content += [span]

span = Span("amet porta")
span.style = style
table.get_cell(3, 0).content += [span]

span = Span("amet")
span.style = style
table.get_cell(3, 1).content += [span]

span = Span("fringilla turpis")
span.style = style
table.get_cell(4, 0).content += [span]

span = Span("erat (mauris aliquam)")
span.style = style
table.get_cell(4, 1).content += [span]

span = Span("nunc eu pulvinar commodo")
span.style = style
table.get_cell(5, 0).content += [span]

span = Span("nunc (eu pulvinar)")
span.style = style
table.get_cell(5, 1).content += [span]

table.style['alignment'] = AlignmentProperty.CENTER
table.set_column_width(0, 55)
table.set_column_width(1, 70)

for row in xrange(0, table.rows_num):
    for col in xrange(0, table.cols_num):
        cell = table.get_cell(row, col).style['alignment'] = \
                    AlignmentProperty.LEFT

document += table

table = Table(7, 2)

graybgcellstyle = Style()
graybgcellstyle['background-color'] = "#cccccc"
graybgcellstyle['font-effect'] = FontEffectProperty.BOLD

cell = table.get_cell(0, 0)
cell.colspan = 2
span = Span("Placerat ac commodo arcu adipiscing")
span.style['font-effect'] = (FontEffectProperty.UNDERLINE + FontEffectProperty.BOLD)
cell.content += [span]
cell.style['alignment'] = AlignmentProperty.CENTER
cell.style.update(graybgcellstyle)

cell = table.get_cell(1, 0)
cell.style['alignment'] = AlignmentProperty.JUSTIFY
cell.colspan = 2
span = Span(u"In suscipit elit tincidunt arcu placerat ac commodo arcu adipiscing. Nunc sagittis suscipit diam, ut lacinia justo hendrerit quis. Sed vitae ante facilisis enim feugiat ultrices in nec libero. Quisque ligula velit, pellentesque a consectetur non, bibendum eleifend nibh. Nam non tincidunt orci. Nunc ultricies neque nec magna vestibulum malesuada. Cras mollis feugiat turpis, eu mollis magna laoreet eu. Vivamus pharetra imperdiet libero, nec bibendum sapien adipiscing at. Nunc dictum facilisis est sed ultricies.")
cell.content += [span]
cell.style.update(graybgcellstyle)

cell = table.get_cell(2, 0)
span = Span("Nam")
cell.content += [span]
cell.style.update(graybgcellstyle)

cell = table.get_cell(2, 1)
span = Span("Quisque?")
cell.content += [span]
cell.style.update(graybgcellstyle)

cell = table.get_cell(3, 0)
span = Span("tincidunt")
cell.content += [span]
cell.style.update(graybgcellstyle)
cell.style['font-name'] = "Courier"

cell = table.get_cell(4, 0)
span = Span("pellentesque")
cell.content += [span]
cell.style.update(graybgcellstyle)
cell.style['font-name'] = "Courier"

cell = table.get_cell(5, 0)
span = Span("vestibulum")
cell.content += [span]
cell.style.update(graybgcellstyle)
cell.style['font-name'] = "Courier"

cell = table.get_cell(6, 0)
span = Span("turpis")
cell.content += [span]
cell.style.update(graybgcellstyle)
cell.style['font-name'] = "Courier"

table.set_column_width(0, 120)
table.set_column_width(1, 30)

document += table

header = Header(Span("Phasellus tempor risus eget."), section_seq)

document += header

document += "Comment"

lst = List()
lst += "Nunc"
lst += "sagittis"
lst += "suscipit diam,"
lst += "ut lacinia justo hendrerit quis."
lst += ""
lst += "Sed vitae ante facilisis enim feugiat ultrices in nec libero."

document += lst

paragraph = Paragraph("Comment")
paragraph.style['alignment'] = AlignmentProperty.CENTER

document += paragraph

lst = List()
lst.style['list-style'] = ListStyleProperty.NUMBER

lst += "Suspendisse a"
lst += "ligula nec elit mattis placerat."
lst += "Aliquam porttitor leo quis tortor gravida ultrices."

document += lst

paragraph = Paragraph("Comment")
paragraph.style['alignment'] = AlignmentProperty.RIGHT

document += paragraph

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
s = ditamap.generate_document(document,'output1.dita')
viewsFile = open('../output/output1.ditamap', 'w')
viewsFile.write(s)
viewsFile.close()

document.builder = OdtBuilder()
document.generate()