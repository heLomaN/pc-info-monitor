class MailConfig:
    from_addr = "mysendermail@yeah.net"
    password = "mysenderpasswd"
    to_addr = "mynotifier@qq.com"
    smtp_server = "smtp.yeah.net"
    pop3_server = "pop.yeah.net"

import importlib
spam_spec = importlib.util.find_spec("iolibs.passwd")
if spam_spec:
    from iolibs.passwd import MailConfig