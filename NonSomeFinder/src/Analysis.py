'''
Created on Apr 27, 2015

@author: bgt
'''

import datetime

def getCsvHeaderRow():
    return "true/false;project;created;commits;last commit;readme URL;hot file URL;project URL"

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
        self.createdAt       = str(repository.created_at.year)+":"+str(repository.created_at.month)+":"+str(repository.created_at.day)
        self.lastCommitDate  = ""
        self.commitCount     = "0"
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
        reva += ";"+self.createdAt
        reva += ";"+self.commitCount
        reva += ";"+self.lastCommitDate
        reva += ";"+self.readmeUrl
        reva += ";"+self.confirmationUrl
        reva += ";"+self.projectUrl
        return reva
    
    def getCreatedAtDatetime(self):
        reva = datetime.datetime.strptime(self.createdAt, "%Y:%m:%d")
        return reva
    
    def getLastCommitDatetime(self):
        reva = datetime.datetime.strptime(self.lastCommitDate, "%Y:%m:%d")
        return reva
    
    def setCommitCount(self, count):
        self.commitCount = str(count)

    def setLastCommitDate(self, theDate):
        self.lastCommitDate = str(theDate.year)+":"+str(theDate.month)+":"+str(theDate.day)
                        
    def setPositive(self, indicatorFile):
        self.positive        = True
        self.confirmationUrl = indicatorFile.html_url

    def setReadmeFile(self, readmeFile):
        self.readmeUrl   = readmeFile.html_url
        
    