import smtplib


def trigger_mail(self, sent_from, to, host, password, subject, body):
    email_text = """
    From: %s  
    To: %s  
    Subject: %s
    
    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP(host, 25)
        server.connect(host, 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sent_from, password)
        server.sendmail(sent_from, to, email_text)
        server.close()
        return 'Email sent!'
    except Exception as e:
        return 'Something went wrong...'+str(e)
