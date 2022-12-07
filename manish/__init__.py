
"""
Unofficial python wrapper for the WhatsApp Cloud API.
"""
import os
import requests
import mimetypes
import validators
from loguru import logger
from .helpers import Helpers
from .location import *
from requests_toolbelt.multipart.encoder import MultipartEncoder
from typing import Optional, Dict, Any, List, Union, Tuple, Callable


class MaNish(object):

    def __init__(self,token:str=None,phone_number_id:str=None):
        """
        Init the MaNish (Whatsapp) object.

        Args:
            token[str]: Token for the Whatsapp cloud API (Make sure to generate permanent one)
            phone_number_id[str]: Phone number id for the WhatsApp cloud API.
        """
        self.phone_number_id = phone_number_id
        self.base_url = "https://graph.facebook.com/v15.0"
        self.url = f"{self.base_url}/{phone_number_id}/messages"
        self.token = token
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.token),
        }


    def send_message(self, message, recipient_id, recipient_type="individual", preview_url=True):
        """
         Sends a text message to a WhatsApp user
         Args:
                message[str]: Message to be sent to the user
                recipient_id[str]: Phone number of the user with country code wihout +
                recipient_type[str]: Type of the recipient, either individual or group
                preview_url[bool]: Whether to send a preview url or not
        Example:
            ```python
            >>> from manish import MaNish
            >>> manish = MaNish(token, phone_number_id)
            >>> manish.send_message("Hello World", "1122334455667")
            >>> manish.send_message("Hello World", "1122334455667", preview_url=False)
        """
        try:
            data = {
                "messaging_product": "whatsapp",
                "recipient_type": recipient_type,
                "to": recipient_id,
                "type": "text",
                "text": {"preview_url": preview_url, "body": message},
            }
            logger.info(f"Sending message to {recipient_id}")
            r = requests.post(f"{self.url}", headers=self.headers, json=data)
            if r.status_code == 200:
                logger.info(f"Message sent to {recipient_id}")
                return r.json()
            logger.info(f"Message not sent to {recipient_id}")
            logger.info(f"Status code: {r.status_code}")
            logger.info(f"Response: {r.json()}")
            return r.json()
        except Exception as e:
            logger.error("aw snap something went wrong: " + str(e))
            return '{"error":"' + str(e)  + '"}'


    def send_video(self, video, recipient_id, caption=None):
        """ "
        Sends a video message to a WhatsApp user
        Video messages can either be sent by passing the video id or by passing the video link.
        Args:
            video[str]: Video id or link of the video
            recipient_id[str]: Phone number of the user with country code wihout +
            caption[str]: Caption of the video
            link[bool]: Whether to send a video id or a video link, True means that the video is an id, False means that the video is a link
        example:
            >>> from manish import MaNish
            >>> manish = MaNish(token, phone_number_id)
            >>> manish.send_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "1122334455667")
        """
        if validators.url(video):
            data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "type": "video",
                "video": {"link": video, "caption": caption},
            }
        else:
            if os.path.exists(video):
                id = self.upload_media(video)
            else:
                id = video
            data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "type": "video",
                "video": {"id": id, "caption": caption},
            }
        logger.info(f"Sending video to {recipient_id}")
        r = requests.post(self.url, headers=self.headers, json=data)
        if r.status_code == 200:
            logger.info(f"Video sent to {recipient_id}")
            return r.json()
        logger.info(f"Video not sent to {recipient_id}")
        logger.info(f"Status code: {r.status_code}")
        logger.error(f"Response: {r.json()}")
        return r.json()


    def send_document(self, document, recipient_id, caption=None):
        """ "
        Sends a document message to a WhatsApp user
        Document messages can either be sent by passing the document id or by passing the document link.
        Args:
            document[str]: Document id or link of the document
            recipient_id[str]: Phone number of the user with country code wihout +
            caption[str]: Caption of the document
            link[bool]: Whether to send a document id or a document link, True means that the document is an id, False means that the document is a link
        Example:
            >>> from manish import MaNish
            >>> manish = MaNish(token, phone_number_id)
            >>> manish.send_document("https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "1122334455667")
        """
        if validators.url(document):
            data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "type": "document",
                "document": {"link": document, "caption": caption},
            }
        else:
            if os.path.exists(document):
                id = self.upload_media(document)
            else:
                id = document
            data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "type": "document",
                "document": {"id": id, "caption": caption},
            }
        logger.info(f"Sending document to {recipient_id}")
        r = requests.post(self.url, headers=self.headers, json=data)
        if r.status_code == 200:
            logger.info(f"Document sent to {recipient_id}")
            return r.json()
        logger.info(f"Document not sent to {recipient_id}")
        logger.info(f"Status code: {r.status_code}")
        logger.error(f"Response: {r.json()}")
        return r.json()


    def send_audio(self, audio, recipient_id):
        """
        Sends an audio message to a WhatsApp user
        Audio messages can either be sent by passing the audio id or by passing the audio link.
        Args:
            audio[str]: Audio id or link of the audio
            recipient_id[str]: Phone number of the user with country code wihout +
            link[bool]: Whether to send an audio id or an audio link, True means that the audio is an id, False means that the audio is a link
        Example:
            >>> from manish import MaNish
            >>> manish = MaNish(token, phone_number_id)
            >>> manish.send_audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", "1122334455667")
        """
        try:
            if validators.url(audio):
                data = {
                    "messaging_product": "whatsapp",
                    "to": recipient_id,
                    "type": "audio",
                    "audio": {"link": audio},
                }
            else:
                if os.path.exists(audio):
                    id = self.upload_media(audio)
                else:
                    id = audio
                data = {
                    "messaging_product": "whatsapp",
                    "to": recipient_id,
                    "type": "audio",
                    "audio": {"id": id},
                }
            logger.info(f"Sending audio to {recipient_id}")
            r = requests.post(self.url, headers=self.headers, json=data)
            if r.status_code == 200:
                logger.info(f"Audio sent to {recipient_id}")
                return r.json()
            logger.info(f"Audio not sent to {recipient_id}")
            logger.info(f"Status code: {r.status_code}")
            logger.error(f"Response: {r.json()}")
            return r.json()
        except Exception as e:
            logger.error("aw snap something went wrong: " + str(e))
            return '{"error":"' + str(e)  + '"}'

    def send_image(self, image, recipient_id, recipient_type="individual", caption=None):
        """
        Sends an image message to a WhatsApp user
        There are two ways to send an image message to a user, either by passing the image id or by passing the image link.
        Image id is the id of the image uploaded to the cloud api.
        Args:
            image[str]: Image id or link of the image
            recipient_id[str]: Phone number of the user with country code wihout +
            recipient_type[str]: Type of the recipient, either individual or group
            caption[str]: Caption of the image
            link[bool]: Whether to send an image id or an image link, True means that the image is an id, False means that the image is a link
        Example:
            >>> from manish import MaNish
            >>> manish = MaNish(token, phone_number_id)
            >>> manish.send_image("https://i.imgur.com/Fh7XVYY.jpeg", "5511999999999")
        """
        if validators.url(image):
            data = {
                "messaging_product": "whatsapp",
                "recipient_type": recipient_type,
                "to": recipient_id,
                "type": "image",
                "image": {"link": image, "caption": caption},
            }
        else:
            if os.path.exists(image):
                id = self.upload_media(image)
            else:
                id = image
            data = {
                "messaging_product": "whatsapp",
                "recipient_type": recipient_type,
                "to": recipient_id,
                "type": "image",
                "image": {"id": id, "caption": caption},
            }
        logger.info(f"Sending image to {recipient_id}")
        r = requests.post(self.url, headers=self.headers, json=data)
        if r.status_code == 200:
            logger.info(f"Image sent to {recipient_id}")
            return r.json()
        logger.info(f"Image not sent to {recipient_id}")
        logger.info(f"Status code: {r.status_code}")
        logger.error(r.json())
        return r.json()

    def send_sticker(self, sticker, recipient_id, recipient_type="individual", caption=None):
        """
        Sends an image message to a WhatsApp user
        There are two ways to send an image message to a user, either by passing the image id or by passing the image link.
        Image id is the id of the image uploaded to the cloud api.
        Args:
            image[str]: Image id or link of the image
            recipient_id[str]: Phone number of the user with country code wihout +
            recipient_type[str]: Type of the recipient, either individual or group
            caption[str]: Caption of the image
            link[bool]: Whether to send an image id or an image link, True means that the image is an id, False means that the image is a link
        Example:
            >>> from manish import MaNish
            >>> manish = MaNish(token, phone_number_id)
            >>> manish.send_image("https://i.imgur.com/Fh7XVYY.jpeg", "5511999999999")
        """
        if validators.url(sticker):
            data = {
                "messaging_product": "whatsapp",
                "recipient_type": recipient_type,
                "to": recipient_id,
                "type": "image",
                "image": {"link": sticker, "caption": caption},
            }
        else:
            if os.path.exists(sticker):
                sticker = Helpers().convert_to_webp(sticker)
                id = self.upload_media(sticker)
            else:
                id = sticker
            data = {
                "messaging_product": "whatsapp",
                "recipient_type": recipient_type,
                "to": recipient_id,
                "type": "sticker",
                "sticker": {"id": id},
            }
        logger.info(f"Sending image to {recipient_id}")
        r = requests.post(self.url, headers=self.headers, json=data)
        if r.status_code == 200:
            logger.info(f"Image sent to {recipient_id}")
            return r.json()
        logger.info(f"Image not sent to {recipient_id}")
        logger.info(f"Status code: {r.status_code}")
        logger.error(r.json())
        return r.json()




    def send_contacts(self, contacts: List[Dict[Any, Any]], recipient_id: str):
        """send_contacts
        Send a list of contacts to a user
        Args:
            contacts(List[Dict[Any, Any]]): List of contacts to send
            recipient_id(str): Phone number of the user with country code wihout +
        Example:
            >>> from manish import MaNish
            >>> manish = MaNish(token, phone_number_id)
            >>> contacts = Contacts Object
        REFERENCE: https://developers.facebook.com/docs/whatsapp/cloud-api/reference/messages#contacts-object
        """

        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "contacts",
            "contacts": contacts,
        }
        logger.info(f"Sending contacts to {recipient_id}")
        r = requests.post(self.url, headers=self.headers, json=data)
        if r.status_code == 200:
            logger.info(f"Contacts sent to {recipient_id}")
            return r.json()
        logger.info(f"Contacts not sent to {recipient_id}")
        logger.info(f"Status code: {r.status_code}")
        logger.error(f"Response: {r.json()}")
        return r.json()






    def send_location(self, location: Location, recipient_id):
        """
        Sends a location message to a WhatsApp user
        Args:
            lat[str]: Latitude of the location
            long[str]: Longitude of the location
            name[str]: Name of the location
            address[str]: Address of the location
            recipient_id[str]: Phone number of the user with country code wihout +
        Example:
            >>> from manish import MaNish
            >>> manish = MaNish(token, phone_number_id)
            >>> manish.send_location("-23.564", "-46.654", "My Location", "Rua dois, 123", "5511999999999")
        """
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "location",
            "location": {
                "latitude": location.latitude,
                "longitude": location.longitude,
                "name": location.name,
                "address": location.address,
            },
        }
        logger.info(f"Sending location to {recipient_id}")
        r = requests.post(self.url, headers=self.headers, json=data)
        if r.status_code == 200:
            logger.info(f"Location sent to {recipient_id}")
            return r.json()
        logger.info(f"Location not sent to {recipient_id}")
        logger.info(f"Status code: {r.status_code}")
        logger.error(r.json())
        return r.json()



    def upload_media(self, media: str):
        """
        Uploads a media to the cloud api and returns the id of the media.
        Args:
            media[str]: Path of the media to be uploaded
        Example:
            >>> from manish import MaNish
            >>> manish = MaNish(token, phone_number_id)
            >>> whatsapp.upload_media("/path/to/media")
        Returns:
            >>> Media ID
        REFERENCE: https://developers.facebook.com/docs/whatsapp/cloud-api/reference/media#
        """
        try:
            form_data = {
                "file": (
                    media,
                    open(os.path.realpath(media), "rb"),
                    mimetypes.guess_type(media)[0],
                ),
                "messaging_product": "whatsapp",
                "type": mimetypes.guess_type(media)[0],
            }
            form_data = MultipartEncoder(fields=form_data)
            headers = self.headers.copy()
            headers["Content-Type"] = form_data.content_type
            logger.info(f"Content-Type: {form_data.content_type}")
            logger.info(f"Uploading media {media}")
            r = requests.post(
                f"{self.base_url}/{self.phone_number_id}/media",
                headers=headers,
                data=form_data,
            )
            if r.status_code == 200:
                logger.info(f"Media {media} uploaded")
                return r.json()["id"]
            logger.info(f"Error uploading media {media}")
            logger.info(f"Status code: {r.status_code}")
            logger.info(f"Response: {r.json()}")
            return None
        except Exception as e:
            logger.error("aw snap something went wrong: " + str(e))
            return '{"error":"' + str(e)  + '"}'