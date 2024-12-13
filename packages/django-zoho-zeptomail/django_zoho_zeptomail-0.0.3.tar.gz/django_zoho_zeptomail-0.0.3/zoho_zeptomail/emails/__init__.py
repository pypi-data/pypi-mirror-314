import requests
from zoho_zeptomail.base import base


class SendEmail(base.NewAPIClient):
    """
    Send an e-mail
    """

    def set_mail_from(self, from_mail, message):
        """
        Appends the 'from' part on an mail
        """
        message["from"] = from_mail

    def set_mail_to(self, mail_to, message):
        """2
        Appends the 'to' part on an mail
        """
        message["to"] = mail_to

    def set_subject(self, subject, message):
        """
        Appends the 'subject' part on an mail
        """
        message["subject"] = subject

    def set_body(self, body, message):
        """
        Appends the 'body' part on an mail
        """
        message["htmlbody"] = body

    def set_cc_recipients(self, cc_recipient, message):
        """
        Appends the 'cc' part on an mail
        """
        message["cc"] = cc_recipient

    def set_bcc_recipients(self, bcc_recipient, message):
        """
        Appends the 'bcc' part on an mail
        """
        message["bcc"] = bcc_recipient


    def set_attachments(self, attachments, message):
        """
        Appends an attachment on an mail
        """
        message["attachments"] = attachments

    def set_reply_to(self, reply_to, message):
        """
        Appends 'reply to' on an mail
        """
        message["reply_to"] = reply_to

    def send(self, message):
        """
        Handles mail sending

        """
        request = requests.post(
            self.get_sendmail_url(self.zeptomail_domain), headers=self.headers_default, json=message
        )
        return request

    def get_sendmail_url(self, zeptomail_url):
        return "https://api."+str(zeptomail_url)+"/v1.1/email"
