import smtplib

mail_from = "xxxx@xxx.com"
mail_to   = "yyyy@yyy.com"
mail_title = "test mail"
msg = "This is a test mail"

mail_server = smtplib.SMTP('smtp.163.com')
mail_server.login(mail_from, 'password')
mail_server.sendmail(mail_from, mail_to, msg)
