# -*- coding: utf-8 -*-

from pydocgen.model import *
from pydocgen.builders.latex import LatexBuilder

document = Document()
document.style += AlignmentProperty.JUSTIFY

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
span.style += (FontEffectProperty.UNDERLINE + FontEffectProperty.BOLD)
paragraph += span

paragraph += "odio, sollicitudin quis vehicula eu, pulvinar at risus. Ut sed lacus libero, vitae eleifend nulla. Vivamus sed enim odio, eu "

span = Span("sodales")
span.style += FontEffectProperty.BOLD

paragraph += span

paragraph += "nulla. Vestibulum urna felis, mattis eget aliquet et, dictum quis risus."

document += paragraph



document.builder = LatexBuilder()
document.generate_file("doc_example03.tex")
