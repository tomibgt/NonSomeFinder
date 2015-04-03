'''
Created on Nov 14, 2014

@author: bgt
'''

import datetime
import os
import unittest
from GitHubDao import GitHubDao


class ConnectedTest(unittest.TestCase):

    def setUp(self):
        self.gitDao = GitHubDao(user="tomibgt", repo="GitHubResearchDataMiner")

    def testGitHubConnection(self):
        commits = self.gitDao.getCommitMessages()
        validFlag = commits.count('\n') > 2
        self.assertTrue(validFlag, "Cannot draw commit logs from GitHub")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()