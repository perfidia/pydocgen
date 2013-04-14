__author__ = 'a'

import os

from pydocgen.model import ListStyleProperty, AlignmentProperty, FontEffectProperty, Image, Style, Table
import datetime

now = datetime.datetime.now()

from pydocgen.builders.common import Builder

class DitaMapBuilder(Builder):
    """Class responsible for creating a DITA Map document.
    It inherits from base Builder class shared between all builder classes.
    """

    def __init__(self):
        super(DitaMapBuilder, self).__init__()
        self.extension = "ditamap"

    def generate_document(self, document,ditaTitle):

        result = ''
        result += '<?xml version="1.0" encoding="utf-8"?>\n'
        result += '<!DOCTYPE map PUBLIC "-//OASIS//DTD DITA Map//EN" "http://docs.oasis-open.org/dita/v1.1/CD01/dtd/map.dtd">'
        result += '<map>\n'
        title = 'Default Title'
        if 'title' in document.properties:
            title = document.properties['title']
        author = 'Tarek Alkhaeir ,Tomasz Bajaczyk '
        if 'author' in document.properties:
            author = document.properties['author']
        result += '\t<title>' + title + '</title>\n'
        result += '\t<topicmeta>\n'
        result += '\t<author> ' + author + ' </author>\n'

        result += '\t<critdates>\n'
        result += '\t<created date=\" ' + str(now) + '\" />\n'
        result += '\t</critdates>\n'
        result += '\t</topicmeta>\n'
        result += ' <topicref href=\"' +ditaTitle + '\"/>\n'
        result += '</map>'
        return result

