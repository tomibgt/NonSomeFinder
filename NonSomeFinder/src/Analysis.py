'''
Created on Apr 27, 2015

@author: bgt
'''

class Analysis(object):
    '''
    This class represents the analysis outcome of an investigated repository.
    If the investigated repository matches what was sought, the first item of this
    object is True, otherwise False.
    If the condition can be determined from a file in the repository, this file is the
    second item of this object.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def getCsvHeaderRow(self):
        return "true/false;fileURL"

    