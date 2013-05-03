import unittest
import string
from pydocgen.builders import OdtBuilder
from pydocgen.model import Document,Span,Paragraph,Sequence,Header,List,Table,Image

class TestOdtBuilder(unittest.TestCase):
    def setUp(self):
        db = OdtBuilder()
        
        d=Document('file name')
        self.document = db.generate_document(d)
        
        s=Span('test span')
        self.span = db.generate_span(s)
        
        p=Paragraph(s)
        self.paragraph = db.generate_paragraph(p)
        
        l=List(s)
        self.list = db.generate_list(l)
        
        t=Table(1,1)
        self.table = db.generate_table(t)
        
    def testList(self):
        l = self.list
        assert string.find(l, '<text:list') > -1
        assert string.find(l, '</text:list>') > -1
                                
    def testTable(self):
        t = self.table
        assert string.find(t, '<table:table') > -1 
        assert string.find(t, '</table:table>') > -1
        assert string.find(t, '<table:table-column') > -1
        assert string.find(t, '<table:table-cell') > -1
        assert string.find(t, '</table:table-cell>') > -1
        assert string.find(t, '<table:table-row') > -1
        assert string.find(t, '</table:table-row>') > -1

    def tearDown(self):
        self.document=None
        self.span=None
        self.paragraph=None      
        self.list=None
        self.table=None
        self.image=None

if __name__ == "__main__":
    unittest.main()
