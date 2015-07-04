import time
import urllib2
import Analysis
import NonSomeFinder
from github import Github
from github import GithubException
from github import GithubObject
from github.GithubObject import NotSet


class GitHubDao(object):
    def __init__(self):
        self.github = Github(NonSomeFinder.config.get('authentication', 'ghusername'), NonSomeFinder.config.get('authentication', 'ghpassword'))

    #This method is used to limit the rate of requests sent to GitHub
    def __choke(self):
        if NonSomeFinder.config.get('debug', 'verbose'):
            print "Sleep? rate_limiting:"+str(self.github.rate_limiting[0])+" resettime:"+str(self.github.rate_limiting_resettime)+" currenttime:"+str(time.time())
        if self.github.rate_limiting[0]<3:
            naptime = self.github.rate_limiting_resettime-int(time.time())+1
            if NonSomeFinder.config.get('debug', 'verbose'):
                print "Sleeping "+str(naptime)+" seconds..."
            time.sleep(naptime)

    def findAllRepositories(self, sinceid):
        self.__choke()
        if sinceid == 0:
            repos = self.github.get_repos()
        else:
            repos = self.github.get_repos(sinceid)
        return repos
        
    def findRepositoryIssuesWithSearchPhrase(self, searchPhrase):
        self.__choke()
        issues = self.github.search_issues(searchPhrase, NotSet, NotSet)
        repos = []
        for issue in issues:
            if NonSomeFinder.config.get('debug', 'verbose'):
                print "Issue:"+issue.title.encode('ascii', 'xmlcharrefreplace')+", repo:"+issue.repository.full_name.encode('ascii', 'xmlcharrefreplace')
            notFound = True
            for repo in repos:
                if repo == issue.repository:
                    found = False
            if notFound:
                repos.append(issue.repository)
        return repos

    def findRepositoryNamesWithSearchPhrase(self, searchPhrase):
        self.__choke()
        repos = self.github.search_repositories(searchPhrase)
        return repos
    
    def getRepositoryByFullName(self, fullname):
        self.__choke()
        repo = self.github.get_repo(str(fullname), True)
        return repo

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
        self.__choke()
        result = self.github.search_code('"graph.facebook.com"', sort=GithubObject.NotSet, order=GithubObject.NotSet, **qualifiers)
        analysis = Analysis.Analysis(repository)
        self.__choke()
        try:
            commits = repository.get_commits()
            #Apparently we have to get the count the hard way, as this list doesn't have a method to
            #request the total count.
            #Same applies to fetching the last commit day
            commitCount = 0
            lastCommitDate = analysis.createdAt
            for commit in commits:
                commitCount += 1
                if analysis.lastCommitDate == "" or analysis.getLastCommitDatetime()<commit.date:
                    analysis.setLastCommitDate(commit.date)
            analysis.setCommitCount(commitCount)
        except GithubException:
            pass
        except:
            pass
        discovered = False
        for item in result:
            analysis.setPositive(item)
            discovered = True
        if discovered:
            qualifiers = {'in':'path', 'repo':repository.full_name}
            self.__choke()
            result = self.github.search_code('README.md', sort=GithubObject.NotSet, order=GithubObject.NotSet, **qualifiers)
            for item in result:
                analysis.setReadmeFile(item)
        return analysis
        
    """
    :Investigates if given project uses the Facebook Graph API.
    :param repository: :class:`github.Repository.Repository`
    :rtype: :class:`Analysis.Analysis`
    """
    def usesSsl(self, repository):
        qualifiers = {'in':'file', 'repo':repository.full_name}
        self.__choke()
        result = self.github.search_code('"javax.net.ssl"', sort=GithubObject.NotSet, order=GithubObject.NotSet, **qualifiers)
        analysis = Analysis.Analysis(repository)
        self.__choke()
        try:
            commits = repository.get_commits()
            #Apparently we have to get the count the hard way, as this list doesn't have a method to
            #request the total count.
            #Same applies to fetching the last commit day
            commitCount = 0
            lastCommitDate = analysis.createdAt
            for commit in commits:
                commitCount += 1
                if analysis.lastCommitDate == "" or analysis.getLastCommitDatetime()<commit.date:
                    analysis.setLastCommitDate(commit.date)
            analysis.setCommitCount(commitCount)
        except GithubException:
            pass
        except:
            pass
        discovered = False
        for item in result:
            analysis.setPositive(item)
            discovered = True
        if discovered:
            qualifiers = {'in':'path', 'repo':repository.full_name}
            self.__choke()
            result = self.github.search_code('README.md', sort=GithubObject.NotSet, order=GithubObject.NotSet, **qualifiers)
            for item in result:
                analysis.setReadmeFile(item)
        return analysis

    def usesTwitter(self, projectName):
        """
        :Investigates if given project uses the twitter API.
        :param projectName: string The project name in format 'author/projectname'
        :rtype: boolean True if the project uses API , :class:`github.PaginatedList.PaginatedList` of :class:`github.ContentFile.ContentFile` files that refer to the API
        """
        qualifiers = {'in':'file', 'repo':projectName}
        self.__choke()
        result = self.github.search_code('api.twitter.com', sort=GithubObject.NotSet, order=GithubObject.NotSet, **qualifiers)
        positive = False
        for item in result:
            positive = True
        return positive, result
    
