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
        items = super(GitHubFacadeForProcessDistibutionDao, self).next().split(',')
        reponame = items[0]
        repoid   = int(items[1])
        print 'reponame: '+reponame+' id: '+str(repoid)
        return self.connection.getRepositoryById(repoid)
        