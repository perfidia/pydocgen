from pydocgen.builders.common import Builder

class DitaBuilder(Builder):
    """Master class responsible for generating DITA files
    """
    
    def __init__(self):
        self.extension = "dita"
       
    def generateTopic(self, topic):
        result = ''
        result 
        
class DitaTopic(object):
    __topic = None
    __title = None
    __shortdesc = None
    __body = None
    __relatedlinks = []
    
    def getTopic(self):
        result = ''
        result += self.generateTopic()
        result += self.generateTitle()
        result += self.generateShortdesc()
        result += self.generateBody()
        result += self.generateRelatedLinks()
        result += '</topic>'
        
        
    
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
            result += self.__body.getContent()
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
        
        
class Link(object):
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
    
class Content(object):
    """Main class for building DITA documents. 
    Opening of every tag should be added to self.__content
    and closing of every tag should be added do self.__stack.
    To close last opened tag just type self.__stack.pop()
    It should allow to nest elements easily
    """
    __content = None
    __stack = []
    
    def __init__(self):
        self.__content = '' 
        
    def getContent(self):
        while not self.__stack:
            self.__content += self.__stack.pop()
            
    def addSimpleTable(self, table):
        self.__content += '<simpletable>'
        self.__stack.append('</simpletable>')
        # TODO generateTable with content
        self.__stack.pop(); #close table
        
    
class Body(Content):
    __content = None
    __sections = []
    
    def __init__(self):
        self.__content = ''
        self.__content += '<body>'
        self.__stack.append('</body>')
        
    def getBody(self):
        return self
    
    def addSection(self, section):
        self.__content += section.getContent
        

class Section(Content):
    #__content = None
    __title = None
    #__stack = []
    
    def __init__(self, title):
        self.__content = ''
        self.__content += '<section>'
        self.__stack.append('</section>')
        if title != None:
            self.__content += '<title>' + title + '</title>'
            
    
            
            
       
            
    
        
        
        
    
    