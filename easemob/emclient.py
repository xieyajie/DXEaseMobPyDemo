# coding = 'utf-8'

from utils import dxrequest

BASE_HEADERS = {'Content-Type': 'application/json',
                'Accept': 'application/json'}


class PyClient(object):

    def __init__(self, app_key, rest_base_url,
                 client_id, client_secret):
        self.app_key = app_key
        self.client_id = client_id
        self.client_secret = client_secret

        if rest_base_url.endswith('/'):
            rest_base_url = rest_base_url[:(len(rest_base_url) - 1)]
        self.rest_base_url = rest_base_url + '/' + app_key.replace('#', '/', 1)

        self.admin_token = ''
        self.username = ''
        self.password = ''
        self.token = ''
        self.rest_token = ''
        self.admin_rest_token = ''

        if len(self.client_id) and len(self.client_secret):
            self.get_admin_token(client_id, client_secret)

    def get_admin_token(self, client_id, client_secret):
        if len(client_id) == 0 or len(client_secret) == 0:
            print('client_id or client_secret is empty')
            return ''

        url = "https://a1.easemob.com/"+ self.app_key.replace('#', '/', 1) + '/token'
        body = {'grant_type': 'client_credentials',
                'client_id': client_id,
                'client_secret': client_secret}
        response = dxrequest.post(url, BASE_HEADERS, body)
        if response.code == 0:
            self.client_id = client_id
            self.client_secret = client_secret
            self.admin_token = response.data['access_token']
            self.admin_rest_token = 'Bearer ' + self.admin_token
            print(self.admin_token)

            return self.admin_token

        return ''

    def delete_user(self, username):
        if len(self.admin_token) == 0 or len(self.username) == 0:
            return -1

        url = self.rest_base_url + '/users/' + username
        headers = {'Authorization': self.admin_rest_token}
        headers.update(BASE_HEADERS)
        response = dxrequest.delete(url, BASE_HEADERS, None)

        return response.code

    def make_user_offline(self, username):
        if len(self.admin_token) == 0 or len(self.username) == 0:
            return -1

        url = self.rest_base_url + '/users/' + username + '/disconnect'
        headers = {'Authorization': self.admin_rest_token}
        headers.update(BASE_HEADERS)
        response = dxrequest.delete(url, BASE_HEADERS, None)

        return response.code

    def create_new_user(self, username, password):
        if len(username) == 0 or len(password) == 0:
            return None

        url = self.rest_base_url + '/users'
        body = {'username': username, 'password': password}
        response = dxrequest.put(url, BASE_HEADERS, body)

        return response

    def get_user_token(self, username, password):
        if len(username) == 0 or len(password) == 0:
            return ''

        url = self.rest_base_url + '/token'
        body = {'grant_type': 'password', 'username': username, 'password': password}
        response = dxrequest.post(url, BASE_HEADERS, body)
        if response.code == 0:
            self.username = username
            self.password = password
            self.token = response.data['access_token']
            self.rest_token = 'Bearer ' + self.token
            return self.token

        return ''

    def get_contacts(self):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return None

        url = self.rest_base_url + '/users/' + self.username + '/contacts/users'
        headers = {'Authorization': self.rest_token}
        headers.update(BASE_HEADERS)
        response = dxrequest.get(url, headers, None)
        if response.code == 0:
            contacts = response.data['data']
            return contacts

        return None

    def get_black_contacts(self):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return None

        url = self.rest_base_url + '/users/' + self.username + '/blocks/users'
        headers = {'Authorization': self.rest_token}
        headers.update(BASE_HEADERS)
        response = dxrequest.get(url, headers, None)
        if response.code == 0:
            blacks = response.data['data']
            return blacks

        return None

    def __option_contacts(self, method, username, body=None):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return None

        if len(username) == 0:
            print('用户名为空')
            return None

        url = self.rest_base_url + '/users/' + self.username + '/contacts/users/' + username
        headers = {'Authorization': self.rest_token}
        headers.update(BASE_HEADERS)
        response = dxrequest.http_request(url, headers, body, method)
        return response

    def add_user(self, username):
        response = self.__option_contacts('POST', username, {'username': username})
        return response.code

    def delete_contact(self, username):
        response = self.__option_contacts('DELETE', username)
        return response.code

    def add_user_to_black(self, username):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return 0

        if len(username) == 0:
            print('用户名为空')
            return 0

        url = self.rest_base_url + '/users/' + self.username + '/blocks/users'
        headers = {'Authorization': self.rest_token}
        headers.update(BASE_HEADERS)
        body = {'usernames': [username]}
        response = dxrequest.post(url, headers, body)
        return response.code

    def remove_user_from_black(self, username):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return 0

        if len(username) == 0:
            print('用户名为空')
            return 0

        url = self.rest_base_url + '/users/' + self.username + '/blocks/users/' + username
        headers = {'Authorization': self.rest_token}
        headers.update(BASE_HEADERS)
        response = dxrequest.delete(url, headers, None)
        return response.code

    def create_group(self, subject='', describe='', max_users=300,
                     members=None, is_public=True, is_approval=True):
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
        headers = {'Authorization': self.admin_rest_token}
        headers.update(BASE_HEADERS)

        body = {'groupname': subject,
                'desc': describe,
                'owner': self.username,
                'public': is_public,
                'approval': is_approval,
                'maxusers': max_users}
        if members is not None and len(members):
            body.update({'members': members})

        response = dxrequest.post(url, headers, body)
        return response.code

    def exit_group(self, group_id):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return None

        if len(group_id) == 0:
            print('群组ID为空')
            return None

        url = self.rest_base_url + '/chatgroups/' + group_id
        headers = {'Authorization': self.rest_token}
        headers.update(BASE_HEADERS)
        response = dxrequest.delete(url, headers, None)
        return response.code

    def get_current_user_groups(self):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return 0

        url = self.rest_base_url + '/users/' + self.username + '/joined_chatgroups'
        headers = {'Authorization': self.rest_token}
        headers.update(BASE_HEADERS)
        response = dxrequest.get(url, headers, None)
        groups = response.data['data']
        return groups

    def get_group_info(self, group_id):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return None

        if len(group_id) == 0:
            print('群组ID为空')
            return None

        url = self.rest_base_url + '/chatgroups/' + group_id
        headers = {'Authorization': self.rest_token}
        headers.update(BASE_HEADERS)
        response = dxrequest.get(url, headers, None)
        return response.data['data']

    def edit_group_info(self, group_id, subject=None,
                        describe=None, max_users=-1):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return None

        if len(group_id) == 0:
            print('群组ID为空')
            return None

        if subject is None and describe is None and max_users == -1:
            return None

        url = self.rest_base_url + '/chatgroups/' + group_id
        headers = {'Authorization': self.rest_token}
        headers.update(BASE_HEADERS)

        body = {}
        if subject is not None:
            body.update({'groupname': subject})
        if describe is not None:
            body.update({'description': describe})
        if max_users > 0:
            body.update({'maxusers': max_users})

        response = dxrequest.put(url, headers, body)
        return response.data['data']

    def get_group_members(self, group_id):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return None
        if len(group_id) == 0:
            print('群组ID为空')
            return None

        url = self.rest_base_url + '/chatgroups/' + group_id + '/users'
        headers = {'Authorization': self.rest_token}
        headers.update(BASE_HEADERS)
        response = dxrequest.get(url, headers, None)
        return response.data['data']

    def add_group_member(self, group_id, username):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return None
        if len(group_id) == 0 or len(username) == 0:
            print('参数为空')
            return None

        url = self.rest_base_url + '/chatgroups/' + group_id + '/users'
        headers = {'Authorization': self.rest_token}
        headers.update(BASE_HEADERS)

        body = {'usernames': [username]}
        response = dxrequest.post(url, headers, body)
        return response.data['data']

    def delete_group_member(self, group_id, username):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return None
        if len(group_id) == 0 or len(username) == 0:
            print('参数为空')
            return None

        url = self.rest_base_url + '/chatgroups/' + group_id + '/users/' + username
        headers = {'Authorization': self.rest_token}
        headers.update(BASE_HEADERS)
        response = dxrequest.delete(url, headers, None)
        return response.data['data']

    def get_group_blacks(self, group_id):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return None
        if len(group_id) == 0:
            print('群组ID为空')
            return None

        url = self.rest_base_url + '/chatgroups/' + group_id + '/blocks/users'
        headers = {'Authorization': self.rest_token}
        headers.update(BASE_HEADERS)
        response = dxrequest.get(url, headers, None)
        return response.data['data']

    def add_user_to_group_block(self, group_id, username):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return None
        if len(group_id) == 0 or len(username) == 0:
            print('参数为空')
            return None

        url = self.rest_base_url + '/chatgroups/' + group_id + '/blocks/users'
        headers = {'Authorization': self.rest_token}
        headers.update(BASE_HEADERS)

        body = {'usernames': [username]}
        response = dxrequest.post(url, headers, body)
        return response.data['data']

    def remove_user_from_group_block(self, group_id, username):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return -1
        if len(group_id) == 0 or len(username) == 0:
            print('参数为空')
            return -1

        url = self.rest_base_url + '/chatgroups/' + group_id + '/blocks/users/' + username
        headers = {'Authorization': self.rest_token}
        headers.update(BASE_HEADERS)
        response = dxrequest.delete(url, headers, None)
        return response.code

    def send_message_apns(self, to, content='推送内容'):
        if len(self.token) == 0:
            print('请先进行获取token操作')
            return -1
        if len(to) == 0:
            print('参数为空')
            return -1

        url = self.rest_base_url + '/notifications'
        headers = {'Authorization': self.admin_rest_token}
        headers.update(BASE_HEADERS)

        body = {'chat_type': 'chat', 'to': to, 'alert': content}
        response = dxrequest.post(url, headers, body)
        print(response.data)

        return response.code

    def send_text_message(self, to, content, mtype):
        target_type = "users"
        if mtype == 1:
            target_type = "chatgroups"
        elif mtype == 2:
            target_type = "chatrooms"

        target = [to]
        msg = {'type': 'txt', 'msg': content}
        ext = {}

        url = self.rest_base_url + '/messages'
        headers = {'Authorization': self.admin_rest_token}
        headers.update(BASE_HEADERS)

        body = {'target_type': target_type,
                'target': target,
                'from': self.username,
                'msg': msg,
                'ext': ext}
        response = dxrequest.post(url, headers, body)
        print(response.data)

        return response.code

    def upload_image(self, image_path):
        url = self.rest_base_url + '/chatfiles'

        headers = {'Authorization': self.admin_rest_token, 'restrict-access': True}
        dxrequest.upload_file(url, image_path, headers)


