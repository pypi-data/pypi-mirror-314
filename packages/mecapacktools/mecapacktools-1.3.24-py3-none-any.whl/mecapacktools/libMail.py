#! /usr/bin/env python
# -*- coding:Utf-8 -*-
# pylint: disable=fixme,invalid-name,line-too-long,dangerous-default-value
"""Mail system management."""
# ============================================================
#    Linux python path and Library import
# ============================================================

import mimetypes
import os.path
from collections import UserList
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEBase, MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP, SMTPServerDisconnected

from . import libLog

try:
    # some systems
    # pylint: disable-next=ungrouped-imports
    from email import charset as Charset
except ImportError:
    from email import Charset

# ============================================================
#    Variables and Constants
# ============================================================

Charset.add_charset("utf-8", Charset.QP, Charset.QP, "utf-8")


# ============================================================
#    Class
# ============================================================


# ||||||||||||||||||||||||||||||||||||||||||||||||||
#    ListEmail
# ||||||||||||||||||||||||||||||||||||||||||||||||||
class ListEmail(object):
    """Class to manage the list of email."""

    # //////////////////////////////////////////////////
    #    Variables and Constants
    # //////////////////////////////////////////////////

    #: Constant
    SEPARATOR = ","

    # //////////////////////////////////////////////////
    #     INITIALIZATION
    # //////////////////////////////////////////////////
    def __init__(self, pval=""):
        valTemp = pval
        if not isinstance(pval, str):
            valTemp = self.SEPARATOR.join(pval)
        self.__val = valTemp

    # //////////////////////////////////////////////////
    #     Value
    # //////////////////////////////////////////////////
    @property
    def Value(self):
        """
        return Value

        Returns:
            str: value
        """
        return self.__val

    # //////////////////////////////////////////////////
    #     __add__
    # //////////////////////////////////////////////////
    def __add__(self, pval):
        valTemp = self.__val
        if not len(pval) == 0:
            if not len(valTemp) == 0:
                valTemp += self.SEPARATOR
            if isinstance(pval, str):
                valTemp += pval
            else:
                valTemp += self.SEPARATOR.join(pval)
        return ListEmail(valTemp)

    # //////////////////////////////////////////////////
    #     __iadd__
    # //////////////////////////////////////////////////
    def __iadd__(self, pval):
        if not len(pval) == 0:
            if not len(self.__val) == 0:
                self.__val += self.SEPARATOR
            if isinstance(pval, str):
                self.__val += pval
            else:
                self.__val += self.SEPARATOR.join(pval)
        return self

    # //////////////////////////////////////////////////
    #     __sub__
    # //////////////////////////////////////////////////
    def __sub__(self, pval):
        valTemp = self.__val
        if not len(pval) == 0 and not len(valTemp) == 0:
            if isinstance(pval, str):
                pval = [pval]
            valTemp = self.SEPARATOR.join(
                [itemTemp for itemTemp in valTemp.split(self.SEPARATOR) if itemTemp not in pval]
            )
        return ListEmail(valTemp)

    # //////////////////////////////////////////////////
    #     __isub__
    # //////////////////////////////////////////////////
    def __isub__(self, pval):
        if not len(pval) == 0 and not len(self.__val) == 0:
            if isinstance(pval, str):
                pval = [pval]
            self.__val = self.SEPARATOR.join(
                [itemTemp for itemTemp in self.__val.split(self.SEPARATOR) if itemTemp not in pval]
            )
        return self

    # //////////////////////////////////////////////////
    #     __str__
    # //////////////////////////////////////////////////
    def __str__(self):
        return self.__val

    # //////////////////////////////////////////////////
    #     __repr__
    # //////////////////////////////////////////////////
    def __repr__(self):
        return self.__val


