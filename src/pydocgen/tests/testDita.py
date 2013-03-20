import unittest
from builders import DitaBuilder

class TestDitaBuilder(unittest.TestCase):
    def setUp(self):
        self.paragraph = DitaBuilder.generate_paragraph(self, 'test paragraph')

    def testParagraph(self):
        p = self.paragraph
        assert p == '\n<p' + DitaBuilder.__generate_style_from_dict(self, 'test paragraph') + \
             '>\n\t' + 'test paragraph' + '\n</p>\n'

    def tearDown(self):
        self.paragraph.dispose()

if __name__ == "__main__":
    unittest.main()
 
