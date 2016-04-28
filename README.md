#watchServ
This is for watching server or something else.
By configuring cmds.py, you can achieve:
1.run the cmd you added at intervals you added
2.if the cmd return non-zero or output something in stderr, we think it's failed;
  you can configure if it's failed when there is anything in stdout;
  then, if you added fixCmd, it will be executed;
  all output of cmd will be send to the email you added
3.as you can see, you need add: strEmail, intTimeInterval, cmd, intDealStdout, strFixCmd

that's all