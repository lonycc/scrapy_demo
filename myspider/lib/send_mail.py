# coding=utf-8

import smtplib
from email.mime.text import MIMEText

class mailSender(object):
    def __init__(self):
        self.server = 'smtp.domain.com'
        self.username = '发信人名称'
        self.password = 'password'
        self.port = 25
        self.sender = 'admin@domain.com'

    def send(self, toList, subject, body):
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['From'] = self.sender
        msg['To'] = ','.join(toList)
        msg['Subject'] = subject
        try:
            smtp_client = smtplib.SMTP()
            smtp_client.connect(self.server, self.port)
            rs = smtp_client.login(self.username, self.password)
            #print(f'登录结果, {rs}')
            print('登录结果', rs)
            if rs and rs[0] == 235:
                print('登录成功')
                smtp_client.sendmail(self.sender, toList, msg.as_string())
            else:
                #print(f'登录失败, code={rs[0]}')
                print('登录失败, code=', rs[0])
            smtp_client.close()
        except Exception as e:
            #print(f'发送邮件失败, {e}')
            print('发送邮件失败', e)

if __name__ == '__main__':
    mailsender = mailSender()
    mailsender.send(['receiver@domain.com'], 'scrapy测试邮件', 'only for test scrapy')