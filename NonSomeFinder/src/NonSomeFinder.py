'''
Created on Nov 14, 2014
Copied from GitHubResearchDataMiner

@author: bgt
'''

import ConfigParser
import os
import sys
import GitHubDao

config = ConfigParser.ConfigParser()
config.readfp(open(os.path.dirname(__file__)+'/config.cfg'))

if __name__ == '__main__':
    search = sys.argv[1]
    connection = GitHubDao.GitHubDao(user=user, repo=repo)
    connection.getCsv()
    