#!/usr/bin/env python3

from email.mime.text import MIMEText
from smtplib import SMTP
from time import sleep
from urllib.request import urlopen as get_request

# ----

subject = " %s "

mail_text = '''
 %s 
'''

list_of_mail_adresses = []

smtp_server_hostname = ''
smtp_server_port = 587
smtp_server_user = ''
smtp_server_password = ''

keyword = ''
list_of_websites = []

check_interval_in_seconds = 60*60*2

# ----

def is_granulat_on(website):
    if not website.startswith('http'):
        website = 'http://' + website
    with get_request(website) as response:
        html_content = response.read().decode()
    return keyword in html_content.casefold()


def write_mail(website):
    mail = MIMEText(mail_text % website)
    mail['Subject'] = subject % website
    mail['From'] = smtp_server_user
    mail['To'] = ','.join(list_of_mail_adresses)
    server = SMTP(host=smtp_server_hostname, port=smtp_server_port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(user=smtp_server_user, password=smtp_server_password)
    server.sendmail(from_addr=smtp_server_user, to_addrs=list_of_mail_adresses, msg=mail.as_string())
    server.quit()
    print(mail.as_string())


# ----
while len(list_of_websites) > 0:
    print(list_of_websites)
    for website in list_of_websites:
        if is_granulat_on(website):
            write_mail(website)
            list_of_websites.remove(website)
    sleep(check_interval_in_seconds)
