'''
Created on Apr 1, 2015

@author: bgt
'''
import unittest
import NonSomeFinder
from GitHubDao import GitHubDao

class FunctionalityTest(unittest.TestCase):

    def setUp(self):
        self.positiveCase="sferik/twitter"
        self.negativeCase="tomibgt/GitHubResearchDataMiner"
        self.gitDao = GitHubDao(user="tomibgt", repo="GitHubResearchDataMiner")

    def testPositiveTwitter(self):
        self.assertTrue(self.gitDao.usesTwitter(self.positiveCase), self.positiveCase+" not detected as positive case.")

    def testNegativeTwitter(self):
        self.assertFalse(self.gitDao.usesTwitter(self.positiveCase), self.negativeCase+" not detected as positive case.")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()