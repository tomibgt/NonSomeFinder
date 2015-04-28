import datetime
import sys
import time
import urllib2
import Analysis
import NonSomeFinder
import github
from github import Github
from github import GithubObject


class GitHubDao(object):
    def __init__(self):
        self.github = Github(NonSomeFinder.config.get('authentication', 'ghusername'), NonSomeFinder.config.get('authentication', 'ghpassword'))

    def findRepositoriesWithSearchPhrase(self, searchPhrase):
        repos = self.github.search_repositories(searchPhrase)
        return repos

    def parseRepositoriesFromUrl(self, urlToParse):
        data = urllib2.urlopen(urlToParse).read()
        reva = data.split('://github.com/')
        i = 0;
        while(i<len(reva)):
            bit = reva[i]
            j = 0
            while(j<=len(bit) and bit[j] in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-"):
                j += 1
            if(j+2>len(bit) or bit[j] != "/"):
                del reva[i]
            else:
                j += 1
                while(j<=len(bit) and bit[j] in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-"):
                    j += 1
                reva[i] = reva[i][0:j]
                i += 1
        return reva
    
    """
    :Investigates if given project uses the Facebook Graph API.
    :param repository: :class:`github.Repository.Repository`
    :rtype: :class:`Analysis.Analysis`
    """
    def usesFacebookGraph(self, repository):
        qualifiers = {'in':'file', 'repo':repository.full_name}
        result = self.github.search_code('"graph.facebook.com"', sort=GithubObject.NotSet, order=GithubObject.NotSet, **qualifiers)
        analysis = Analysis.Analysis(repository)
        for item in result:
            analysis.setPositive(item)
        return analysis
        
    def usesTwitter(self, projectName):
        """
        :Investigates if given project uses the twitter API.
        :param projectName: string The project name in format 'author/projectname'
        :rtype: boolean True if the project uses API , :class:`github.PaginatedList.PaginatedList` of :class:`github.ContentFile.ContentFile` files that refer to the API
        """
        qualifiers = {'in':'file', 'repo':projectName}
        result = self.github.search_code('api.twitter.com', sort=GithubObject.NotSet, order=GithubObject.NotSet, **qualifiers)
        positive = False
        for item in result:
            positive = True
        return positive, result
    