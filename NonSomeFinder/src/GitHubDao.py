import datetime
import time
import NonSomeFinder
from github import Github
from github import GithubObject


class GitHubDao(object):
    def __init__(self, user, repo):
        self.gitHubUserName = user
        self.gitHubRepoName = repo
        self.github = Github(NonSomeFinder.config.get('authentication', 'ghusername'), NonSomeFinder.config.get('authentication', 'ghpassword'))
        self.repo = self.github.get_repo(user+"/"+repo)
        
    def getCommitMessages(self):
        commits = self.repo.get_commits()
        reva = ""
        for commit in commits:
            reva = reva + commit.commit.message+"\n"
        return reva

    def usesTwitter(self, projectName):
        print "\n\n{{usesTwitter}}" #bgt debug
        #return self.github.search_code('api%2Etwitter%2Ecom+in:file+repo:'+projectName, GithubObject.NotSet, GithubObject.NotSet)._isBiggerThan(0)
        return self.github.search_code('twitter+in:file+repo:'+projectName, GithubObject.NotSet, GithubObject.NotSet)._isBiggerThan(0)
