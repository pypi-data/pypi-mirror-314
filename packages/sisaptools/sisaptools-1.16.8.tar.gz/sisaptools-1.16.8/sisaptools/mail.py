# -*- coding: utf8 -*-

"""
Utilitats per enviar mails.
"""

import smtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE, formatdate
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from os.path import basename

from .constants import APP_CHARSET, IS_PYTHON_3
from .aes import AESCipher
from .services import MAIL_SERVERS


class Mail(object):
    """Classe principal a instanciar."""

    def __init__(self):
        """Inicialització de paràmetres."""
        server = "gencat" if IS_PYTHON_3 else "gmail"
        self.srv = MAIL_SERVERS[server]['host']
        self.port = MAIL_SERVERS[server]['port']
        self.ssl = MAIL_SERVERS[server]['ssl']
        self.usr = MAIL_SERVERS[server]['user']
        self.pwd = MAIL_SERVERS[server]['password']
        self.me = MAIL_SERVERS[server]['me']
        self.to = []
        self.cc = []
        self.subject = ''
        self.text = ''
        self.attachments = []

    def __construct(self):
        """Construcció del missatge, cridat per send."""
        banned = ("mmedinap@gencat.cat",)
        self.to = [el for el in self.to if el not in banned]
        self.cc = [el for el in self.cc if el not in banned]
        self.message = MIMEMultipart()
        self.message['From'] = self.me
        self.message['To'] = COMMASPACE.join(self.to)
        self.message['Cc'] = COMMASPACE.join(self.cc)
        self.message['Date'] = formatdate(localtime=True)
        self.message['Subject'] = Header(self.subject, APP_CHARSET)
        self.message.attach(MIMEText(self.text, 'plain', APP_CHARSET))
        for _attachment in self.attachments:
            if type(_attachment) in (list, tuple):
                filename, iterable = _attachment
                data = '\r\n'.join([';'.join(map(str, row)) for row in iterable])  # noqa
                attachment = MIMEText(data, 'plain', APP_CHARSET)
                attachment.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=filename
                )
            else:
                filename = _attachment
                attachment = MIMEBase('application', 'octet-stream')
                attachment.set_payload(open(filename, 'rb').read())
                if "xls" in filename:
                    encoders.encode_base64(attachment)
                attachment.add_header('Content-Disposition', 'attachment; filename="{}"'.format(basename(filename)))  # noqa
            self.message.attach(attachment)
        self.to += self.cc

    def __connect(self):
        """Connexió al servidor, cridat per send."""
        method = smtplib.SMTP_SSL if self.ssl else smtplib.SMTP
        self.server = method(self.srv, self.port)
        try:
            self.server.login(self.usr, AESCipher().decrypt(self.pwd))
        except Exception:
            pass

    def send(self):
        """Enviament del mail."""
        if self.to or self.cc:
            self.__construct()
            self.__connect()
            self.server.sendmail(self.me, self.to, self.message.as_string())
            self.server.close()
