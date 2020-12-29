# NewCumtLogin
中国矿业大学融合门户登录。
-
URL：http://authserver.cumt.edu.cn/authserver/login?service=http%3A//portal.cumt.edu.cn/casservice 

本项目实现了新版统一登录认证页面的登录和一系列操作  
具体有:  
 + 登录操作
 + 简单查询校园卡余额
 + 简单查询图书借阅信息
 + 简单查询校园卡流水
 + 按照时间查询校园卡流水
 + 校园卡充值
 + 图书馆jwt获取
 + 图书馆当前借阅信息
 + 图书馆历史借阅信息
 + 图书馆收藏信息
 <h4>请在内网环境下使用</h4>
 把学号和密码换成自己的  
 
 使用方法：
 
           pip install bs4
           pip install pyexecjs -i https://pypi.tuna.tsinghua.edu.cn/simple
           python login.py
 
 目前只是能用,如果你想更好的使用，请不要使用request.session,并将class拆分，cookie可以用redis存一下(请注意过期时间，以及如何验证过期)。json数据还是处理一下比较好

 如果只是想简单的使用，请看着整(最基础的爬虫，就是加密部分有一点麻烦)
 
 网站更新的话,这边也会陆续更新的
 
 本项目在不久的将来会集成的矿小助里面
 
 <h4>什么？你还不知道矿小助？</h4>
 
 
 请访问https://www.lvyingzhao.cn 或者我们的正式网站 https://kxz.atcumt.com/
 
 后续做一下验证码自动识别(如果有空的话)
 
 关于爬虫的一部分的介绍和AES加密的部分，有时间会更新在博客 https://boopo.github.io (应该会有的)
 
 如果你有更好的实现，请直接 pull request
 
 
