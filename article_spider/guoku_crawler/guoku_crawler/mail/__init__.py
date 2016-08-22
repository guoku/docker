# -*- coding: utf-8 -*-
#导入smtplib和MIMEText
import smtplib
from guoku_crawler.config import logger
from email.mime.text import MIMEText

def send_mail(to_list,sub,content):
    #设置服务器，用户名、口令以及邮箱的后缀
    mail_host="smtp.exmail.qq.com"
    mail_user="jslong@guoku.com"
    mail_pass="Ab123456"
    mail_postfix="guoku.com"
    me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content)
    msg['Subject'] = sub
    msg['From'] = mail_user
    msg['To'] = to_list
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        logger.info('send mail to %s ' %to_list)
        return True
    except Exception as e:
        logger.info('error sending mail , exception %s'%e)

        return False


masters = 'jslong@guoku.com'
def send_mail_to_masters(sub, content):
    return send_mail(masters, sub, content)



if __name__ == '__main__':
    send_mail('anchen@guoku.com,tayak@sina.com','test python mail','test content')
