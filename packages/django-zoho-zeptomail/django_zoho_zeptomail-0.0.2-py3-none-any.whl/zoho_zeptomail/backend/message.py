# Python Standard Library
import json
import base64
import mimetypes
from django.conf import settings
from email.utils import parseaddr
from email.mime.base import MIMEBase
from zoho_zeptomail.emails import SendEmail


class ZeptoMailEmailMessage:
    """Wrapper class for Django email messages to send it through the
    ZeptoMail API.
    """
    if hasattr(settings, 'ZOHO_ZEPTOMAIL_API_KEY_TOKEN') and not hasattr(settings, 'ZOHO_ZEPTOMAIL_HOSTED_REGION'):
        __Zoho_ZeptoMail = SendEmail(settings.ZOHO_ZEPTOMAIL_API_KEY_TOKEN)

    elif hasattr(settings, 'ZOHO_ZEPTOMAIL_API_KEY_TOKEN') and hasattr(settings, 'ZOHO_ZEPTOMAIL_HOSTED_REGION'):
        __Zoho_ZeptoMail = SendEmail(settings.ZOHO_ZEPTOMAIL_API_KEY_TOKEN, settings.ZOHO_ZEPTOMAIL_HOSTED_REGION)

    else:
        raise ValueError("The api_key configurations are missing in settings.py")

    def __init__(self, email_message):
        """Initializes a zeptoMail email message.
        Args:
            email_message (:obj:`django.core.mail.message.EmailMessage`): The
                email message to send through the ZeptoMail API.
        """

        self.__email_message = email_message
        """:obj:`django.core.mail.message.EmailMessage`: The Django email
        message to send.
        """

        self.__email_data = {}
        """dict: Stores the converted data of the email message."""

        self.__nameless_attachment_index = 1

        self.__validate_headers()
        self.__set_body()
        self.__set_mail_from()
        self.__set_mail_to()
        self.__set_subject()
        self.__set_cc_recipients()
        self.__set_bcc_recipients()
        self.__set_reply_to()
        self.__set_attachments()

    def send(self):
        """Sends the encapsulated Django email message through the ZeptoMail
        API.

        Returns:
            int: The amount of emails sent; 1 if successfull, 0 if failed.
        """

        """Send the email message."""
        response = self.__Zoho_ZeptoMail.send(self.__email_data)
        print(f'Response : {self.handle_to_response(response)}')
        if response.status_code // 100 == 2:
            return 1
        return 0

    def __validate_headers(self):
        """Private helper method for validating the Django email message
        headers.

        Raises:
            :obj:`ValueError`: If the Django email message contains extra
                headers.
        """
        # Make sure the email does not contain any extra headers
        if len(self.__email_message.extra_headers.keys()) > 0:
            raise ValueError('Extra headers not supported')

    def __set_body(self):
        """Private helper method for converting the Django email message
       `body` and `alternatives` and setting it in the internal state.

       Raises:
           :obj:`ValueError`: If the Django email message content subtype is
               not 'plain' or 'html'.
           :obj:`ValueError`: If the Django email message has an alternative
               of which the content type is not 'text/html'.
       """

        # Make sure the main content type is supported
        content = {}
        if self.__email_message.content_subtype == 'plain':
            content['text/plain'] = self.__email_message.body
        elif self.__email_message.content_subtype == 'html':
            content['text/html'] = self.__email_message.body
        else:
            raise ValueError('Content type not supported')

        # Make sure the alternative content type is supported, if present
        if hasattr(self.__email_message, 'alternatives'):
            for alternative in self.__email_message.alternatives:
                if alternative[1] in ['text/html', 'text/plain']:
                    content[alternative[1]] = alternative[0]
                else:
                    raise ValueError('Content type not supported')

        # Set the mail content
        content['body'] =''
        if 'text/plain' in content:
            content['body'] += content['text/plain'] +"\n"
        if 'text/html' in content:
            content['body'] += content['text/html']
        self.__Zoho_ZeptoMail.set_body(content['body'], self.__email_data)

    def __set_mail_from(self):
        """Private helper method for converting the Django email message
        `from_email` and setting it in the internal state.
        """
        if self.__email_message.from_email:
           self.__Zoho_ZeptoMail.set_mail_from(self.__get_from_json(self.__email_message.from_email), self.__email_data)
        else:
           raise Exception("Zoho ZeptoMail is not providing the 'From' address!")

    def __set_mail_to(self):
        """Private helper method for converting the Django email message
        `to` and setting it in the internal state.
        """
        if self.__email_message.to:
           self.__Zoho_ZeptoMail.set_mail_to(self.__get_to_array(self.__email_message.to), self.__email_data)
        else:
           raise Exception("Zoho ZeptoMail is not providing the 'To' address!")

    def __set_subject(self):
        """Private helper method for converting the Django email message
        `subject` and setting it in the internal state.
        """
        if self.__email_message.subject:
           self.__Zoho_ZeptoMail.set_subject(self.__email_message.subject, self.__email_data)
        else:
           raise Exception("Zoho ZeptoMail is not providing the 'Subject'")

    def __set_cc_recipients(self):
        """Private helper method for converting the Django email message
        `cc` and setting it in the internal state.
        """
        if self.__email_message.cc:
           self.__Zoho_ZeptoMail.set_cc_recipients(self.__get_to_array(self.__email_message.cc), self.__email_data)

    def __set_bcc_recipients(self):
        """Private helper method for converting the Django email message
        `bcc` and setting it in the internal state.
        """
        if self.__email_message.bcc:
           self.__Zoho_ZeptoMail.set_bcc_recipients(self.__get_to_array(self.__email_message.bcc), self.__email_data)

    def __set_reply_to(self):
        """Private helper method for converting the Django email message
        `reply_to` and setting it in the internal state.
        """
        if self.__email_message.reply_to:
           self.__Zoho_ZeptoMail.set_reply_to(self.__get_replyto_array(self.__email_message.reply_to), self.__email_data)

    def __set_attachments(self):
        """Private helper method for converting the Django email message
        `attachments` and setting it in the internal state.
        """
        if self.__email_message.attachments:
           self.__Zoho_ZeptoMail.set_attachments(self.__get_attachment_array(self.__email_message.attachments), self.__email_data)

    def __get_from_json(self, default_from):
        name, email =  parseaddr(default_from)
        return { "address" : email, "name": name }

    def __get_to_array(self, to_address):
       to_array =[]
       for to in to_address:
          to_array.append(self.__get_to_json(to))
       return to_array

    def __get_to_json(self, to):
        name, email =  parseaddr(to)
        return {"email_address":{ "address": email, "name": name}}

    def __get_replyto_array(self, replyto):
        reply_array = []
        for reply in replyto:
            reply_array.append(self.__get_reply_json(reply))
        return reply_array

    def __get_reply_json(self, reply):
        name, email =  parseaddr(reply)
        return  { "address" : email, "name" :name }

    def __get_attachment_array(self, attachments):
        """Private helper method for converting the Django email message
        `attachments` and setting it in the internal state.
        """
        if len(attachments) == 0:
            return
        mail_attachments = []
        for attachment in attachments:
            file_name, file_content, content_type, *extra_info = attachment
            filename = self.__get_attachment_filename(attachment)
            content = self.__get_attachment_content(attachment)
            mail_attachments.append({
                'name': filename,
                'content': base64.b64encode(content).decode('ascii'),
                'mime_type': self.__get_mime_type(filename, content_type)
            })
        return mail_attachments

    def __get_mime_type(self, file_name, content_type):
        # Convert file_name to lowercase to handle case-insensitive file extensions
        file_name = file_name.lower()
        # Image files
        if file_name.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp')):
            if file_name.endswith(('.jpg', '.jpeg')):
               return 'image/jpeg'
            return 'image/png'  # Default to 'image/png' for other image types
        # Audio files
        elif file_name.endswith(('.mp3', '.wav', '.flac', '.aac', '.ogg')):
            return 'audio/mpeg' if file_name.endswith('.mp3') else 'audio/wav'
        # Video files
        elif file_name.endswith(('.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv')):
            return 'video/mp4' if file_name.endswith('.mp4') else 'video/x-msvideo'
        # Document files
        elif file_name.endswith(('.pdf')):
            return 'application/pdf'
        # Text files
        elif file_name.endswith(('.txt')):
            return 'text/plain'
        # HTML files
        elif file_name.endswith(('.html', '.htm')):
            return 'text/html'
       # Spreadsheet files
        elif file_name.endswith(('.xls', '.xlsx', '.csv')):
            return 'application/vnd.ms-excel' if file_name.endswith(('.xls', '.xlsx')) else 'text/csv'
       # JSON and XML files
        elif file_name.endswith(('.json')):
           return 'application/json'
        elif file_name.endswith(('.xml')):
           return 'application/xml'
       # Compressed files
        elif file_name.endswith(('.zip')):
            return 'application/zip'
        elif file_name.endswith(('.tar', '.gz', '.bz2', '.xz')):
            return 'application/x-tar'  # Use appropriate type for tarballs
       # Archive files
        elif file_name.endswith(('.rar', '.7z')):
           return 'application/x-rar-compressed'
       # PowerPoint files
        elif file_name.endswith(('.ppt', '.pptx')):
           return 'application/vnd.ms-powerpoint'
        # Word files
        elif file_name.endswith(('.doc', '.docx')):
           return 'application/msword'
       # Excel files
        elif file_name.endswith(('.xls', '.xlsx')):
            return 'application/vnd.ms-excel'
       # Font files
        elif file_name.endswith(('.ttf', '.otf')):
            return 'font/ttf' if file_name.endswith('.ttf') else 'font/otf'
       # Return the provided content_type as fallback
        else:
           return content_type

    def __get_attachment_filename(self, attachment):
        """Private helper method for getting the filename of an `attachment`
        in the Django email message.

        Note:
            If the attachment does not provide a filename, a filename is
            automatically provided using the pattern "attachment-", followed by
            an auto-incremented number which starts at 1. The filename
            extension is guessed using the attachment's mimetype.

        Returns:
            str: The filename of the attachment.
        """
        if isinstance(attachment, MIMEBase):
            filename = attachment.get_filename()
        else:
            filename = attachment[0]

        # If no filename was given, provide a generic filename
        if filename is None:
            filename = \
                'ZeptoMail Attachment-' \
                + str(self.__nameless_attachment_index) \
                + mimetypes.guess_extension(
                    attachment.get_content_type()
                )
            self.__nameless_attachment_index += 1

        return filename

    def __get_attachment_content(self, attachment):
        """Private helper method for getting the content of an `attachment`
        in the Django email message as bytes.

        Returns:
            bytes: The content of the Django email message as bytes.
        """
        if isinstance(attachment, MIMEBase):
            content = attachment.get_payload()

            # If no content charset is present, the file is a
            # binary file, so base64 decode the string into bytes
            if attachment.get_content_charset() is None:
                content = base64.b64decode(content)

            # Otherwise, the file is a text file, so encode the
            # string to bytes
            else:
                content = content.encode()

        else:
            content = attachment[1]

            # If the content is a string, encode it into bytes
            if isinstance(content, str):
                content = content.encode()

        return content

    def handle_to_response(self, response):
        response_data = {}
        data = json.loads(response.text)

        # If the response status code is 2xx.
        if response.status_code // 100 == 2:
            response_data['status'] = 'suceess'
            response_data['message'] = data['data'][0]['message'] or 'successfully sent the email'
        # If the response status code is not 2xx.
        else:
            response_data['staus'] = 'failure'
            response_data['message'] = data['error']['details'][0]['message']
            try:
                response_data['target'] = data['error']['details'][0]['target']
            except:
                pass
        return response_data



