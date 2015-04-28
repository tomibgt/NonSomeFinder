'''
Created on Nov 14, 2014
Copied from GitHubResearchDataMiner

@author: bgt
'''

import ConfigParser
import os
import sys
import CsvDao
import GitHubDao

config = ConfigParser.ConfigParser()
config.readfp(open(os.path.dirname(__file__)+'/config.cfg'))

def printHowToUse():
    print "Usage: python NonSomeFinder.py searchword"

if __name__ == '__main__':
    if len(sys.argv) != 2:
        printHowToUse()
        sys.exit()
    search = sys.argv[1]
    connection = GitHubDao.GitHubDao()
    csvDao = CsvDao.CsvDao()
    hits = connection.findRepositoriesWithSearchPhrase(search)
    for repo in hits:
        print "Analysing repository "+repo.full_name
        analysis = connection.usesFacebookGraph(repo)
        csvDao.addRow(analysis)
    csvDao.close()
    