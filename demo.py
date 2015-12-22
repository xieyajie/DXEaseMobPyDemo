#coding = 'utf-8'

__author__ = 'xieyajie'

import io
from easemob.em_client import *

DEFAULT_ID = 'YXA6TX5LoNxKEeOQ1eH_uqza9Q'
DEFAULT_SECRET = 'YXA6IGRmXvNxlDIy2QxeMzaimIE5IeI'
DEFAULT_APPKEY = 'easemob-demo#chatdemoui'
DEFAULT_REST = 'https://a1.easemob.com'

class Demo:

    def taskOptions(self, op):
        if op == 1:
            username = input('username:')
            password = input('password:')
            self.client_.create_new_user(username, password)
        elif op == 2:
            username = input('username:')
            password = input('password:')
            self.client_.get_user_token(username, password)
        elif op == 3:
            id = input('client_id:')
            if len(id) == 0:
                id = DEFAULT_ID

            secret = input('client_secret:')
            if len(secret) == 0:
                secret = DEFAULT_SECRET

            self.client_.get_admin_token(id, secret)
        elif op == 4:
            self.client_.get_contacts()
        elif op == 5:
            self.client_.get_black_contacts()
        elif op == 6:
            username = input('username:')
            self.client_.add_user(username)
        elif op == 7:
            username = input('username:')
            self.client_.delete_user(username)
        elif op == 8:
            username = input('username:')
            self.client_.add_user_to_black(username)
        elif op == 9:
            username = input('username:')
            self.client_.remove_user_from_black(username)
        elif op == 10:
            self.client_.get_current_user_groups()
        elif op == 11:
            subject = input('群主题:')
            des = input('群描述:')

            max_users = 300
            tmp = input('最大群人数(默认300):')
            if len(tmp):
                max_users = int(tmp)

            members = input('群成员:')

            is_public = True
            tmp = input('是否是公开群(1是,0否):')
            if len(tmp):
                is_public = bool(tmp)

            is_approval = True
            if is_public == 1:
                tmp = input('进群是否需要群主同意(1是,0否):')
                if len(tmp):
                    is_approval = bool(tmp)


            self.client_.create_group(subject, des, max_users, members, is_public, is_approval)
        elif op == 12:
            group_id = input('要退出的群组ID:')
            self.client_.exit_group(group_id)
        elif op == 13:
            group_id = input('群组ID:')

            subject = input('群主题:')
            if len(subject) == 0:
                subject = None

            des = input('群描述:')
            if len(des) == 0:
                des = None

            max_users = -1
            tmp = input('最大群人数(默认不修改):')
            if len(tmp):
                max_users = int(tmp)

            self.client_.edit_group_info(group_id, subject, des, max_users)
        elif op == 14:
            group_id = input('群组ID:')
            self.client_.get_group_members(group_id)
        elif op == 15:
            group_id = input('群组ID:')
            username = input('要添加成员username:')
            self.client_.add_group_member(group_id, username)
        elif op == 16:
            group_id = input('群组ID:')
            username = input('要删除成员username:')
            self.client_.delete_group_member(group_id, username)
        elif op == 17:
            group_id = input('群组ID:')
            self.client_.get_group_blacks(group_id)
        elif op == 18:
            group_id = input('群组ID:')
            username = input('要加入群组黑名单的username:')
            self.client_.add_user_to_group_block(group_id, username)
        elif op == 19:
            group_id = input('群组ID:')
            username = input('要移出群组黑名单的username:')
            self.client_.remove_user_from_group_block(group_id, username)
        # elif op == 20:
        # elif op == 21:
        # elif op == 22:
        # elif op == 23:



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

        self.client_ = PyClient(appkey, rest + '/' + appkey.replace('#', '/', 1))

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
                       '退出群组(owner退出群组销毁)',
                       '获取群组详情',
                       '修改群组详情',
                       '获取群成员',
                       '添加群成员',
                       '删除群成员(必须是owner)',
                       '获取群组黑名单',
                       '将用户加入群组黑名单',
                       '将用户移出群组黑名单',
                       '上传语音图片',
                       '下载语音图片'
                       '发送单聊消息',
                       '发送群聊消息',]
            op = self.showOptions(options)

            self.taskOptions(op)

        print('main end')


if __name__ == '__main__':
    demo = Demo()
    demo.main()