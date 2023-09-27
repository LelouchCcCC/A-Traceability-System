import smtplib
from email.mime.text import MIMEText


class SendEmail(object):
    def sending(self, receiver, content):
        mail_host = 'smtp.qq.com'
        mail_pass = 'cbdykauznackbcib'
        mail_user = '605286079@qq.com'
        sender = '605286079@qq.com'
        receivers = [receiver]
        message = MIMEText(content, 'plain', 'utf-8')
        message['Subject'] = '致谢'
        message['From'] = sender
        message['To'] = receivers[0]
        try:
            smtpObj = smtplib.SMTP()
            # 连接到服务器
            smtpObj.connect(mail_host, 25)
            # 登录到服务器
            smtpObj.login(mail_user, mail_pass)
            # 发送
            smtpObj.sendmail(
                sender, receivers, message.as_string())
            # 退出
            smtpObj.quit()
            return {'status': 'success'}
        except smtplib.SMTPException as e:
            return {'status': 'error'}
