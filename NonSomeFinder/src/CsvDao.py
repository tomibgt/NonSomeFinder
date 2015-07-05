'''
Created on Apr 27, 2015

@author: bgt
'''
import Analysis

class CsvDao(object):
    '''
    classdocs
    '''


    def __init__(self, outputpath):
        '''
        Constructor
        '''
        self.outputFileHandle = open(outputpath, 'w')
        self.started = False
        #self.outputFileHandle.write(Analysis.getCsvHeaderRow())

    def addRow(self, analysis):
        '''
        Adds a row in the csv-file
        '''
        if not self.started:
            line = Analysis.getCsvHeaderRow()+'\n'
            self.outputFileHandle.write(line.encode("utf-8"))
            self.started = True
        line = analysis.getCsv()+'\n'
        self.outputFileHandle.write(line.encode("utf-8"))
        self.outputFileHandle.flush()
        
    def close(self):
        '''
        Returns a handle to a csv file
        '''
        self.outputFileHandle.close()

