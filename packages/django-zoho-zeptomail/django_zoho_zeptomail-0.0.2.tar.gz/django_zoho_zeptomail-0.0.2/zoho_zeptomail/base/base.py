
DOMAIN = 'zeptomail.zoho.com'

class NewAPIClient:
    """
    Instantiates the parent object all endpoints follow.
    Provides necessary connection information to perform API operations.
    """
    Domain_list = {'zeptomail.zoho.com': 'zeptomail.com', 'zeptomail.zoho.in' : 'zeptomail.in', 'zeptomail.zoho.eu' : 'zeptomail.eu','zeptomail.zoho.jp': 'zeptomail.jp', 'zeptomail.zohocloud.ca' : 'zeptomail.ca', 'zeptomail.zoho.sa': 'zeptomail.sa', 'zeptomail.zoho.com.au' : 'zeptomail.com.au', 'zeptomail.zoho.com.cn' : 'zeptomail.com.cn'}

    def __init__(self, zeptomail_api_key, zeptomail_domain = DOMAIN):
        """
        NewAPIClient constructor
        """
        if not zeptomail_api_key:
            raise ValueError("The api_key configurations are missing in settings.py")

        if not zeptomail_domain:
            raise ValueError("The domain configurations are missing in settings.py")

        if zeptomail_domain not in self.Domain_list:
            raise ValueError("Invalid domain. Please verify it.")

        self.zeptomail_domain = self.Domain_list[zeptomail_domain]
        self.zeptomail_api_key =  zeptomail_api_key
        self.headers_default = {
            "Content-Type": "application/json",
            "User-Agent": "Django ZeptoMail",
            "Authorization": f"{self.zeptomail_api_key}",
        }