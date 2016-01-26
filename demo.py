# coding = utf-8

from easemob.emclient import *

DEFAULT_CLIENT_ID = ''
DEFAULT_CLIENT_SECRET = ''
DEFAULT_APPKEY = ''
DEFAULT_REST = ''

class Demo:

    def __init__(self):
        self.client = None

    def task_options(self, op):
        if op == 1:
            client_id = input('client_id:')
            if len(client_id) == 0:
                client_id = DEFAULT_CLIENT_ID

            secret = input('client_secret:')
            if len(secret) == 0:
                secret = DEFAULT_CLIENT_SECRET

            self.client.get_admin_token(client_id, secret)
        elif op == 2:
            username = input('username:')
            self.client.delete_user(username)
        elif op == 3:
            username = input('username:')
            self.client.make_user_offline(username)
        elif op == 4:
            username = input('username:')
            password = input('password:')
            self.client.create_new_user(username, password)
        elif op == 5:
            username = input('username:')
            password = input('password:')
            self.client.get_user_token(username, password)
        elif op == 6:
            self.client.get_contacts()
        elif op == 7:
            self.client.get_black_contacts()
        elif op == 8:
            username = input('username:')
            self.client.add_user(username)
        elif op == 9:
            username = input('username:')
            self.client.delete_contact(username)
        elif op == 10:
            username = input('username:')
            self.client.add_user_to_black(username)
        elif op == 11:
            username = input('username:')
            self.client.remove_user_from_black(username)
        elif op == 12:
            self.client.get_current_user_groups()
        elif op == 13:
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

            self.client.create_group(subject, des, max_users,
                                     members, is_public, is_approval)
        elif op == 14:
            group_id = input('要退出的群组ID:')
            self.client.exit_group(group_id)
        elif op == 15:
            group_id = input('要查询的群组ID:')
            self.client.get_group_info(group_id)
        elif op == 16:
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

            self.client.edit_group_info(group_id, subject, des, max_users)
        elif op == 17:
            group_id = input('群组ID:')
            self.client.get_group_members(group_id)
        elif op == 18:
            group_id = input('群组ID:')
            username = input('要添加成员username:')
            self.client.add_group_member(group_id, username)
        elif op == 19:
            group_id = input('群组ID:')
            username = input('要删除成员username:')
            self.client.delete_group_member(group_id, username)
        elif op == 20:
            group_id = input('群组ID:')
            self.client.get_group_blacks(group_id)
        elif op == 21:
            group_id = input('群组ID:')
            username = input('要加入群组黑名单的username:')
            self.client.add_user_to_group_block(group_id, username)
        elif op == 22:
            group_id = input('群组ID:')
            username = input('要移出群组黑名单的username:')
            self.client.remove_user_from_group_block(group_id, username)
        elif op == 23:
            to = input('接收者: ')
            content = input('显示内容: ')
            self.client.send_message_apns(to, content)
        elif op == 24:
            reciver = input('接收者:')
            text = input('文字:')
            mtype = input('单聊->0, 群聊->1, 聊天室->2:')
#             ext = input('扩展({\'key\': \'value\', \'key\': \'value\'}):')
            self.client.send_text_message(reciver, text, int(mtype))
        elif op == 25:
            image_path = input('图片路径:')
            self.client.upload_image(image_path)
        # elif op == 26:

    def show_options(self, options):
        print('\n%s' % ('=' * 40))
        print('输入编号,-1返回上一级\n')
        for i in range(0, len(options)):
            print(str.format('  {0}', options[i]))
        print('\n%s' % ('=' * 40))

        op = int(input())
        if op <= len(options):
            return op

        return self.show_options(options)

    def init_client(self):
        print('\n初始化client\n')

        appkey = input('appkey(%s):' % DEFAULT_APPKEY)
        if len(appkey) == 0:
            appkey = DEFAULT_APPKEY

        rest = input('rest(%s):' % DEFAULT_REST)
        if len(rest) == 0:
            rest = DEFAULT_REST

        client_id = input('client_id:')
        if len(client_id) == 0:
            client_id = DEFAULT_CLIENT_ID

        client_secret = input('client_secret:')
        if len(client_secret) == 0:
            client_secret = DEFAULT_CLIENT_SECRET

        self.client = PyClient(appkey, rest, client_id, client_secret)

    def main(self):
        print('\n这里是环信python demo\n')

        self.init_client()

        options = ['1. 获取管理员权限(标注管理员的都必须先进行1)',
                   '2. 删除用户(管理员)',
                   '3. 强制用户下线(管理员)',
                   '4. 创建新用户',
                   '5. 获取用户token(没标注管理员的操作必须先进行5)',
                   '6. 获取好友列表',
                   '7. 获取好友黑名单列表',
                   '8. 添加好友',
                   '9. 删除好友',
                   '10. 将用户加入黑名单',
                   '11. 将用户移出黑名单',
                   '12. 获取当前用户的所有群组',
                   '13. 创建群组',
                   '14. 退出群组(owner退出群组销毁)',
                   '15. 获取群组详情',
                   '16. 修改群组详情',
                   '17. 获取群成员',
                   '18. 添加群成员',
                   '19. 删除群成员(必须是owner)',
                   '20. 获取群组黑名单',
                   '21. 将用户加入群组黑名单',
                   '22. 将用户移出群组黑名单',
                   '23. 推送消息Apns(管理员)',
                   '24. 发送文字消息(管理员)',
                   '25. 上传图片',
                   '26. 下载图片']

        op = 1
        while op:
            op = self.show_options(options)
            self.task_options(op)

        print('main end')


if __name__ == '__main__':
    demo = Demo()
    demo.main()
