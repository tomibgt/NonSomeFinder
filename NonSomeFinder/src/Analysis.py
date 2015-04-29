'''
Created on Apr 27, 2015

@author: bgt
'''

def getCsvHeaderRow():
    return "true/false;project;readme URL;hot file URL;project URL"

class Analysis(object):
    '''
    This class represents the analysis outcome of an investigated repository.
    If the investigated repository matches what was sought, the first item of this
    object is True, otherwise False.
    If the condition can be determined from a file in the repository, this file is the
    second item of this object.
    '''

    def __init__(self, repository):
        '''
        Constructor
        '''
        self.positive        = False
        self.projectName     = repository.full_name
        self.confirmationUrl = ""
        self.readmeUrl       = ""
        self.projectUrl      = repository.html_url

    def getCsv(self):
        reva = ""
        if self.positive:
            reva += "true"
        else:
            reva += "false"
        reva += ";"+self.projectName
        reva += ";"+self.readmeUrl
        reva += ";"+self.confirmationUrl
        reva += ";"+self.projectUrl
        return reva
                
    def setPositive(self, indicatorFile):
        self.positive        = True
        self.confirmationUrl = indicatorFile.html_url

    def setReadmeFile(self, readmeFile):
        self.readmeUrl   = readmeFile.html_url
        
    