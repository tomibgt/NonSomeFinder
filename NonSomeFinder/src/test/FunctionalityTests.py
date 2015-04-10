'''
Created on Apr 1, 2015

@author: bgt
'''
import unittest
from GitHubDao import GitHubDao

class FunctionalityTest(unittest.TestCase):

    def setUp(self):
        self.positiveCase="sferik/twitter"
        self.negativeCase="tomibgt/GitHubResearchDataMiner"
        self.urlToParse="http://tucs.fi/bgt/github.html"
        self.gitDao = GitHubDao(user="tomibgt", repo="GitHubResearchDataMiner")

    '''
    Issue #1
    '''
    def testPositiveTwitter(self):
        self.assertTrue(self.gitDao.usesTwitter(self.positiveCase)[0], self.positiveCase+" not detected as positive case.")

    def testNegativeTwitter(self):
        self.assertFalse(self.gitDao.usesTwitter(self.negativeCase)[0], self.negativeCase+" not detected as negative case.")

    '''
    Issue #2
    '''
    def testUrlParsing(self):
        result = self.gitDao.parseRepositoriesFromUrl(self.urlToParse);
        self.assertTrue(len(result)==2, "The parser failed to detect two URLs on the test page : "+str(len(result)))
        self.assertEqual(result[0], "sferik/twitter", "Missparsed sferik/twitter : "+result[0])
        self.assertEqual(result[1], "tomibgt/GitHubResearchDataMiner", "Missparsed tomibgt/GitHubResearchDataMiner : "+result[1])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()