# ||||||||||||||||||||||||||||||||||||||||||||||||||
#    Mails
# ||||||||||||||||||||||||||||||||||||||||||||||||||
class Mails(UserList):
    """Class to manage the mail stream."""

    # //////////////////////////////////////////////////
    #    Variables and Constants
    # //////////////////////////////////////////////////

    #: Default parameters
    hshParam = {}
    hshParam["process"] = "Mails"
    hshParam["server"] = ""
    hshParam["port"] = 0
    hshParam["portTLS"] = 587
    hshParam["user"] = ""
    hshParam["password"] = ""
    hshParam["realEmail_send"] = False
    hshParam["defaultEmail"] = ""

    # //////////////////////////////////////////////////
    #     INITIALIZATION
    # //////////////////////////////////////////////////
    def __init__(self, phshParam={}):
        """Initialization of the class"""

        # Base initialization
        UserList.__init__(self)
        # Start log manager
        self.log = libLog.Log()
        # Update of parameters
        self.hshParam.update(phshParam)

    # //////////////////////////////////////////////////
    #     Send_all
    # //////////////////////////////////////////////////
    def Send_all(self, pserver="", pport=0, puser="", ppassword=""):
        """
        Send all mail in class

        Args:
            pserver (str, optional): the smtp server. Defaults to "".
            pport (int, optional): the smtp port. Defaults to 0.
            puser (str, optional): user. Defaults to "".
            ppassword (str, optional): password. Defaults to "".

        Raises:
            self.log.CustomException: Some mails were not sent
            self.log.CustomException: All sending mails failed
            self.log.CustomException: No mail to send
        """

        self.log.setStep = "SMTP_initialization"
        # Setting work variables
        if pserver != "":
            self.hshParam["server"] = pserver
        if pport != 0:
            self.hshParam["port"] = pport
        if puser != "":
            self.hshParam["user"] = puser
        if ppassword != "":
            self.hshParam["password"] = ppassword
        # Initialization of the SMTP management
        SMTP_management = SMTP(self.hshParam["server"], self.hshParam["port"], timeout=300)
        if self.hshParam["user"]:
            SMTP_management = self.TLS_Connect()

        # Log
        self.log.Debug("SMTP Server : %s", self.hshParam["server"])
        self.log.Debug("Port : %s", self.hshParam["port"])

        self.log.setStep = "Sending"
        # Work variables
        mailRowcount = len(self.data)
        mailSentOk = mailSentKo = 0
        # Sending all mail
        for msg_temp in self.data:
            if isinstance(msg_temp, Mail):
                mailSender = msg_temp.Sender()
                mailReceivers = msg_temp.Receivers()
                self.log.Debug("Sender : %s", mailSender)
                self.log.Debug("Receivers : %s", mailReceivers)
                if not self.hshParam["realEmail_send"]:
                    mailReceivers = self.hshParam["defaultEmail"]
                    self.log.Debug("Default email used : %s", mailReceivers)
                try:
                    SMTP_management.sendmail(mailSender, mailReceivers, msg_temp.msg.as_string())
                    mailSentOk += 1
                    self.log.Info("Mail sent to %s with success", mailReceivers)
                except SMTPServerDisconnected:  # Retry to connect one time to mail server in case of timout
                    try:
                        SMTP_management.quit()  # Ensure that previus session was disconected
                    # pylint: disable-next=broad-exception-caught
                    except Exception:
                        pass  # Deal with alea of deconnexion by office365
                    SMTP_management = self.TLS_Connect()
                    SMTP_management.sendmail(mailSender, mailReceivers, msg_temp.msg.as_string())
                    mailSentOk += 1
                    self.log.Info("Mail sent to %s with success", mailReceivers)
                # pylint: disable-next=broad-exception-caught
                except Exception as e:
                    self.log.Warning("Mail not sent to %s : %s", mailReceivers, e, exc_info=1)
                    mailSentKo += 1
            else:
                self.log.Warning("Mail definition is not valid : %s", Mail, exc_info=1)
                mailSentKo += 1
        # Assessment
        try:
            SMTP_management.quit()
        except SMTPServerDisconnected:
            pass  # Deal with alea of deconnexion by office365
        self.log.Debug("Mail count : %s", mailRowcount)
        self.log.Debug("ok : %s", mailSentOk)
        self.log.Debug("failed : %s", mailSentKo)
        if mailRowcount == 0:
            raise self.log.CustomException("No mail to send")
        elif mailRowcount == mailSentKo:
            raise self.log.CustomException("All sending mails failed")
        elif mailRowcount == mailSentOk:
            self.log.Info("All mails are sent successfully")
        else:
            raise self.log.CustomException("Some mails were not sent")

    # //////////////////////////////////////////////////
    #     Connect to mail server via TLS
    #     Return SMTP connection
    # //////////////////////////////////////////////////
    def TLS_Connect(self):
        """
        Connect to mail server via TLS

        Returns:
            SMTP: SMTP_management
        """
        self.log.Info("Connecting to mail server via TLS")
        SMTP_management = SMTP(self.hshParam["server"], self.hshParam["portTLS"], timeout=300)
        # SMTP_management.connect()
        SMTP_management.ehlo()
        SMTP_management.starttls()
        # SMTP_management.ehlo()
        SMTP_management.login(self.hshParam["user"], self.hshParam["password"])
        return SMTP_management


