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
from GitHubFacadeForProcessDistibutionDao import GitHubFacadeForProcessDistibutionDao
from github.GithubException import GithubException
import ProcessDistributionDao

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

def delegateRepositories(hits, delegatepath):
    minions = ProcessDistributionDao.ProcessDistributionDao(delegatepath, True)
    for repo in hits:
        minions.pushToDelegationFile(repo.full_name)

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
    print "Usage: python NonSomeFinder.py [-ssl | -facebook] [-issues] [-delegate delegationfile1[,delegationfile2[...]] searchword"
    print "Usage: python NonSomeFinder.py -facebook [-delegate delegationfile1[,delegationfile2[...]] [-since #id]"
    print "Usage: python NonSomeFinder.py -ssl | -facebook -takeover delegationfile"

if __name__ == '__main__':
    search    = ""
    searching = ""
    lookinto  = "reponame"
    sinceid   = 0
    sinceidflag = False
    delegation = "none"
    delegatepath = ""
    delegateflag = False
    for argh in sys.argv:       #Parse command line parameters
        if argh == sys.argv[0]:
            pass
        elif sinceidflag:
            sinceid = int(argh)
            sinceidflag = False
        elif delegateflag:
            delegatepath = argh
            delegateflag = False
        elif argh == "-delegate":
            delegateflag = True
            delegation = "delegate"
        elif argh == "-facebook":
            searching = "facebook"
        elif argh == "-ssl":
            searching = "ssl"
        elif argh == "-issues":
            lookinto = "issues"
        elif argh == "-since":
            sinceidflag = True
            if searching != "facebook":
                print "Can only use '-since' with '-facebook'."
                printHowToUse()
                sys.exit()
        elif argh == "-takeover":
            delegateflag = True
            delegation = "takeover"
        else:
            search = argh
    if sinceidflag:
        print "'-since' required the ID of the repository from which to start."
        printHowToUse()
        sys.exit()
    if search != "":
        print "Looking for "+search
    if search == "" and searching != "facebook":
        printHowToUse()
        sys.exit()
    connection = GitHubDao.GitHubDao()
    csvDao = CsvDao.CsvDao()
    startTime = int(time.time())
    if delegation == "takeover":   #We will either analyse repositories from a delegation file...
        hits = GitHubFacadeForProcessDistibutionDao(delegatepath, connection)
    elif search == "":             #...or look through all repositories...
        hits = connection.findAllRepositories(sinceid)
    elif lookinto == "reponame":   #...or seek by the names of the repositories...
        hits = connection.findRepositoryNamesWithSearchPhrase(search)
    else:                          #...or seek for repositories with keyword in issues.
        hits = connection.findRepositoryIssuesWithSearchPhrase(search)

    if delegation == "delegate":   #Delegate forth the analysing job 
        delegateRepositories(hits, delegatepath)
    else:                          #The search result pipe is given as a parameter
        analyseRepositories(hits)
    
    endTime = int(time.time())
    announceRunTimeFromSeconds(endTime-startTime)

