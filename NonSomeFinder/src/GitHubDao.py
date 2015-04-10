import datetime
import time
import urllib2
import NonSomeFinder
import github
from github import Github
from github import GithubObject


class GitHubDao(object):
    def __init__(self, user, repo):
        self.gitHubUserName = user
        self.gitHubRepoName = repo
        self.github = Github(NonSomeFinder.config.get('authentication', 'ghusername'), NonSomeFinder.config.get('authentication', 'ghpassword'))

    def parseRepositoriesFromUrl(self, urlToParse):
        data = urllib2.urlopen(urlToParse).read()
        reva = data.split('://github.com/')
        i = 0;
        while(i<len(reva)):
            bit = reva[i]
            j = 0
            while(j<=len(bit) and bit[j] in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"):
                j += 1
            if(j+2>len(bit) or bit[j] != "/"):
                del reva[i]
            else:
                j += 1
                while(j<=len(bit) and bit[j] in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"):
                    j += 1
                reva[i] = reva[i][0:j]
                i += 1
        return reva
        
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
    