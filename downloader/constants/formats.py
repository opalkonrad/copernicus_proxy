class Format:
    def __init__(self, name, extension):
        self.name = name
        self.extension = extension

formats = [Format('.zip file', '.zip'), Format('compressed .tar file', '.tar.gz')]
