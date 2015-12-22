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
from BgtConfiguration import BgtConfiguration
from BgtConfiguration import BadCommandLineException

def analyseRepositories(hits):
    countDooku = 0
    
    for repo in hits:
        countDooku += 1
        try:
            print "Analysing repository #"+str(countDooku)+", "+repo.full_name+" "+str(repo.id)
            if config.searching == "facebook":
                analysis = connection.usesFacebookGraph(repo)
            else:
                analysis = connection.usesSsl(repo)
            csvDao.addRow(analysis)
        except GithubException:
            print "...except that repository has blocked access"
    csvDao.close()

def delegateRepositories(config, hits):
    minions = ProcessDistributionDao.ProcessDistributionDao(config, True)
    for repo in hits:
        minions.pushToDelegationFile(str(repo.full_name)+','+str(repo.id))

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
    print "Usage: python NonSomeFinder.py [-ssl|-facebook] [-issues] -search searchword outputfile.csv"
    print "Usage: python NonSomeFinder.py [-ssl|-facebook] [-issues] -search searchword [-delegate delegationfile1[,delegationfile2[...]]"
    print "Usage: python NonSomeFinder.py -facebook [-since #id] outputfile.csv"
    print "Usage: python NonSomeFinder.py -facebook [-since #id] [-delegate delegationfile1[,delegationfile2[...]]"
    print "Usage: python NonSomeFinder.py -ssl|-facebook -takeover delegationfile outputfile.csv"

if __name__ == '__main__':
    config = BgtConfiguration()
    try:
        config.readConfigfile(os.path.dirname(__file__)+'/config.cfg')
        config.parseCommandLine(sys.argv)
    except BadCommandLineException as e:
        print e.message
        printHowToUse()
        sys.exit()

    #Ready to start working!
    if config.search != "":
        print "Looking for "+config.search
    connection = GitHubDao.GitHubDao(config)
    if config.outputfile != "":
        csvDao     = CsvDao.CsvDao(config.outputfile)
    startTime = int(time.time())
    if config.delegation == "takeover":   #We will either analyse repositories from a delegation file...
        hits = GitHubFacadeForProcessDistibutionDao(config.delegatepath, connection)
    elif config.search == "":             #...or look through all repositories...
        hits = connection.findAllRepositories(config.sinceid)
    elif config.lookinto == "reponame":   #...or seek by the names of the repositories...
        hits = connection.findRepositoryNamesWithSearchPhrase(config.search)
    else:                          #...or seek for repositories with keyword in issues.
        hits = connection.findRepositoryIssuesWithSearchPhrase(config.search)

    if config.delegation == "delegate":   #Delegate forth the analysing job 
        delegateRepositories(config, hits)
    else:                          #The search result pipe is given as a parameter
        analyseRepositories(hits)
    
    endTime = int(time.time())
    announceRunTimeFromSeconds(endTime-startTime)
