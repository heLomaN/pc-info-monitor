import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

from  iolibs.mailconfig import MailConfig


def send_mail_to_qq(title, body):
    from email import encoders
    from email.header import Header
    from email.mime.text import MIMEText
    from email.utils import parseaddr, formataddr

    import smtplib


    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    msg = MIMEText('{}'.format(body), 'plain', 'utf-8')
    msg['From'] = _format_addr('home-moniter <%s>' % MailConfig.from_addr)
    msg['To'] = _format_addr('root <%s>' % MailConfig.to_addr)
    msg['Subject'] = Header('Home PC Info : {}'.format(title), 'utf-8').encode()

    server = smtplib.SMTP(MailConfig.smtp_server, 25)
    # server.set_debuglevel(1)
    server.login(MailConfig.from_addr, MailConfig.password)
    server.sendmail(MailConfig.from_addr, [MailConfig.to_addr], msg.as_string())
    server.quit()


# 邮件的Subject或者Email中包含的名字都是经过编码后的str,要正常显示
# 就必须decode
def decode_str(s):
    # 在不转换字符集的情况下解码消息头值,返回一个list
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


# 文本邮件的内容也是str,还需要检测编码，
# 否则，非UTF-8编码的邮件都无法正常显示：

def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        # lower:所有大写字符为小写
        content_type = msg.get('Content-Type', '').lower()
        # find:检测字符串中是否包含子字符串
        # 返回charset=头字符的位置
        pos = content_type.find('charset=')
        if pos >= 0:
            # strip:移除字符串头尾指定的字符(默认为空格)
            charset = content_type[pos + 8:].strip()
    # print('charset::%s' % charset)
    return charset


# indent用于缩进显示：
"""
only get first part if multi part
"""

class EmailStruct:
    def __init__(self):
        self.sender = ""
        self.receiver = ""
        self.subject = ""
        self.content = ""

def email_to_plain_text(msg, indent=0):
    email_content = EmailStruct()
    # 初始分析
    if indent == 0:
        # 遍历获取 发件人，收件人，主题
        for header in ['From', 'To', 'Subject']:
            # 获得对应的内容
            value = msg.get(header, '')
            # 有内容
            if value:
                # 如果是主题
                if header == 'Subject':
                    # 解码主题
                    value = decode_str(value)
                    email_content.subject = value
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    if header == 'From':
                        email_content.sender = value
                    elif header == 'To':
                        email_content.receiver = value

    if msg.is_multipart():
        parts = msg.get_payload()
        email_content.content += email_to_plain_text(parts[0], indent + 1).content
    else:
        content_type = msg.get_content_type()
        if content_type == 'text/plain' or content_type == 'text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            email_content.content += "{}{}".format(' ' * indent, content + '')

    return email_content


def get_latest_mail():
    # 连接到POP3服务器:
    server = poplib.POP3(MailConfig.pop3_server)
    # 可以打开或关闭调试信息:
    # server.set_debuglevel(1)
    # 可选:打印POP3服务器的欢迎文字:
    print(server.getwelcome().decode('utf-8'))

    # 身份认证:
    server.user(MailConfig.from_addr)
    server.pass_(MailConfig.password)

    # stat()返回邮件数量和占用空间:
    print('get_latest_mail: Messages: %s. Size: %s' % server.stat())
    # list()返回所有邮件的编号:
    resp, mails, octets = server.list()
    # 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
    print("get_latest_mail", mails)

    # 获取最新一封邮件, 注意索引号从1开始:
    index = len(mails)
    resp, lines, octets = server.retr(index)

    # lines存储了邮件的原始文本的每一行,
    # 可以获得整个邮件的原始文本:
    msg_content = b'\r\n'.join(lines).decode('utf-8')
    # 稍后解析出邮件:
    msg = Parser().parsestr(msg_content)

    server.quit()

    return email_to_plain_text(msg)