#coding = 'utf-8'

__author__ = 'xieyajie'

from model import DXRequest

BASE_HEADERS = {'Content-Type': 'application/json',
               'Accept': 'application/json'}

class EMPyClient(object):

    def __init__(self, aAppkey, aRestBaseUrl):
        self.appkey = aAppkey
        self.restBaseUrl = aRestBaseUrl
        print('EMPyClient init')

    def __del__(self):
        print('EMPyClient del')

    def createNewUser(self, aUsername, aPassword):
        if len(aUsername) == 0 or len(aPassword) == 0:
            return None

        url = self.restBaseUrl + '/users'
        body = {'username': aUsername, 'password': aPassword}
        response = DXRequest.put(url, BASE_HEADERS, body)
        if response.code != 0:
            print('\n Create %s failed:%s' %(aUsername, response.data))

        return response


    def getUserToken(self, aUsername, aPassword):
        if len(aUsername) == 0 or len(aPassword) == 0:
            return ''

        url = self.restBaseUrl + '/token'
        body = {'grant_type': 'password', 'username': aUsername, 'password': aPassword}
        response = DXRequest.post(url, BASE_HEADERS, body)
        if response.code == 0:
            self.username = aUsername
            self.password = aPassword
            self.token = response.data['access_token']
            self.restToken = 'Bearer ' + self.token
            return self.token

        print(response.data)
        return ''

    def getAdminToken(self, aID, aSecret):
        if len(aID) == 0 or len(aSecret) == 0:
            print('client_id or client_secret is empty')
            return ''

        url = self.restBaseUrl + '/token'
        body = {'grant_type': 'client_credentials',
                'client_id': aID,
                'client_secret': aSecret}
        response = DXRequest.post(url, BASE_HEADERS, body)
        if response.code == 0:
            self.clientId = aID
            self.clientSecret = aSecret
            self.adminToken = response.data['access_token']
            self.adminRestToken = 'Bearer ' + self.adminToken
            return self.adminToken

        print(response.data)
        return ''


    def getContacts(self):
        if len(self.token) == 0:
            print('请先进行第1项:获取token')
            return ''

        url = self.restBaseUrl + '/users/' + self.username + '/contacts/users'
        headers = dict({'Authorization': self.restToken})
        headers.update(BASE_HEADERS)
        response = DXRequest.get(url, headers, None)
        if response.code == 0:
            contacts = response.data['data']
            return contacts

        print(response.data)
        return ''

    def getBlackContacts(self):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return ''

        url = self.restBaseUrl + '/users/' + self.username + '/blocks/users'
        headers = dict({'Authorization': self.restToken})
        headers.update(BASE_HEADERS)
        response = DXRequest.get(url, headers, None)
        if response.code == 0:
            blacks = response.data['data']
            return blacks

        print(response.data)
        return ''

    def optionContacts(self, aMethod, aUsername, aBody = None):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return 0

        if len(aUsername) == 0:
            print('用户名为空')
            return 0

        url = self.restBaseUrl + '/users/' + self.username + '/contacts/users/' + aUsername
        headers = dict({'Authorization': self.restToken})
        headers.update(BASE_HEADERS)
        response = DXRequest.httpRequest(url, headers, aBody, aMethod)
        return response

    def addUser(self, aUsername):
        response = self.optionContacts('POST', aUsername, {'username':aUsername})
        if response.code != 0:
            print('add user failed:%s' %(response.data))
        return response.code

    def deleteUser(self, aUsername):
        response = self.optionContacts('DELETE', aUsername)
        if response.code != 0:
            print('delete user failed:%s' %(response.data))
        return response.code

    def addUserToBlack(self, aUsername):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return 0

        if len(aUsername) == 0:
            print('用户名为空')
            return 0

        url = self.restBaseUrl + '/users/' + self.username + '/blocks/users'
        headers = dict({'Authorization': self.restToken})
        headers.update(BASE_HEADERS)
        body = dict({'usernames': [aUsername]})
        response = DXRequest.post(url, headers, body)

        if response.code != 0:
            print('block user failed:%s' %(response.data))
        return response.code

    def removeUserFromBlack(self, aUsername):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return 0

        if len(aUsername) == 0:
            print('用户名为空')
            return 0

        url = self.restBaseUrl + '/users/' + self.username + '/blocks/users/' + aUsername
        headers = dict({'Authorization': self.restToken})
        headers.update(BASE_HEADERS)
        response = DXRequest.delete(url, headers, None)

        if response.code != 0:
            print('unblock user failed:%s' %(response.data))
        return response.code


    def createGroup(self, aSubject = '', aDescribe = '', aMaxUsers = 300, aMembers = None, aIsPublic = True, aApproval = True):
        if len(self.adminToken) == 0:
            print('请先进行获取管理员token操作')
            return 0

        if len(self.token) == 0:
            print('请先进行获取token操作')
            return 0

        if len(aSubject) == 0:
            print('群主题为空')
            return 0

        url = self.restBaseUrl + '/chatgroups'
        headers = dict({'Authorization': self.adminRestToken})
        headers.update(BASE_HEADERS)

        body = {'groupname':aSubject,
                'desc':aDescribe,
                'owner':self.username,
                'public':aIsPublic,
                'approval':aApproval,
                'maxusers':aMaxUsers}
        if aMembers != None and len(aMembers):
            body.update({'members':aMembers})

        response = DXRequest.post(url, headers, body)

        if response.code != 0:
            print('create group failed:%s' %(response.data))
        return response.code

    def exitGroup(self, aGroupId):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return None

        if len(aGroupId) == 0:
            print('群组ID为空')
            return None

        url = self.restBaseUrl + '/chatgroups/' + aGroupId
        headers = dict({'Authorization': self.restToken})
        headers.update(BASE_HEADERS)
        response = DXRequest.delete(url, headers, None)

        if response.code != 0:
            print('delete group failed:%s' %(response.data))
        return response.code

    def getCurrentUserGroups(self):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return 0

        url = self.restBaseUrl + '/users/' + self.username + '/joined_chatgroups'
        headers = dict({'Authorization': self.restToken})
        headers.update(BASE_HEADERS)
        response = DXRequest.get(url, headers, None)
        groups = response.data['data']

        if response.code != 0:
            print('get groups failed:%s' %(response.data))
        return groups

    def getGroupInfo(self, aGroupId):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return None

        if len(aGroupId) == 0:
            print('群组ID为空')
            return None

        url = self.restBaseUrl + '/chatgroups/' + aGroupId
        headers = dict({'Authorization': self.restToken})
        headers.update(BASE_HEADERS)
        response = DXRequest.get(url, headers, None)

        if response.code != 0:
            print('get group info failed:%s' %(response.data))
        return response.data['data']

    def editGroupInfo(self, aGroupId, aSubject = None, aDescribe = None, aMaxUsers = -1):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return None

        if len(aGroupId) == 0:
            print('群组ID为空')
            return None

        if aSubject == None and aDescribe == None and aMaxUsers == -1:
            return None

        url = self.restBaseUrl + '/chatgroups/' + aGroupId
        headers = dict({'Authorization': self.restToken})
        headers.update(BASE_HEADERS)

        body = {}
        if aSubject != None:
            body.update({'groupname':aSubject})
        if aDescribe != None:
            body.update({'description':aDescribe})
        if aMaxUsers > 0:
            body.update({'maxusers':aMaxUsers})

        response = DXRequest.put(url, headers, body)

        if response.code != 0:
            print('edit group info failed:%s' %(response.data))
        return response.data['data']

    def getGroupMembers(self, aGroupId):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return None
        if len(aGroupId) == 0:
            print('群组ID为空')
            return None

        url = self.restBaseUrl + '/chatgroups/' + aGroupId + '/users'
        headers = dict({'Authorization': self.restToken})
        headers.update(BASE_HEADERS)
        response = DXRequest.get(url, headers, None)

        if response.code != 0:
            print('get group members failed:%s' %(response.data))
        return response.data['data']

    def addGroupMember(self, aGroupId, aUsername):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return None
        if len(aGroupId) == 0 or len(aUsername) == 0:
            print('参数为空')
            return None

        url = self.restBaseUrl + '/chatgroups/' + aGroupId + '/users'
        headers = dict({'Authorization': self.restToken})
        headers.update(BASE_HEADERS)

        body = dict({'usernames':[aUsername]})
        response = DXRequest.post(url, headers, body)

        if response.code != 0:
            print('add group member failed:%s' %(response.data))
        return response.data['data']

    def deleteGroupMember(self, aGroupId, aUsername):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return None
        if len(aGroupId) == 0 or len(aUsername) == 0:
            print('参数为空')
            return None

        url = self.restBaseUrl + '/chatgroups/' + aGroupId + '/users/' + aUsername
        headers = dict({'Authorization': self.restToken})
        headers.update(BASE_HEADERS)
        response = DXRequest.delete(url, headers, None)

        if response.code != 0:
            print('add group member failed:%s' %(response.data))
        return response.data['data']

    def getGroupBlacks(self, aGroupId):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return None
        if len(aGroupId) == 0:
            print('群组ID为空')
            return None

        url = self.restBaseUrl + '/chatgroups/' + aGroupId + '/blocks/users'
        headers = dict({'Authorization': self.restToken})
        headers.update(BASE_HEADERS)
        response = DXRequest.get(url, headers, None)

        if response.code != 0:
            print('get group blocks failed:%s' %(response.data))
        return response.data['data']

    def addUserToGroupBlock(self, aGroupId, aUsername):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return None
        if len(aGroupId) == 0 or len(aUsername) == 0:
            print('参数为空')
            return None

        url = self.restBaseUrl + '/chatgroups/' + aGroupId + '/blocks/users'
        headers = dict({'Authorization': self.restToken})
        headers.update(BASE_HEADERS)

        body = dict({'usernames':[aUsername]})
        response = DXRequest.post(url, headers, body)

        if response.code != 0:
            print('add group block failed:%s' %(response.data))
        return response.data['data']

    def removeUserFromGroupBlock(self, aGroupId, aUsername):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return None
        if len(aGroupId) == 0 or len(aUsername) == 0:
            print('参数为空')
            return None

        url = self.restBaseUrl + '/chatgroups/' + aGroupId + '/blocks/users/' + aUsername
        headers = dict({'Authorization': self.restToken})
        headers.update(BASE_HEADERS)
        response = DXRequest.delete(url, headers, None)

        if response.code != 0:
            print('remove group block failed:%s' %(response.data))
        return response.data['data']


