'''
Created on Aug 20, 2015
A class that reads configuration from a configuration file and command line parameters,
and gives out this information.

@author: bgt
'''

import ConfigParser

class BgtConfiguration(object):
    '''
    classdocs
    '''

    def __init__(self):
        self.fileConfig = None

        self.search         = ""
        self.searching      = ""
        self.lookinto       = "reponame"
        self.sinceid        = 0
        self.delegation     = "none"
        self.delegatepath   = ""
        self.outputfile     = ""
    
    def get(self, section, option):
        return self.fileConfig.get(section, option)
    
    def parseCommandLine(self, argv):
        delegateflag   = False
        searchwordflag = False
        sinceidflag    = False
        for argh in argv:       #Parse command line parameters
            if argh == argv[0]:
                pass
            elif sinceidflag:
                self.sinceid = int(argh)
                sinceidflag = False
            elif delegateflag:
                self.delegatepath = argh
                delegateflag = False
            elif searchwordflag:
                self.search = argh
            elif argh == "-delegate":
                delegateflag = True
                self.delegation = "delegate"
            elif argh == "-facebook":
                self.searching = "facebook"
            elif argh == "-ssl":
                self.searching = "ssl"
            elif argh == "-issues":
                self.lookinto = "issues"
            elif argh == "-search":
                searchwordflag = True
            elif argh == "-since":
                sinceidflag = True
                if self.searching != "facebook":
                    raise BadCommandLineException("Can only use '-since' with '-facebook'.")
            elif argh == "-takeover":
                delegateflag = True
                self.delegation = "takeover"
            else:
                outputfile = argh
        #Validate the parameters
        if sinceidflag:
            raise BadCommandLineException("'-since' required the ID of the repository from which to start.")
        if self.outputfile == "" and self.delegation != "delegate":
            raise BadCommandLineException("If you are not delegating the work, you must give the outputfile.")
        if self.search == "" and self.searching != "facebook":
            raise BadCommandLineException("If you are not using -facebook, you must give searchword.")

    def readConfigfile(self, configFilePathName):
        self.fileConfig = ConfigParser.ConfigParser()
        self.fileConfig.readfp(open(configFilePathName))

class BadCommandLineException(Exception):
    pass

        