# ||||||||||||||||||||||||||||||||||||||||||||||||||
#    Mail
# ||||||||||||||||||||||||||||||||||||||||||||||||||
class Mail(object):
    """Class to manage the mail data."""

    # //////////////////////////////////////////////////
    #    Variables and Constants
    # //////////////////////////////////////////////////

    #: Variables
    hshParam = {}
    hshParam["process"] = "Mail"

    # //////////////////////////////////////////////////
    #     INITIALIZATION
    # //////////////////////////////////////////////////
    def __init__(self):
        # Definition of the message details
        self.msg = MIMEMultipart()

        # Work variables
        self.__From = ""
        self.__To = ListEmail()
        self.__Cc = ListEmail()
        self.__Bcc = ListEmail()
        self.__Subject = ""
        self.__Body_html = ""
        self.__Body_text = ""
        self.__Attachments = []

    # //////////////////////////////////////////////////
    #     From
    # //////////////////////////////////////////////////
    @property
    def From(self):
        """
        From property

        Args:
            pemail (str): From

        Returns:
            str: From
        """
        return self.__From

    @From.setter
    def From(self, pemail):
        self.msg["From"] = self.__From = pemail

    # //////////////////////////////////////////////////
    #     To
    # //////////////////////////////////////////////////
    @property
    def To(self):
        """
        To property

        Args:
            pemails (listEmail or str): email

        Returns:
            listEmail or str: To
        """
        return self.__To

    @To.setter
    def To(self, pemails):
        if isinstance(pemails, ListEmail):
            self.__To = pemails
        else:
            self.__To = ListEmail(pemails)
        del self.msg["To"]
        self.msg["To"] = self.__To.Value

    # //////////////////////////////////////////////////
    #     Cc
    # //////////////////////////////////////////////////
    @property
    def Cc(self):
        """
        Cc property

        Args:
            pemails (listEmail or str): email

        Returns:
            listEmail or str: Cc
        """
        return self.__Cc

    @Cc.setter
    def Cc(self, pemails):
        if isinstance(pemails, ListEmail):
            self.__Cc = pemails
        else:
            self.__Cc = ListEmail(pemails)
        del self.msg["Cc"]
        self.msg["Cc"] = self.__Cc.Value

    # //////////////////////////////////////////////////
    #     Bcc
    # //////////////////////////////////////////////////
    @property
    def Bcc(self):
        """
        Bcc property

        Args:
            pemails (listEmail or str): email

        Returns:
            listEmail or str: Bcc
        """
        return self.__Bcc

    @Bcc.setter
    def Bcc(self, pemails):
        if isinstance(pemails, ListEmail):
            self.__Bcc = pemails
        else:
            self.__Bcc = ListEmail(pemails)

    # //////////////////////////////////////////////////
    #     Subject
    # //////////////////////////////////////////////////
    @property
    def Subject(self):
        """
        Subject property

        Args:
            pmessage (str): Subject

        Returns:
            str: Subject
        """
        return self.__Subject

    @Subject.setter
    def Subject(self, pmessage):
        self.msg["Subject"] = self.__Subject = pmessage

    # //////////////////////////////////////////////////
    #     Body_html
    # //////////////////////////////////////////////////
    @property
    def Body_html(self):
        """
        Body_html property

        Args:
            pbody (str): Body_html

        Returns:
            str: Body_html
        """
        return self.__Body_html

    @Body_html.setter
    def Body_html(self, pbody):
        self.__Body_html = pbody
        msg_text_temp = MIMEText(self.__Body_html, "html", "UTF-8")
        self.msg.attach(msg_text_temp)

    # //////////////////////////////////////////////////
    #     Body_text
    # //////////////////////////////////////////////////
    @property
    def Body_text(self):
        """
        Body_text property

        Args:
            pbody (str): Body_text

        Returns:
            str: Body_text
        """
        return self.__Body_text

    @Body_text.setter
    def Body_text(self, pbody):
        self.__Body_text = pbody
        msg_text_temp = MIMEText(self.__Body_text, "plain")
        self.msg.attach(msg_text_temp)

    # //////////////////////////////////////////////////
    #     Add_attachment
    # //////////////////////////////////////////////////
    def Add_attachment(self, pAttachFile_path, pAttachFile_newname=""):
        """
        Add file to mail

        Args:
            pAttachFile_path (str): the attach file path
            pAttachFile_newname (str, optional): the new name of the file. Defaults to "".
        """

        # Check value of file path
        if not len(pAttachFile_path.strip()) == 0:
            # Manage special characters and return absolute path
            pAttachFile_path = os.path.abspath(pAttachFile_path)
            # Check the file path
            if os.path.isfile(pAttachFile_path):
                # Define the name of file in mail
                fileTemp_name = os.path.basename(pAttachFile_path)
                fileTemp_extension = os.path.splitext(pAttachFile_path)[1].strip()
                if not len(os.path.splitext(pAttachFile_newname)[0].strip()) == 0:
                    if len(os.path.splitext(pAttachFile_newname)[1].strip()) == 0:
                        fileTemp_name = os.path.splitext(pAttachFile_newname)[0].strip() + fileTemp_extension
                    else:
                        fileTemp_name = pAttachFile_newname
                # Determine type and encoding of file
                ctype, encoding = mimetypes.guess_type(pAttachFile_path)
                if ctype is None or encoding is not None:
                    ctype = "application/octet-stream"
                maintype, subtype = ctype.split("/", 1)
                # Loading file
                if maintype == "text":
                    fileTemp = open(pAttachFile_path, encoding="utf-8")
                    msg_attach_temp = MIMEText(fileTemp.read(), _subtype=subtype)
                    fileTemp.close()
                elif maintype == "image":
                    fileTemp = open(pAttachFile_path, "rb")
                    msg_attach_temp = MIMEImage(fileTemp.read(), _subtype=subtype)
                    fileTemp.close()
                elif maintype == "audio":
                    fileTemp = open(pAttachFile_path, "rb")
                    msg_attach_temp = MIMEAudio(fileTemp.read(), _subtype=subtype)
                    fileTemp.close()
                else:
                    fileTemp = open(pAttachFile_path, "rb")
                    msg_attach_temp = MIMEBase(maintype, subtype)
                    msg_attach_temp.set_payload(fileTemp.read())
                    fileTemp.close()
                    # Encode the payload using Base64
                    encoders.encode_base64(msg_attach_temp)
                # Set filename parameter
                msg_attach_temp.add_header("Content-Disposition", "attachment", filename=fileTemp_name)
                # Attach the file to the message and save reference
                self.msg.attach(msg_attach_temp)
                self.__Attachments.append([fileTemp_name, pAttachFile_path, msg_attach_temp])

    # //////////////////////////////////////////////////
    #     Receivers
    # //////////////////////////////////////////////////
    def Sender(self):
        """
        Returns From

        Returns:
            str: From email
        """
        return self.__From

    # //////////////////////////////////////////////////
    #     Receivers
    # //////////////////////////////////////////////////
    def Receivers(self):
        """
        Email "Receivers" property

        Returns:
            str: email in order To + Cc + Bcc
        """
        lstTemp = []
        if not len(self.__To.Value) == 0:
            lstTemp += self.__To.Value.split(self.__To.SEPARATOR)
        if not len(self.__Cc.Value) == 0:
            lstTemp += self.__Cc.Value.split(self.__Cc.SEPARATOR)
        if not len(self.__Bcc.Value) == 0:
            lstTemp += self.__Bcc.Value.split(self.__Bcc.SEPARATOR)
        return lstTemp

    # //////////////////////////////////////////////////
    #     Attachment
    # //////////////////////////////////////////////////
    def Attachments(self):
        """
        Attachments property

        Returns:
            list: attachment list
        """
        return self.__Attachments
