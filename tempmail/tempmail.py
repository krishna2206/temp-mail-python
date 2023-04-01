import random
import string
import hashlib

from requests import Session


class TempMailException(Exception):
    pass


class TempMail:
    def __init__(self, api_key: str) -> None:
        self.session = Session()
        self.url = "https://api.apilayer.com/temp_mail"
        self.session.headers.update({"apikey": api_key})

        self.__domains = []

    def create_email(self, username: str = None) -> str:
        """Create a temporary email address.

        Args:
            username (str, optional): The desired username for the email
                address. If not specified, a random username will be generated.
                Defaults to None.

        Returns:
            dict: A dictionary containing the email address and its expiration date.
        """
        domain = random.choice(self.get_domains())
        if not username:
            username = ''.join(random.choices(
                string.ascii_letters + string.digits, k=8))
        email_address = f"{username}{domain}"

        return email_address

    def get_attachments(self, mail_id: str) -> dict:
        """
        Get message attachments by mail id.

        Args:
            mail_id (str): Unique mail id.

        Sample response:
            {
                "item": {
                    "item": [
                        {
                            "cid": "f_la6ikdda1",
                            "content-type": "image/jpeg",
                            "name": "SouthwestAirlines.jpg",
                            "size": 437867
                        },
                        {
                            "cid": "f_la6ikddf2",
                            "content-type": "image/jpeg",
                            "name": "PerrierLimeLP.jpg",
                            "size": 160885
                        },
                        {
                            "cid": "f_la6ikdcy0",
                            "content-type": "image/jpeg",
                            "name": "SouthwestAirlinesVoucherExpirationLP.jpg",
                            "size": 220895
                        }
                    ]
                }
            }
        """
        response = self.session.get(self.url + f"/attachments/id/{mail_id}")

        if response.status_code != 200:
            raise TempMailException(
                f"{response.status_code} {response.reason}: {response.json()['message']}")
        return response.json()

    def delete_message(self, mail_id: str) -> dict:
        """
        Delete message by message id.

        Args:
            mail_id (str): Unique mail id.

        Sample response:
            {
                "result": "success"
            }
        """
        response = self.session.get(self.url + f"/delete/id/{mail_id}")

        if response.status_code != 200:
            raise TempMailException(
                f"{response.status_code} {response.reason}: {response.json()['message']}")
        return response.json()

    def get_domains(self, fresh: bool = False) -> list:
        """Get list of usable domains.

        Args:
            fresh (bool, optional): Get fresh list of domains. Defaults to False.

        Sample response:
            [
                "@cevipsa.com",
                "@cpav3.com",
                "@nuclene.com",
                "@steveix.com",
                "@mocvn.com",
                "@tenvil.com",
                "@tgvis.com",
                "@amozix.com",
                "@anypsd.com",
                "@maxric.com"
            ]
        """
        if not self.__domains or fresh:
            response = self.session.get(self.url + "/domains")

            if response.status_code != 200:
                raise TempMailException(
                    f"{response.status_code} {response.reason}: {response.json()['message']}")
            self.__domains = response.json()
        return self.__domains

    def get_mails(self, mail_address: str) -> list:
        """
        Check and get a list of emails for a mailbox.

        Args:
            mail_address (str): Mailbox address.

        Sample response:
            [
                {
                    "_id": {
                    "$oid": "6368bd726792f000194ecd59"
                    },
                    "createdAt": {
                    "$date": {
                        "$numberLong": 1667808626055
                    }
                    },
                    "mail_address_id": "041e3c606326862bc70f92ab8af8a3fe",
                    "mail_attachments": [],
                    "mail_attachments_count": 0,
                    "mail_from": "API Test ",
                    "mail_html": "This is just a email testing demo.",
                    "mail_id": "f22028c061a5787284a0999941cdd784",
                    "mail_preview": "...",
                    "mail_subject": "Email test",
                    "mail_text": "This is just a email testing demo.",
                    "mail_text_only": "This is just a email testing demo.",
                    "mail_timestamp": 1667808626.052
                },
                {
                    "_id": {
                    "$oid": "6368be2f40ee390023960482"
                    },
                    "createdAt": {
                    "$date": {
                        "$numberLong": 1667808815947
                    }
                    },
                    "mail_address_id": "041e3c606326862bc70f92ab8af8a3fe",
                    "mail_attachments": [],
                    "mail_attachments_count": 0,
                    "mail_from": "API Test ",
                    "mail_html": "This is another test.",
                    "mail_id": "3d4d6e84797c6bbba794f8de882abb2f",
                    "mail_preview": "...",
                    "mail_subject": "Another test",
                    "mail_text": "This is another test.",
                    "mail_text_only": "This is another test.",
                    "mail_timestamp": 1667808815.944
                }
            ]
        """
        domain = f"@{mail_address.split('@')[1]}"
        if domain not in self.get_domains():
            raise TempMailException(
                f"Domain {domain} is not in the list of usable domains.")

        hash_object = hashlib.md5(mail_address.encode())
        hashed_mail_address = hash_object.hexdigest()
        response = self.session.get(
            self.url + f"/mail/id/{hashed_mail_address}")

        if response.status_code != 200:
            raise TempMailException(
                f"{response.status_code} {response.reason}: {response.json()['message']}")
        return response.json()

    def get_one_attachments(self, mail_id: str, attachment_id: str) -> dict:
        """Get one message attachments by mail id and attachment id from attachments list.
        Content response field encoded in base64 RFC 4648.

        Args:
            mail_id (str): Unique mail id.
            attachment_id (str): Unique attachment id.

        Sample response:
            {
                "cid": "f_la6ikdcy0",
                "content": "/9j/ 4RMSRXhpZgAATU0AKgAAAAgABwESAAMAAAABAAEAAAEaAAUAAAABAAAAYgEbAAUAAAABAAAAagEoAAMAAAABAAMAAAExAAIAAAAfAAAAcgEyAAIAAAAUAAAAkYdpAAQAAAABAAAAqAAAANQABFNJAAAnEAAEU0kAACcQQWRvYmUgUGhvdG9zaG9wIDIxLjEgKFdpbmRvd3MpADIwMjI6MTE6MDYgMTU6NTM6NDEAAAAAAAOgAQADAAAAAf////9k=",
                "contentType": "image/jpeg",
                "name": "SouthwestAirlinesVoucherExpirationLP.jpg",
                "size": 220895
            }
        """
        response = self.session.get(
            self.url + f"/one_attachment/id/{mail_id}/{attachment_id}")

        if response.status_code != 200:
            raise TempMailException(
                f"{response.status_code} {response.reason}: {response.json()['message']}")
        return response.json()

    def get_mail(self, mail_id: str) -> dict:
        """Get one message by id.

        Args:
            mail_id (str): Unique mail id.

        Sample response:
            {
                "_id": {
                    "$oid": "6368bd726792f000194ecd59"
                },
                "createdAt": {
                    "$date": {
                        "$numberLong": 1667808626055
                    }
                },
                "mail_address_id": "041e3c606326862bc70f92ab8af8a3fe",
                "mail_attachments": [],
                "mail_attachments_count": 0,
                "mail_from": "API Test ",
                "mail_html": "This is just a email testing demo.",
                "mail_id": "f22028c061a5787284a0999941cdd784",
                "mail_preview": "...",
                "mail_subject": "Email test",
                "mail_text": "This is just a email testing demo.",
                "mail_text_only": "This is just a email testing demo.",
                "mail_timestamp": 1667808626.052
            }
        """
        response = self.session.get(self.url + f"/one_mail/id/{mail_id}")

        if response.status_code != 200:
            raise TempMailException(
                f"{response.status_code} {response.reason}: {response.json()['message']}")
        return response.json()

    def get_message_source(self, mail_id: str) -> dict:
        """Get message source by mail_id.

        Args:
            mail_id (str): Unique mail id.
        """
        response = self.session.get(self.url + f"/source/id/{mail_id}")

        if response.status_code != 200:
            raise TempMailException(
                f"{response.status_code} {response.reason}: {response.json()['message']}")
        return response.json()
