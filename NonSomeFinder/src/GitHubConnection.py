import datetime
import time
import NonSomeFinder
from github import Github


class GitHubConnection(object):
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
    
