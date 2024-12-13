from django.core.mail.backends.base import BaseEmailBackend
from zoho_zeptomail.backend.message import ZeptoMailEmailMessage

class ZohoZeptoMailEmailBackend(BaseEmailBackend):
    """
    Custom email backend for sending emails via ZeptoMail's API.
    Supports all `EmailMessage` attributes like subject, body, cc, bcc, reply_to, attachments, etc.
    """

    def send_messages(self, email_messages):
        """Send the provided Django email messages through the ZeptoMail API.

        Args:
            :obj:`list` of :obj:`django.core.mail.message.EmailMessage`: A list
                of the Django email messages to send.
        Returns:
            int: The amount of emails sent.
        """
        sent_emails = 0
        for email_message in email_messages:
            zepto_email_message = ZeptoMailEmailMessage(email_message)
            sent_emails += zepto_email_message.send()
        return sent_emails
