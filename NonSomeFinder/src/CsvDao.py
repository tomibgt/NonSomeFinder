'''
Created on Apr 27, 2015

@author: bgt
'''
from Analysis import Analysis

class CsvDao(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        filepath = 'output.csv'
        self.outputFileHandle = open(filepath, 'w')
        self.started = False
        self.outputFileHandle.write(self.getCsvHeaderRow())

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
        
    def close(self):
        '''
        Returns a handle to a csv file
        '''
        self.outputFileHandle.close()

    def getCsvHeaderRow(self):
        '''
        Returns the header row for the output csv file
        '''
        return u"sha;commit date;committed file names;commit additions;commit deletions;commit changes;commit message"

    def getCsvLineFromCommit(self, commit):
        '''
        Parses the given GitHub commit into a row for the csv file.
        '''
        commitcommit  = commit.commit
        commitauthor  = commit.author
        commitfiles   = ""
        commitadds    = ""
        commitdels    = ""
        commitchanges = ""
        comma        = False
        try:
            for afile in commit.files:
                if(comma):
                    commitfiles   = commitfiles+','
                    commitadds    = commitadds+','
                    commitdels    = commitdels+','
                    commitchanges = commitchanges+','
                commitfiles   = commitfiles+afile.filename
                commitadds    = commitadds+str(afile.additions)
                commitdels    = commitdels+str(afile.deletions)
                commitchanges = commitchanges+str(afile.changes)
                comma = True
            if GitHubResearchDataMiner.config.get('debug', 'verbose'):
                print "Read commit "+commit.sha+": "+commitcommit.message+";"+str(commitauthor)
            reva = commit.sha+";"+str(commitauthor.created_at)+";"+commitfiles+";"+commitadds+";"+commitdels+";"+commitchanges+";"+commitcommit.message
            reva = reva.replace('\n', ' ')
        except AttributeError as detail:
            print "Attribute Error for sha("+commit.sha+")", detail
            return(None)
            #raise
            #AttributeErrors are ignored, because some commits have no committer, which causes these errors
            #This means that some of the commits are dropped off
        return reva
