from pydocgen.builders.common import Builder

class DitaBuilder(Builder):
    """Master class responsible for generating DITA files
    """
    def __init__(self):
        self.extension = "dita"