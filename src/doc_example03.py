# -*- coding: utf-8 -*-

from pydocgen.model import *
from pydocgen.builders.latex import LatexBuilder

document = Document()
document.style += AlignmentProperty.JUSTIFY
document.style['font-name'] = "Computer Modern"

section_seq = Sequence()

document += Header("Phasellus tempor risus eget.", section_seq)

paragraph = Paragraph("Sed in purus dolor. Ut id mauris vel urna fringilla blandit. Phasellus non risus dolor. Curabitur convallis dolor ac massa sollicitudin dapibus. Phasellus nulla neque, vestibulum eget gravida vel, euismod eget lacus. Sed in purus dolor. Ut id mauris vel urna fringilla blandit. Phasellus non risus dolor. Curabitur convallis dolor ac massa sollicitudin dapibus. Phasellus nulla neque, vestibulum eget gravida vel, euismod eget lacus.")
paragraph.style += AlignmentProperty.LEFT
document += paragraph

document += Header("Phasellus tempor risus eget.", section_seq)

document += "Sed in purus dolor. Ut id mauris vel urna fringilla blandit. Phasellus non risus dolor. Curabitur convallis dolor ac massa sollicitudin dapibus. Phasellus nulla neque, vestibulum eget gravida vel, euismod eget lacus."

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
span.style += FontEffectProperty.BOLD

paragraph += span

paragraph += " arcu adipiscing. Nunc sagittis suscipit diam, ut lacinia justo hendrerit quis. Sed vitae ante facilisis enim feugiat ultrices in nec libero."

document += paragraph

paragraph = Paragraph()

span = Span("Nam orci")
span.style += FontEffectProperty.UNDERLINE
paragraph += span

paragraph += "odio, sollicitudin quis vehicula eu, pulvinar at risus. Ut sed lacus libero, vitae eleifend nulla. Vivamus sed enim odio, eu "

span = Span("sodales")
span.style += FontEffectProperty.BOLD

paragraph += span

paragraph += "nulla. Vestibulum urna felis, mattis eget aliquet et, dictum quis risus."

document += paragraph

subsection_seq = Sequence(parent=section_seq)

header = Header("Lorem ipsum", subsection_seq)
header.style['background-color'] = "#101010"
header.style['border-width'] = 1

document += header

paragraph = Paragraph("In suspicit")
paragraph.content[0].style['font-name'] = "Courier"
paragraph += " elit tincidunt arcu placerat ac commodo arcu adipiscing:"

document += paragraph

image = Image("ppwi.png")
image.style['alignment'] = AlignmentProperty.CENTER
image.style['width'] = 66

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

table = Table(2, 2)
table.style['alignment'] = AlignmentProperty.CENTER

cell = table.get_cell(0, 0)
cell.colspan = 2
span = Span("Placerat ac commodo arcu adipiscing")
span.style['font-effect'] = FontEffectProperty.BOLD
cell.content += [span]
cell.style['background-color'] = "#cccccc"

cell = table.get_cell(1, 0)
cell.style['alignment'] = AlignmentProperty.JUSTIFY
cell.colspan = 2
span = Span("In suscipit elit tincidunt arcu placerat ac commodo arcu adipiscing. Nunc sagittis suscipit diam, ut lacinia justo hendrerit quis. Sed vitae ante facilisis enim feugiat ultrices in nec libero. Quisque ligula velit, pellentesque a consectetur non, bibendum eleifend nibh. Nam non tincidunt orci. Nunc ultricies neque nec magna vestibulum malesuada. Cras mollis feugiat turpis, eu mollis magna laoreet eu. Vivamus pharetra imperdiet libero, nec bibendum sapien adipiscing at. Nunc dictum facilisis est sed ultricies.")
span.style['font-effect'] = FontEffectProperty.BOLD
cell.content += [span]
cell.style['background-color'] = "#cccccc"

table.set_column_width(0, 130)
table.set_column_width(1, 30)

document += table

document.builder = LatexBuilder()
document.generate_file("doc_example03.tex")
