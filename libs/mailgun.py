import os
from typing import List
from requests import Response, post


class MailgunException:
    def __init__(self, message):
        return self.message

class Mailgun:

    FROM_TITLE = "Prcing-service"
    FROM_EMAIL = "<do-not-reply@sandbox9508e951653f46459ae12f6017a965ab.mailgun.org>"
    
    
    @classmethod
    def send_email(cls, email: List[str], subject: str,text: str, html: str) -> Response:
        api_key = os.environ.get("MAILGUN_API_KEY", None)
        domain = os.environ.get("MAILGUN_DOMAIN", None)
        
        if api_key is None:
            raise MailgunException("Failed to load API KEY")

        if domain is None:
            raise MailgunException("Failed to load DOMAIN")
    	
        response = post( f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", api_key),
        data={"from": f"{Mailgun.FROM_TITLE} {Mailgun.FROM_EMAIL}",
        "to": [email, domain],
        "subject": subject,
        "text": text,
        "html": html})
        
        if response.status_code != 200:
            print(response.json())
        
        return response
    


