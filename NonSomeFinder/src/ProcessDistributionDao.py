'''
Created on Jul 3, 2015

@author: bgt
'''
import errno
import fcntl
import time

class ProcessDistributionDao(object):
    '''
    classdocs
    '''


    def __init__(self, delegationfiles, delegator=True):
        '''
        Constructor
        '''
        self.delegationFileNames = delegationfiles.split(',')
        self.delegationFileHandles = []
        self.delegationFileRowCounts = []
        self.delegationFileIterator = DelegationFileIterator(len(self.delegationFileNames))
        self.delegator = delegator;
        self.takeover  = not delegator;
        if len(self.delegationFileNames) < 1:
            raise NoFileNamesException('No filenames given as delegation queue files.')
        if self.takeover and len(self.delegationFileNames) > 1:
            raise TooManyFilenamesException('When taking over delegated queue, only one file should be given as a parameter.')
        #Open the delegation files
        mode = 'a'
        if self.takeover:
            mode = 'r+'
        for filename in self.delegationFileNames:
            self.delegationFileHandles.append(open(filename, mode))
            self.delegationFileRowCounts.append(0) #Each file initially considered empty
            
    def __iter__(self):
        return self
    
    def getLengthOfDelegationFile(self, idnumber):
        linecount = 0
        with open(self.delegationFileNames[idnumber]) as infp:
            for line in infp:
                linecount += 1
        self.delegationFileRowCounts[idnumber] = linecount
        return linecount
    
    def next(self):
        return self.popFromDelegationFile()

    def popFromDelegationFile(self):
        fileRow = ""
        sleepLength = 0.1
        while fileRow == "": #Read the first row from the file with locking
            try:
                fcntl.flock(self.delegationFileHandles[0], fcntl.LOCK_EX | fcntl.LOCK_NB)
                fileRow = self.delegationFileHandles[0].readline()
            except IOError as e:
                if e.errno != errno.EAGAIN:
                    raise
            else:
                time.sleep(sleepLength)
                sleepLength = sleepLength * 2.0
        #remove the row just read
        handle = (open(self.delegationFileNames[0], 'r+'))
        handle.seek(0)
        for segment in iter(lambda: self.delegationFileHandles[0].read(2), ''):
            handle.write(segment)
        handle.truncate()
        handle.flush()
        self.delegationFileHandles[0].seek(0)
        fcntl.flock(self.delegationFileHandles[0], fcntl.LOCK_UN)
        return fileRow 

    def pushToDelegationFile(self, fileRow):
        #Discover the shortest queue
        while self.getLengthOfDelegationFile(self.delegationFileIterator.current) > min(self.delegationFileRowCounts):
            self.delegationFileIterator.next()
        sleepLength = 0.1
        unstored = True
        handle = self.delegationFileHandles[self.delegationFileIterator.current]
        while unstored: #Repeat until storing succeeds
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                handle.write(fileRow+'\n')
                handle.flush()
                unstored = False
            except IOError as e:
                if e.errno != errno.EAGAIN:
                    raise
            else:
                time.sleep(sleepLength)
                sleepLength = sleepLength * 2.0
        fcntl.flock(handle, fcntl.LOCK_UN)
    
class DelegationFileIterator(object):

    def __init__(self, maximum):
        self.range = maximum
        self.current = 0
        if self.range < 1:
            raise ValueError('DelegationFileIterator given range less than 1.')
    
    def __iter__(self):
        return self
    
    def current(self):
        return self.current
    
    def next(self):
        reva = self.current
        self.current += 1
        if self.current >= self.range:
            self.current = 0
        return reva
        
class NoFileNamesException(Exception):
    pass

class TooManyFilenamesException(Exception):
    pass
