import unittest
import string
from builders import DitaBuilder

class TestDitaBuilder(unittest.TestCase):
    def setUp(self):
        self.paragraph = DitaBuilder.generate_paragraph(self, 'test paragraph')

    def testParagraph(self):
        p = self.paragraph
        assert string.find(p,'<p>') != -1
        assert string.find(p,'test paragraph') != -1
        assert string.find(p,'</p>') != -1

    def tearDown(self):
        self.paragraph.dispose()

if __name__ == "__main__":
    unittest.main()
