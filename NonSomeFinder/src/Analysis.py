'''
Created on Apr 27, 2015

@author: bgt
'''
from github.Repository import Repository

def getCsvHeaderRow():
    return "true/false;project;fileURL"

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

    def getCsv(self):
        reva = ""
        if self.positive:
            reva += "true;"
        else:
            reva += "false;"
        reva += self.projectName+";"
        reva += self.confirmationUrl
        return reva
                
    def setPositive(self, indicatorFile):
        self.positive        = True
        self.confirmationUrl = indicatorFile.html_url
        
    