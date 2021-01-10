from iolibs.infotool import get_public_ip
from iolibs.mailtool import get_latest_mail, send_mail_to_qq



if __name__ == "__main__":
    send_mail_to_qq("report new ip", get_public_ip())

    mail_text = get_latest_mail()
    print("get mail:\n", mail_text.content)

    print("complete")