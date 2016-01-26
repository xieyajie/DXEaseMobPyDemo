# DXEaseMobPyDemo
Python 封装 环信rest接口

提供功能如下：
  1. 获取管理员权限(标注管理员的都必须先进行1)
  2. 删除用户(管理员)
  3. 强制用户下线(管理员)
  4. 创建新用户
  5. 获取用户token(没标注管理员的操作必须先进行5)
  6. 获取好友列表
  7. 获取好友黑名单列表
  8. 添加好友
  9. 删除好友
  10. 将用户加入黑名单
  11. 将用户移出黑名单
  12. 获取当前用户的所有群组
  13. 创建群组
  14. 退出群组(owner退出群组销毁)
  15. 获取群组详情
  16. 修改群组详情
  17. 获取群成员
  18. 添加群成员
  19. 删除群成员(必须是owner)
  20. 获取群组黑名单
  21. 将用户加入群组黑名单
  22. 将用户移出群组黑名单
  23. 推送消息Apns(管理员)
  24. 发送文字消息(管理员)
  25. 上传图片
  26. 下载图片

# 使用说明

###替换demo.py中的4个宏定义

DEFAULT_CLIENT_ID: app的client_id

DEFAULT_CLIENT_SECRET: app的client_secret

DEFAULT_APPKEY: appkey

DEFAULT_REST: rest地址

### 运行
命令行输入 

	$python3 demo.py

