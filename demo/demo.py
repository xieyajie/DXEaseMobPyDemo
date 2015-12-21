#coding = 'utf-8'

__author__ = 'xieyajie'

import io
from easemob.EMPyClient import *

DEFAULT_ID = 'YXA6TX5LoNxKEeOQ1eH_uqza9Q'
DEFAULT_SECRET = 'YXA6IGRmXvNxlDIy2QxeMzaimIE5IeI'
DEFAULT_APPKEY = 'easemob-demo#chatdemoui'
DEFAULT_REST = 'https://a1.easemob.com'

class Demo:

    def taskOptions(self, op):
        if op == 1:
            username = input('username:')
            password = input('password:')
            self.client_.createNewUser(username, password)
        elif op == 2:
            username = input('username:')
            password = input('password:')
            self.client_.getUserToken(username, password)
        elif op == 3:
            id = input('client_id:')
            if len(id) == 0:
                id = DEFAULT_ID

            secret = input('client_secret:')
            if len(secret) == 0:
                secret = DEFAULT_SECRET

            self.client_.getAdminToken(id, secret)
        elif op == 4:
            self.client_.getContacts()
        elif op == 5:
            self.client_.getBlackContacts()
        elif op == 6:
            username = input('username:')
            self.client_.addUser(username)
        elif op == 7:
            username = input('username:')
            self.client_.deleteUser(username)
        elif op == 8:
            username = input('username:')
            self.client_.addUserToBlack(username)
        elif op == 9:
            username = input('username:')
            self.client_.removeUserFromBlack(username)
        elif op == 10:
            self.client_.getCurrentUserGroups()
        elif op == 11:
            subject = input('群主题:')
            des = input('群描述:')

            maxUsers = 300
            tmp = input('最大群人数(默认300):')
            if len(tmp):
                maxUsers = int(tmp)

            members = input('群成员:')

            isPublic = True
            tmp = input('是否是公开群(1是,0否):')
            if len(tmp):
                isPublic = bool(tmp)

            isApproval = True
            if isPublic == 1:
                tmp = input('进群是否需要群主同意(1是,0否):')
                if len(tmp):
                    isApproval = bool(tmp)


            self.client_.createGroup(subject, des, maxUsers, members, isPublic, isApproval)
        elif op == 12:
            groupId = input('要退出的群组ID:')
            self.client_.exitGroup(groupId)
        # elif op == 13:
        # elif op == 14:
        # elif op == 15:
        # elif op == 16:




    def showOptions(self, options):
        print('\n%s' %('=' * 40))
        print('输入编号,-1退出\n')
        for i in range(0, len(options)):
            print(str.format('  {0}：{1}', i + 1, options[i]))
        print('\n%s' %('=' * 40))

        try:
            op = int(input())
            if op <= len(options):
                return op
        except:
            pass

        return self.showOptions(options)

    def main(self):
        print('\n这里是环信python demo\n')

        appkey = input('appkey(%s):' %(DEFAULT_APPKEY))
        if len(appkey) == 0:
            appkey = DEFAULT_APPKEY

        rest = input('rest(%s):' %(DEFAULT_REST))
        if len(rest) == 0:
            rest = DEFAULT_REST
        if rest.endswith('/'):
            rest = rest[:(len(rest) - 1)]

        self.client_ = EMPyClient(appkey, rest + '/' + appkey.replace('#', '/', 1))

        op = 1
        while op:
            options = ['创建新用户',
                       '获取用户token',
                       '获取管理员token',
                       '获取好友',
                       '获取好友黑名单',
                       '添加好友',
                       '删除好友',
                       '将用户加入黑名单',
                       '将用户移出黑名单',
                       '获取当前用户的所有群组',
                       '创建群组',
                       '退出群组(owner退出群组销毁)'
                       '获取群组详情',
                       '修改群组详情',
                       '添加群成员',
                       '删除群成员(必须是owner)'
                       '发送单聊消息',
                       '发送群聊消息',]
            op = self.showOptions(options)

            self.taskOptions(op)

        print('main end')


if __name__ == '__main__':
    demo = Demo()
    demo.main()