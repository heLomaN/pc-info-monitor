# homepc info monitor

-----------------

### 功能介绍

- 获取当前设备的公网IP，并发往指定邮箱，可以解决需要远程设备IP（如内网穿透），但是公网IP会不停变化的场景
- 参考`report-local-info.py`，编写一个脚本，每天定时运行即可


### 如何使用

- 在`iolibs/mailconfig.py`中填写发送邮件的邮箱、密码、接收邮箱

 * 注意smtp/pop协议的邮箱默认为yeah.net，如果使用163邮箱、qq邮箱，需要做相应的修改
 