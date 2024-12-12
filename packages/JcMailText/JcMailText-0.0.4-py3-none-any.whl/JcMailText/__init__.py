import email
from bs4 import BeautifulSoup

__copyright__    = 'Copyright (C) 2024 JavaCommons Technologies'
__version__      = '0.0.4'
__license__      = 'MIT'
__author__       = 'JavaCommons Technologies'
__author_email__ = 'javacommmons@gmail.com'
__url__          = 'https://github.com/javacommons/py-mail-text'
__all__ = ['JcMailText']

class JcMailText:
    def __init__(self):
        pass
    def get_mail_text(self, raw_email):
        try:
          raw_email = raw_email.decode()
        except (UnicodeDecodeError, AttributeError):
           pass
        b = email.message_from_string(raw_email)
        body = ""
        if b.is_multipart():
            for part in b.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))
                #print(f"ctype: {ctype} cdispo: {cdispo}")
                if (ctype == 'text/plain' or ctype == 'text/html') and 'attachment' not in cdispo:
                    body = part.get_payload(decode=True)  # decode
                    break
        else:
            body = b.get_payload(decode=True)
        if not isinstance(body, str):
            body = body.decode("utf-8")
        if body.startswith('<html'):
            soup = BeautifulSoup(body, features="html.parser")
            body = soup.get_text('\n')
        return body
