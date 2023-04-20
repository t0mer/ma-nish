
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
from .button import *
from requests_toolbelt.multipart.encoder import MultipartEncoder
from typing import Optional, Dict, Any, List, Union, Tuple, Callable


class MaNish(object):


    def __init__(self,token:str=None,phone_number_id:str=None):
        try:
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
        except Exception as e:
            logger.error("Error initializing MaNish: " + str(e))


    def set_status(self, message_id):
        """
        Change the status of a message.
        Args:
            message_id[str]: The id of the message
        Example:
            ```python
            >>> from manish import MaNish
            >>> manish = MaNish(token, phone_number_id)
            >>> manish.set_status(message_id)

        """
        try:
            data = {
                "messaging_product": "whatsapp",
                "status": "read",
                "message_id": message_id
            }
            r = requests.post(f"{self.url}", headers=self.headers, json=data)
            if r.status_code == 200:
                logger.info(f"Message ID {message_id} marked as read")
                return r.json()
        except Exception as e:
            logger.error("aw snap something went wrong: " + str(e))
            return '{"error":"' + str(e)  + '"}'



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
            >>> manish.send_video("https://www.youtube.com/watch?v=ul_9qe_fiTY", "1122334455667")
        """
        try:
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
        except Exception as e:
            logger.error("aw snap something went wrong: " + str(e))
            return '{"error":"' + str(e)  + '"}'

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
        try:
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
        except Exception as e:
            logger.error("aw snap something went wrong: " + str(e))
            return '{"error":"' + str(e)  + '"}'

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
            >>> manish.send_audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-9.mp3", "1122334455667")
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
            >>> manish.send_image("https://i.imgur.com/Fh7XVYY.jpeg", "1122334455667")
        """
        try:
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
                    logger.debug(id)
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
        except Exception as e:
            logger.error("aw snap something went wrong: " + str(e))
            return '{"error":"' + str(e)  + '"}'

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
            >>> manish.send_image("https://i.imgur.com/COXQuEz.jpeg", "1122334455667")
        """
        try:
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
        except Exception as e:
            logger.error("aw snap something went wrong: " + str(e))
            return '{"error":"' + str(e)  + '"}'

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
        try:
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
        except Exception as e:
            logger.error("aw snap something went wrong: " + str(e))
            return '{"error":"' + str(e)  + '"}'

    def send_location(self, location: Location, recipient_id):
        """
        Sends a location message to a WhatsApp user
        Args:
            location: Location object (If no coordinates provided, it will be generated using geopy)
            recipient_id[str]: Phone number of the user with country code wihout +
        Example:
            >>> from manish import MaNish
            >>> manish = MaNish(token, phone_number_id)
            >>> manish.send_location(Location, "1122334455667")
        """
        try:
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
        except Exception as e:
            logger.error("aw snap something went wrong: " + str(e))
            return '{"error":"' + str(e)  + '"}'

    def send_template(self, template, recipient_id, lang="en_US", components: str={}):
        """
        Sends a template message to a WhatsApp user, Template messages can either be;
            1. Text template
            2. Media based template
        You can customize the template message by using the Component object and pass it as json.
        You can find the available components in the documentation.
        https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-message-templates
        Args:
            template[str]: Template name to be sent to the user
            recipient_id[str]: Phone number of the user with country code wihout +
            lang[str]: Language of the template message
            components[dict]: Dictionary of components to be sent to the user
        Example:
            >>> from namish import MaNish
            >>> namish = MaNish(token, phone_number_id)
            >>> MaNish.send_template("hello_world", "1122334455667", lang="en_US"))
        """
        try:
            data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "type": "template",
                "template": {
                    "name": template,
                    "language": {"code": lang},
                    "components": components,
                },
            }
            logger.info(f"Sending template to {recipient_id}")
            r = requests.post(self.url, headers=self.headers, json=data)
            if r.status_code == 200:
                logger.info(f"Template sent to {recipient_id}")
                return r.json()
            logger.info(f"Template not sent to {recipient_id}")
            logger.info(f"Status code: {r.status_code}")
            logger.info(f"Response: {r.json()}")
            return r.json()
        except Exception as e:
            logger.error("aw snap something went wrong: " + str(e))
            return '{"error":"' + str(e)  + '"}'

    def reply_to_message(self, message_id: str, recipient_id: str, message: str, preview_url: bool = True):
        """
        Replies to a message
        Args:
            message_id[str]: Message id of the message to be replied to
            recipient_id[str]: Phone number of the user with country code wihout +
            message[str]: Message to be sent to the user
            preview_url[bool]: Whether to send a preview url or not
        """
        try:
            data = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": recipient_id,
                "type": "text",
                "context": {"message_id": message_id},
                "text": {"preview_url": preview_url, "body": message},
            }

            logger.info(f"Replying to {message_id}")
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

    def send_button(self, button, recipient_id):
        """
        Sends an interactive buttons message to a WhatsApp user
        Args:
            button[dict]: Generate button using Button object and pass it as srting
            recipient_id[str]: Phone number of the user with country code wihout +
        check https://github.com/Neurotech-HQ/heyoo#sending-interactive-reply-buttons for an example.
        """
        try:
            button = json.loads(button)
            data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "type": "interactive",
                "interactive": self.create_button(button),
            }
            logger.info(f"Sending buttons to {recipient_id}")
            r = requests.post(self.url, headers=self.headers, json=data)
            if r.status_code == 200:
                logger.info(f"Buttons sent to {recipient_id}")
                return r.json()
            logger.info(f"Buttons not sent to {recipient_id}")
            logger.info(f"Status code: {r.status_code}")
            logger.info(f"Response: {r.json()}")
            return r.json()
        except Exception as e:
            logger.error("aw snap something went wrong: " + str(e))
            return '{"error":"' + str(e)  + '"}'

    def delete_media(self, media_id: str):
        """
        Deletes a media from the cloud api
        Args:
            media_id[str]: Id of the media to be deleted
        """
        try:
            logger.info(f"Deleting media {media_id}")
            r = requests.delete(f"{self.base_url}/{media_id}", headers=self.headers)
            if r.status_code == 200:
                logger.info(f"Media {media_id} deleted")
                return r.json()
            logger.info(f"Error deleting media {media_id}")
            logger.info(f"Status code: {r.status_code}")
            logger.info(f"Response: {r.json()}")
            return None
        except Exception as e:
            logger.error("aw snap something went wrong: " + str(e))
            return '{"error":"' + str(e)  + '"}'

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

    def preprocess(self, data):
        """
        Preprocesses the data received from the webhook.
        This method is designed to only be used internally.
        Args:
            data[dict]: The data received from the webhook
        """
        return data["entry"][0]["changes"][0]["value"]

    def query_media_url(self, media_id: str):
        """
        Query media url from media id obtained either by media Id
        Args:
            media_id[str]: Media id of the media
        Returns:
            str: Media url
        Example:
            >>> from manish import MaNish
            >>> manish = MaNish(token, phone_number_id)
            >>> manish.query_media_url("media_id")
        """
        try:
            logger.info(f"Querying media url for {media_id}")
            r = requests.get(f"{self.base_url}/{media_id}", headers=self.headers)
            if r.status_code == 200:
                logger.info(f"Media url queried for {media_id}")
                return r.json()["url"]
            logger.info(f"Media url not queried for {media_id}")
            logger.info(f"Status code: {r.status_code}")
            logger.info(f"Response: {r.json()}")
            return None
        except Exception as e:
            logger.error("aw snap something went wrong: " + str(e))
            return '{"error":"' + str(e)  + '"}'

    def download_media(self, media_url: str, mime_type: str, file_path: str = ""):
        """
        Download media from media url obtained either by manually uploading media or received media
        Args:
            media_url[str]: Media url of the media
            mime_type[str]: Mime type of the media
            file_path[str]: Path of the file to be downloaded to. Default is "temp"
                            Do not include the file extension. It will be added automatically.
        Returns:
            str: Media url
        Example:
            >>> from manish import MaNish
            >>> manish = MaNish(token, phone_number_id)
            >>> manish.download_media("media_url", "image/jpeg")
            >>> manish.download_media("media_url", "video/mp4", "path/to/file") #do not include the file extension
        """
        try:
            r = requests.get(media_url, headers=self.headers)
            content = r.content
            extension = mime_type.split("/")[1]
            if ";" in extension:
                extension = extension.split(";")[0]
            # create a temporary file
            try:
                if file_path == "":
                    save_file_here = f"/tmp/temp.{extension}"
                else:
                    save_file_here = f"{file_path}/temp.{extension}"
                save_file_here = (
                    f"{file_path}.{extension}" if file_path else f"temp.{extension}"
                )
                with open(save_file_here, "wb") as f:
                    f.write(content)
                logger.info(f"Media downloaded to {save_file_here}")
                return f.name
            except Exception as e:
                print(e)
                logger.info(f"Error downloading media to {save_file_here}")
                return None
        except Exception as e:
            logger.error("aw snap something went wrong: " + str(e))
            return '{"error":"' + str(e)  + '"}'


    def get_name(self, data):
        """
        Extracts the name of the sender from the data received from the webhook.
        Args:
            data[dict]: The data received from the webhook
        Returns:
            str: The name of the sender
        Example:
            >>> from manish import MaNish
            >>> manish = MaNish(token, phone_number_id)
            >>> mobile = manish.get_name(data)
        """
        try:
            contact = self.preprocess(data)
            if contact:
                return contact["contacts"][0]["profile"]["name"]
            return None
        except Exception as e:
            logger.error("aw snap something went wrong: " + str(e))
            return None

    def get_message(self, data):
        """
        Extracts the text message of the sender from the data received from the webhook.
        Args:
            data[dict]: The data received from the webhook
        Returns:
            str: The text message received from the sender
        Example:
            >>> from manish import MaNish
            >>> manish = MaNish(token, phone_number_id)
            >>> message = manish.get_message(data)
        """
        try:
            data = self.preprocess(data)
            if "messages" in data:
                return data["messages"][0]["text"]["body"]
            return None
        except Exception as e:
            logger.error("aw snap something went wrong: " + str(e))
            return None

    def get_message_id(self, data):
        """
        Extracts the message id of the sender from the data received from the webhook.
        Args:
            data[dict]: The data received from the webhook
        Returns:
            str: The message id of the message
        Example:
            >>> from manish import MaNish
            >>> manish = MaNish(token, phone_number_id)
            >>> message_id = manish.get_message_id(data)
        """
        try:
            data = self.preprocess(data)
            if "messages" in data:
                return data["messages"][0]["id"]
            return None
        except Exception as e:
            logger.error("aw snap something went wrong: " + str(e))
            return None

    def get_message_timestamp(self, data):
        """ "
        Extracts the timestamp of the message from the data received from the webhook.
        Args:
            data[dict]: The data received from the webhook
        Returns:
            str: The timestamp of the message
        Example:
            >>> from manish import Manish
            >>> manish = Manish(token, phone_number_id)
            >>> manish.get_message_timestamp(data)
        """
        try:
            data = self.preprocess(data)
            if "messages" in data:
                return data["messages"][0]["timestamp"]
            return None
        except Exception as e:
            logger.error("aw snap something went wrong: " + str(e))
            return None

    def get_interactive_response(self, data):
        """
         Extracts the response of the interactive message from the data received from the webhook.
         Args:
            data[dict]: The data received from the webhook
        Returns:
            dict: The response of the interactive message
        Example:
            >>> from manish import MaNish
            >>> manish = MaNish(token, phone_number_id)
            >>> response = manish.get_interactive_response(data)
            >>> intractive_type = response.get("type")
            >>> message_id = response[intractive_type]["id"]
            >>> message_text = response[intractive_type]["title"]
        """
        try:
            data = self.preprocess(data)
            if "messages" in data:
                if "interactive" in data["messages"][0]:
                    return data["messages"][0]["interactive"]
            return None
        except Exception as e:
            logger.error("aw snap something went wrong: " + str(e))
            return '{"error":"' + str(e)  + '"}'

    def get_location(self, data):
        """
        Extracts the location of the sender from the data received from the webhook.
        Args:
            data[dict]: The data received from the webhook
        Returns:
            dict: The location of the sender
        Example:
            >>> from manish import MaNish
            >>> manish = MaNish(token, phone_number_id)
            >>> manish.get_location(data)
        """
        try:
            data = self.preprocess(data)
            if "messages" in data:
                if "location" in data["messages"][0]:
                    return data["messages"][0]["location"]
            return None
        except Exception as e:
            logger.error("aw snap something went wrong: " + str(e))
            return None

    def get_image(self, data):
        """ "
        Extracts the image of the sender from the data received from the webhook.
        Args:
            data[dict]: The data received from the webhook
        Returns:
            dict: The image_id of an image sent by the sender
        Example:
            >>> from manish import MaNish
            >>> manish = MaNish(token, phone_number_id)
            >>> image_id = manish.get_image(data)
        """
        try:
            data = self.preprocess(data)
            if "messages" in data:
                if "image" in data["messages"][0]:
                    return data["messages"][0]["image"]
            return None
        except Exception as e:
            logger.error("aw snap something went wrong: " + str(e))
            return None

    def get_audio(self, data):
        """
        Extracts the audio of the sender from the data received from the webhook.
        Args:
            data[dict]: The data received from the webhook
        Returns:
            dict: The audio of the sender
        Example:
            >>> from manish import MaNish
            >>> manish = MaNish(token, phone_number_id)
            >>> manish.get_audio(data)
        """
        try:
            data = self.preprocess(data)
            if "messages" in data:
                if "audio" in data["messages"][0]:
                    return data["messages"][0]["audio"]
            return None
        except Exception as e:
            logger.error("aw snap something went wrong: " + str(e))
            return None


    def get_mobile(self, data: Dict[Any, Any]) -> Union[str, None]:
        """
        Extracts the mobile number of the sender from the data received from the webhook.
        Args:
            data[dict]: The data received from the webhook
        Returns:
            str: The mobile number of the sender
        Example:
            >>> from whatsapp import WhatsApp
            >>> manish = MaNish(token, phone_number_id)
            >>> mobile = manish.get_mobile(data)
        """
        data = self.preprocess(data)
        if "contacts" in data:
            return data["contacts"][0]["wa_id"]


    def get_video(self, data):
        """
        Extracts the video of the sender from the data received from the webhook.
        Args:
            data[dict]: The data received from the webhook
        Returns:
            dict: Dictionary containing the video details sent by the sender
        Example:
            >>> from manish import MaNish
            >>> manish = MaNish(token, phone_number_id)
            >>> manish.get_video(data)
        """
        try:
            data = self.preprocess(data)
            if "messages" in data:
                if "video" in data["messages"][0]:
                    return data["messages"][0]["video"]
            return None
        except Exception as e:
            logger.error("aw snap something went wrong: " + str(e))
            return None

    def get_message_type(self, data):
        """
        Gets the type of the message sent by the sender from the data received from the webhook.
        Args:
            data [dict]: The data received from the webhook
        Returns:
            str: The type of the message sent by the sender
        Example:
            >>> from manish import MaNish
            >>> manish = MaNish(token, phone_number_id)
            >>> manish.get_message_type(data)
        """
        try:
            data = self.preprocess(data)
            if "messages" in data:
                return data["messages"][0]["type"]
            return None
        except Exception as e:
            logger.error("aw snap something went wrong: " + str(e))
            return None

    def get_delivery(self, data):
        """
        Extracts the delivery status of the message from the data received from the webhook.
        Args:
            data [dict]: The data received from the webhook
        Returns:
            dict: The delivery status of the message and message id of the message
        """
        try:
            data = self.preprocess(data)
            if "statuses" in data:
                return data["statuses"][0]["status"]
            return None
        except Exception as e:
            logger.error("aw snap something went wrong: " + str(e))
            return None

    def changed_field(self, data):
        """
        Helper function to check if the field changed in the data received from the webhook.
        Args:
            data [dict]: The data received from the webhook
        Returns:
            str: The field changed in the data received from the webhook
        Example:
            >>> from manish import MaNish
            >>> manish = MaNish(token, phone_number_id)
            >>> manish.changed_field(data)
        """
        try:
            return data["entry"][0]["changes"][0]["field"]
        except Exception as e:
            logger.error("aw snap something went wrong: " + str(e))
            return None

    def create_button(self, button):
        """
        Method to create a button object to be used in the send_message method.
        This is method is designed to only be used internally by the send_button method.
        Args:
               button[dict]: A dictionary containing the button data
        """
        data = {
            "type": "list",
            "action": button.get("action")
        }
        if button.get("header"):
            data["header"] = {"type": "text", "text": button.get("header")}
        if button.get("body"):
            data["body"] = {"text": button.get("body")}
        if button.get("footer"):
            data["footer"] = {"text": button.get("footer")}
        return data
