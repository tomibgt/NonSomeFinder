'''
Created on Nov 14, 2014
Copied from GitHubResearchDataMiner

@author: bgt
'''

import ConfigParser
import os
import sys
import time
import CsvDao
import GitHubDao

config = ConfigParser.ConfigParser()
config.readfp(open(os.path.dirname(__file__)+'/config.cfg'))

def announceRunTimeFromSeconds(seconds):
    remains = int(seconds)
    actualSeconds = remains-60*int(remains/60) #remove full minutes and bigger
    remains -= actualSeconds
    actualMinutes = int((remains-3600*int(remains/3600))/60) #remove full hours and covert seconds to minutes
    remains -= actualMinutes*60
    actualHours   = int(remains/21600) #convert seconds to hours
    outputString = "Run time:"
    if actualHours>0:
        outputString += " "+str(actualHours)+" hours"
    if actualMinutes>0:
        outputString += " "+str(actualMinutes)+" minutes"
    if actualSeconds>0:
        outputString += " "+str(actualSeconds)+" seconds ("+str(seconds)+" total seconds)"
    print outputString
    
def printHowToUse():
    print "Usage: python NonSomeFinder.py [-ssl] [-issues] searchword"

if __name__ == '__main__':
    search    = ""
    searching = "facebook"
    lookinto  = "reponame"
    for argh in sys.argv:
        if argh == sys.argv[0]:
            pass
        elif argh == "-ssl":
            searching = "ssl"
        elif argh == "-issues":
            lookinto = "issues"
        else:
            search = argh
    print "Looking for "+search
    if search == "":
        printHowToUse()
        sys.exit()
    connection = GitHubDao.GitHubDao()
    csvDao = CsvDao.CsvDao()
    startTime = int(time.time())
    if lookinto == "reponame":
        hits = connection.findRepositoryNamesWithSearchPhrase(search)
    else:
        hits = connection.findRepositoryIssuesWithSearchPhrase(search)
    countDooku = 0
    for repo in hits:
        countDooku += 1
        print "Analysing repository #"+str(countDooku)+", "+repo.full_name
        if searching == "facebook":
            analysis = connection.usesFacebookGraph(repo)
        else:
            analysis = connection.usesSsl(repo)
        csvDao.addRow(analysis)
    csvDao.close()
    endTime = int(time.time())
    announceRunTimeFromSeconds(endTime-startTime)
    