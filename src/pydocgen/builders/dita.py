from pydocgen.builders.common import Builder

class DitaBuilder(Builder):
    """Master class responsible for generating DITA files
    """
    
    def __init__(self):
        self.extension = "dita"
       
    def generateTopic(self, topic):
        result = ''
        result 
        
class DitaTopic:
    __topic = None
    __title = None
    __shortdesc = None
    __body = None
    __relatedlinks = []
    
    def setTopic(self, topic):
        __topic = topic
        
    def generateTopic(self):
        result = ''
        if self.__topic != None:
            result += '<topic id="' + self.__topic + '">'
        return result
            
    def setTitle(self, title):
        __title = title
        
    def generateTitle(self):
        result = ''
        if self.__title != None:
            result += '<title>' + self.__title + '</title>'
        return result
        
    def setShortdesc(self, shortdesc):
        __shortdesc = shortdesc
        
    def generateShortdesc(self):
        result = ''
        if self.__shortdesc != None:
            result += '<shortdesc>' + self.__shortdesc + '</shortdesc>'
        return result
        
    def setBody (self, body):
        __body = body
        
    def generateBody(self):
        result = ''
        if self.__body != None:
            result += '<body>' + self.__body + '</body>'
        return result
        
    def addLink(self, iformat, href, scope):
        self.__relatedlinks.append(Link(iformat, href, scope))
        
    def generateRelatedLinks(self):
        result = ''
        if len(self.__relatedlinks) > 0:
            result += '<related-links>'
            for l in self.__relatedlinks:
                result += '<link format = "' + l.getFormat() + '" href="' + l.getHref() + '" scope="' + l.getScope() + '">'
                result += '<linktext>' + l.getText() + '</linktext>'
                result += '</link>'
        result += '</related-links>'
        return result
        
        
class Link:
    __format = None
    __href = None
    __scope = None
    __text = None
    
    def __init__(self, iformat, href, scope, text):
        self.__format = iformat
        self.__href = href
        self.__scope = scope
        self.__text = text
        
    def getFormat(self):
        return self.__format
    
    def getHref(self):
        return self.__href
    
    def getScope(self):
        return self.__scope
    
    def getText(self):
        return self.__text
    
    def getLink(self):
        return self
    
        
        
        
    
    