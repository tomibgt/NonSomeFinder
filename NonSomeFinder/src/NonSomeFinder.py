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
    remains = seconds
    actualSeconds = remains-60*int(remains/60) #remove full minutes and bigger
    remains -= actualSeconds
    actualMinutes = int((remains-360*int(remains/360))/60) #remove full hours and covert seconds to minutes
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
    print "Usage: python NonSomeFinder.py searchword"

if __name__ == '__main__':
    if len(sys.argv) != 2:
        printHowToUse()
        sys.exit()
    search = sys.argv[1]
    connection = GitHubDao.GitHubDao()
    csvDao = CsvDao.CsvDao()
    startTime = int(time.time())
    hits = connection.findRepositoriesWithSearchPhrase(search)
    countDooku = 0
    for repo in hits:
        countDooku += 1
        print "Analysing repository #"+str(countDooku)+", "+repo.full_name
        analysis = connection.usesFacebookGraph(repo)
        csvDao.addRow(analysis)
    csvDao.close()
    endTime = int(time.time())
    announceRunTimeFromSeconds(endTime-startTime)
    