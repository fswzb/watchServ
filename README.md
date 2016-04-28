#watchServ
This is for watching server or something else.
By configuring cmds.py, you can achieve:
1.run the cmd you added at intervals you added
2.if the cmd return non-zero or output something in stderr, we think it's failed;
  you can configure if it's failed when there is anything in stdout;
  then, if you added fixCmd, it will be executed;
  all output of cmd will be send to the email you added
3.as you can see, you need add: strEmailAddress, intTimeInterval, cmd, intDealStdout, strFixCmd
4.if you modified cmds.py or config.py, watching will be restart

Modify mailUser and mailPasswd in config.py then you can run python watchDaemon.py.
that's all

Chinese/中文：
用于监测某个服务。通过配置 cmds.py 文件，添加如下几项：
strEmailAddress, intTimeInterval, cmd, intDealStdout, strFixCmd
可以实现如下效果:
	如果 config.py/cmds.py 有更新，最迟10s会自动重新加载此文件
    每隔 intTimeInterval 秒执行一次 cmd
    如果命令返回值不为0或者标准输出（intDealStdout=0则忽略）、错误输出中有任何输出，
		则把当前时间、返回值、标准输出及错误输出通过邮件发送给指定监视者；
    如果有修复命令，则执行并把修复命令的标准输出和错误输出添加到邮件内容中
	发送邮件到指定地址
	
运行前请先配置 config.py 文件中的 mailUser 和 mailPasswd，然后运行命令 python watchDaemon.py
	