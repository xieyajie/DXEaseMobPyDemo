#coding = 'utf-8'

__author__ = 'xieyajie'

from model import dx_request

BASE_HEADERS = {'Content-Type': 'application/json',
               'Accept': 'application/json'}

class PyClient(object):

    def __init__(self, appkey, rest_base_url):
        self.appkey = appkey
        self.rest_base_url = rest_base_url
        print('EMPyClient init')

    def __del__(self):
        print('EMPyClient del')

    def create_new_user(self, username, password):
        if len(username) == 0 or len(password) == 0:
            return None

        url = self.rest_base_url + '/users'
        body = {'username': username, 'password': password}
        response = dx_request.put(url, BASE_HEADERS, body)
        if response.code != 0:
            print('\n Create %s failed:%s' %(username, response.data))

        return response


    def get_user_token(self, username, password):
        if len(username) == 0 or len(password) == 0:
            return ''

        url = self.rest_base_url + '/token'
        body = {'grant_type': 'password', 'username': username, 'password': password}
        response = dx_request.post(url, BASE_HEADERS, body)
        if response.code == 0:
            self.username = username
            self.password = password
            self.token = response.data['access_token']
            self.rest_token = 'Bearer ' + self.token
            return self.token

        print(response.data)
        return ''

    def get_admin_token(self, client_id, client_secret):
        if len(client_id) == 0 or len(client_secret) == 0:
            print('client_id or client_secret is empty')
            return ''

        url = self.rest_base_url + '/token'
        body = {'grant_type': 'client_credentials',
                'client_id': client_id,
                'client_secret': client_secret}
        response = dx_request.post(url, BASE_HEADERS, body)
        if response.code == 0:
            self.client_id = client_id
            self.client_secret = client_secret
            self.admin_token = response.data['access_token']
            self.admin_rest_token = 'Bearer ' + self.admin_token
            return self.admin_token

        print(response.data)
        return ''


    def get_contacts(self):
        if len(self.token) == 0:
            print('请先进行第1项:获取token')
            return ''

        url = self.rest_base_url + '/users/' + self.username + '/contacts/users'
        headers = dict({'Authorization': self.rest_token})
        headers.update(BASE_HEADERS)
        response = dx_request.get(url, headers, None)
        if response.code == 0:
            contacts = response.data['data']
            return contacts

        print(response.data)
        return ''

    def get_black_contacts(self):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return ''

        url = self.rest_base_url + '/users/' + self.username + '/blocks/users'
        headers = dict({'Authorization': self.rest_token})
        headers.update(BASE_HEADERS)
        response = dx_request.get(url, headers, None)
        if response.code == 0:
            blacks = response.data['data']
            return blacks

        print(response.data)
        return ''

    def __option_contacts(self, method, username, body = None):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return 0

        if len(username) == 0:
            print('用户名为空')
            return 0

        url = self.rest_base_url + '/users/' + self.username + '/contacts/users/' + username
        headers = dict({'Authorization': self.rest_token})
        headers.update(BASE_HEADERS)
        response = dx_request.httpRequest(url, headers, body, method)
        return response

    def add_user(self, username):
        response = self.optionContacts('POST', username, {'username':username})
        if response.code != 0:
            print('add user failed:%s' %(response.data))
        return response.code

    def delete_user(self, username):
        response = self.optionContacts('DELETE', username)
        if response.code != 0:
            print('delete user failed:%s' %(response.data))
        return response.code

    def add_user_to_black(self, username):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return 0

        if len(username) == 0:
            print('用户名为空')
            return 0

        url = self.rest_base_url + '/users/' + self.username + '/blocks/users'
        headers = dict({'Authorization': self.rest_token})
        headers.update(BASE_HEADERS)
        body = dict({'usernames': [username]})
        response = dx_request.post(url, headers, body)

        if response.code != 0:
            print('block user failed:%s' %(response.data))
        return response.code

    def remove_user_from_black(self, username):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return 0

        if len(username) == 0:
            print('用户名为空')
            return 0

        url = self.rest_base_url + '/users/' + self.username + '/blocks/users/' + username
        headers = dict({'Authorization': self.rest_token})
        headers.update(BASE_HEADERS)
        response = dx_request.delete(url, headers, None)

        if response.code != 0:
            print('unblock user failed:%s' %(response.data))
        return response.code


    def create_group(self, subject = '', describe = '', max_users = 300, members = None, is_public = True, is_approval = True):
        if len(self.admin_token) == 0:
            print('请先进行获取管理员token操作')
            return 0

        if len(self.token) == 0:
            print('请先进行获取token操作')
            return 0

        if len(subject) == 0:
            print('群主题为空')
            return 0

        url = self.rest_base_url + '/chatgroups'
        headers = dict({'Authorization': self.admin_rest_token})
        headers.update(BASE_HEADERS)

        body = {'groupname':subject,
                'desc':describe,
                'owner':self.username,
                'public':is_public,
                'approval':is_approval,
                'maxusers':max_users}
        if members != None and len(members):
            body.update({'members':members})

        response = dx_request.post(url, headers, body)

        if response.code != 0:
            print('create group failed:%s' %(response.data))
        return response.code

    def exit_group(self, group_id):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return None

        if len(group_id) == 0:
            print('群组ID为空')
            return None

        url = self.rest_base_url + '/chatgroups/' + group_id
        headers = dict({'Authorization': self.rest_token})
        headers.update(BASE_HEADERS)
        response = dx_request.delete(url, headers, None)

        if response.code != 0:
            print('delete group failed:%s' %(response.data))
        return response.code

    def get_current_user_groups(self):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return 0

        url = self.rest_base_url + '/users/' + self.username + '/joined_chatgroups'
        headers = dict({'Authorization': self.rest_token})
        headers.update(BASE_HEADERS)
        response = dx_request.get(url, headers, None)
        groups = response.data['data']

        if response.code != 0:
            print('get groups failed:%s' %(response.data))
        return groups

    def get_group_info(self, group_id):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return None

        if len(group_id) == 0:
            print('群组ID为空')
            return None

        url = self.rest_base_url + '/chatgroups/' + group_id
        headers = dict({'Authorization': self.rest_token})
        headers.update(BASE_HEADERS)
        response = dx_request.get(url, headers, None)

        if response.code != 0:
            print('get group info failed:%s' %(response.data))
        return response.data['data']

    def edit_group_info(self, group_id, subject = None, describe = None, max_users = -1):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return None

        if len(group_id) == 0:
            print('群组ID为空')
            return None

        if subject == None and describe == None and max_users == -1:
            return None

        url = self.rest_base_url + '/chatgroups/' + group_id
        headers = dict({'Authorization': self.rest_token})
        headers.update(BASE_HEADERS)

        body = {}
        if subject != None:
            body.update({'groupname':subject})
        if describe != None:
            body.update({'description':describe})
        if max_users > 0:
            body.update({'maxusers':max_users})

        response = dx_request.put(url, headers, body)

        if response.code != 0:
            print('edit group info failed:%s' %(response.data))
        return response.data['data']

    def get_group_members(self, group_id):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return None
        if len(group_id) == 0:
            print('群组ID为空')
            return None

        url = self.rest_base_url + '/chatgroups/' + group_id + '/users'
        headers = dict({'Authorization': self.rest_token})
        headers.update(BASE_HEADERS)
        response = dx_request.get(url, headers, None)

        if response.code != 0:
            print('get group members failed:%s' %(response.data))
        return response.data['data']

    def add_group_member(self, group_id, username):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return None
        if len(group_id) == 0 or len(username) == 0:
            print('参数为空')
            return None

        url = self.rest_base_url + '/chatgroups/' + group_id + '/users'
        headers = dict({'Authorization': self.rest_token})
        headers.update(BASE_HEADERS)

        body = dict({'usernames':[username]})
        response = dx_request.post(url, headers, body)

        if response.code != 0:
            print('add group member failed:%s' %(response.data))
        return response.data['data']

    def delete_group_member(self, group_id, username):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return None
        if len(group_id) == 0 or len(username) == 0:
            print('参数为空')
            return None

        url = self.rest_base_url + '/chatgroups/' + group_id + '/users/' + username
        headers = dict({'Authorization': self.rest_token})
        headers.update(BASE_HEADERS)
        response = dx_request.delete(url, headers, None)

        if response.code != 0:
            print('add group member failed:%s' %(response.data))
        return response.data['data']

    def get_group_blacks(self, group_id):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return None
        if len(group_id) == 0:
            print('群组ID为空')
            return None

        url = self.rest_base_url + '/chatgroups/' + group_id + '/blocks/users'
        headers = dict({'Authorization': self.rest_token})
        headers.update(BASE_HEADERS)
        response = dx_request.get(url, headers, None)

        if response.code != 0:
            print('get group blocks failed:%s' %(response.data))
        return response.data['data']

    def add_user_to_group_block(self, group_id, username):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return None
        if len(group_id) == 0 or len(username) == 0:
            print('参数为空')
            return None

        url = self.rest_base_url + '/chatgroups/' + group_id + '/blocks/users'
        headers = dict({'Authorization': self.rest_token})
        headers.update(BASE_HEADERS)

        body = dict({'usernames':[username]})
        response = dx_request.post(url, headers, body)

        if response.code != 0:
            print('add group block failed:%s' %(response.data))
        return response.data['data']

    def remove_user_from_group_block(self, group_id, username):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return None
        if len(group_id) == 0 or len(username) == 0:
            print('参数为空')
            return None

        url = self.rest_base_url + '/chatgroups/' + group_id + '/blocks/users/' + username
        headers = dict({'Authorization': self.rest_token})
        headers.update(BASE_HEADERS)
        response = dx_request.delete(url, headers, None)

        if response.code != 0:
            print('remove group block failed:%s' %(response.data))
        return response.data['data']


