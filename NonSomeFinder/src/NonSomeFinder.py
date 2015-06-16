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
from github.GithubException import GithubException

config = ConfigParser.ConfigParser()
config.readfp(open(os.path.dirname(__file__)+'/config.cfg'))

def analyseRepositories(hits):
    countDooku = 0
    for repo in hits:
        countDooku += 1
        print "Analysing repository #"+str(countDooku)+", "+repo.full_name
        try:
            if searching == "facebook":
                analysis = connection.usesFacebookGraph(repo)
            else:
                analysis = connection.usesSsl(repo)
            csvDao.addRow(analysis)
        except GithubException:
            print "...except that repository has blocked access"
    csvDao.close()

'''
Given the duration of runtime as seconds, this method will print out the duration
as hours, minutes and seconds.
'''
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
    print "Usage: python NonSomeFinder.py [-ssl | -facebook] [-issues] searchword"
    print "Usage: python NonSomeFinder.py -facebook"

if __name__ == '__main__':
    search    = ""
    searching = ""
    lookinto  = "reponame"
    for argh in sys.argv:
        if argh == sys.argv[0]:
            pass
        elif argh == "-facebook":
            searching = "facebook"
        elif argh == "-ssl":
            searching = "ssl"
        elif argh == "-issues":
            lookinto = "issues"
        else:
            search = argh
    print "Looking for "+search
    if search == "" and searching != "facebook":
        printHowToUse()
        sys.exit()
    connection = GitHubDao.GitHubDao()
    csvDao = CsvDao.CsvDao()
    startTime = int(time.time())
    
    if search == "":
        hits = connection.findAllRepositories()
    elif lookinto == "reponame":
        hits = connection.findRepositoryNamesWithSearchPhrase(search)
    else:
        hits = connection.findRepositoryIssuesWithSearchPhrase(search)

    analyseRepositories(hits)        
    
    endTime = int(time.time())
    announceRunTimeFromSeconds(endTime-startTime)
    