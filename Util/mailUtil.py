import imaplib
import email
import datetime
import base64
import time


class MailClient():

    def __init__(self, user, password):
        # 建立连接，登录账号
        self.connect = imaplib.IMAP4_SSL(port='993', host='mail.galasports.net')
        self.connect.login(user, password)

    def find_my_mail(self, send, toal_title):
        d1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return self.re_connect_server1(d1, send, toal_title)

    def select_mail1(self, d1, send, toal_title, range=100):
        # 选择文件夹获取邮件总数
        self.connect.select()
        type, data = self.connect.search(None, 'ALL')
        self.datelist = data[0].split()
        toal_list = []
        # 把目标时间转成datetime类型
        try:
            toal_time1 = datetime.datetime.strptime(d1, '%Y-%m-%d %H:%M:%S')
        except:
            raise Exception("时间格式有误，请保证格式为：xxxx-xx-xx ")
        for count in self.datelist[::-1][:range]:
            count1 = int(count.decode()) - 1
            type1, data = self.connect.fetch(self.datelist[count1], '(RFC822)')
            # 拿到邮件内容
            msg = email.message_from_string(data[0][1].decode('utf-8'))
            # 拿到邮件创建时间并转型
            date_str = email.header.decode_header(msg['Date'])[0][0].split('+')[0].split('-')[0]
            mail_time = datetime.datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S ")
            text, style = email.header.decode_header(msg.get('subject'))[0]
            if style == None:
                title = text
            else:
                title = text.decode(style)
            # 比对时间
            if mail_time > toal_time1:
                # 比对发件人
                if email.utils.parseaddr(msg.get("from"))[1] == send:
                    if title == toal_title:
                        # 查找邮件正文
                        for part in msg.walk():
                            if not part.is_multipart():
                                # 暂不考虑附件
                                if part.get_param("name"):
                                    pass
                                else:
                                    text = part.get_payload(decode=True)
                                    try:
                                        #print("邮件内容为：'%s'" % text.decode())
                                        return text.decode()
                                    except:
                                        raise Exception("邮件解码异常")
                elif count1 == len(self.datelist) - range + 1:
                    raise Exception("没有找到该发件人的邮件")
            else:
                break

    def re_connect_server1(self, d1, send, total_title, count=5):
        while count > 0:
            count -= 1
            toal_list = self.select_mail1(d1, send, total_title)
            if len(toal_list) == 0:
                time.sleep(1)
                print("第'%s'次重连没找到指定邮件" % str(count))
            else:
                return toal_list
        raise Exception("未找到邮件")

    def close(self):
        self.connect.close()
        self.connect.logout()




if __name__ == '__main__':
    a = MailClient('liyang@galasports.net',"23fPa'62")
    a.find_my_mail('2019-05-20 11:56:23','a13we6511@163.com','11111')
    del a
