import unittest
import string
from pydocgen.builders import DitaBuilder
from pydocgen.model import Document,Span,Paragraph,Sequence,Header,List,Table,Image

class TestDitaBuilder(unittest.TestCase):
    def setUp(self):
        db = DitaBuilder()
        
        d=Document('file name')
        self.document = db.generate_document(d)
        
        s=Span('test span')
        self.span = db.generate_span(s)
        
        p=Paragraph(s)
        self.paragraph = db.generate_paragraph(p)
        
#        h=Header(s,Sequence())
#        self.header = db.generate_header(h)
        
        l=List(s)
        self.list = db.generate_list(l)
        
        t=Table(1,1)
        self.table = db.generate_table(t)
        
        i=Image()
        i.path='path'
        self.image = db.generate_image(i)
        
    def testDocument(self):
        d = self.document
        assert string.find(d,'<?xml version="1.0" encoding="utf-8"?>\n') == 0
        assert string.find(d,'<!DOCTYPE map PUBLIC "-//OASIS//DTD DITA Map//EN" "../dtd/map.dtd">\n') != -1
        assert string.find(d,'<topic xml:lang="en" id="main_topic">\n\t<title></title>\n\t') != -1
        assert string.find(d,'<shortdesc></shortdesc>\n<body>\n\n</body>\n</topic>\n') != -1
        
    def testSpan(self):
        s = self.span
        assert s == '<span>test span</span>'
                
    def testParagraph(self):
        p = self.paragraph
        assert p == '\n<p>\n\t\n</p>\n'
        
#    def testHeader(self):
#        h = self.header
#        assert string.find(h, '<section>\n\t<title>') == 0
#        assert string.find(h, '</title>\n</section>') == len(h)-19        
        
    def testList(self):
        l = self.list
        assert string.find(l, '\n<ul>\n\n') == 0
        assert string.find(l, '\n\n</ul>\n') == len(l)-8
                                
    def testTable(self):
        t = self.table
        assert string.find(t, '\n\n<simpletable') == 0
        assert string.find(t, '\n</simpletable>\n\n') == len(t)-17
        
    def testImage(self):
        i = self.image
        assert string.find(i, '<div><image href=\"path\"') == 0
        assert string.find(i, '\n</image>\n</div>') == len(i)-16        

    def tearDown(self):
        self.document=None
        self.span=None
        self.paragraph=None        
#        self.header=None
        self.list=None
        self.table=None
        self.image=None

if __name__ == "__main__":
    unittest.main()
