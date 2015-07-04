'''
Created on Jul 4, 2015

@author: bgt
'''

import ProcessDistributionDao

class GitHubFacadeForProcessDistibutionDao(ProcessDistributionDao.ProcessDistributionDao):
    
    def __init__(self, delegatepath, connection):
        super(GitHubFacadeForProcessDistibutionDao, self).__init__(delegatepath, False)
        self.connection = connection
        
    def next(self):
        reponame = super(GitHubFacadeForProcessDistibutionDao, self).next()
        print 'reponame: '+reponame
        return self.connection.getRepositoryByFullName(reponame)
        