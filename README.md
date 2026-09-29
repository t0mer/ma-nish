# manish

[![PyPI version](https://img.shields.io/pypi/v/ma-nish)](https://pypi.org/project/ma-nish/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/t0mer/ma-nish/blob/main/LICENSE)

WhatsApp has now opened up its API, so you no longer have to go through a partner to send and receive WhatsApp messages!

**MaNish** (`ma-nish` on PyPI, imported as `manish`) is an unofficial Python wrapper for the [WhatsApp Cloud API](https://developers.facebook.com/docs/whatsapp/cloud-api). It lets you send text, media, stickers, locations, contacts, interactive lists, reactions and template messages from Python, and it gives you helpers for parsing the webhook payloads that WhatsApp sends back. The repository also includes a ready-to-run [FastAPI webhook example](https://github.com/t0mer/ma-nish/blob/main/webhook.py).

> **Disclaimer:** This is an unofficial project. It is not affiliated with, endorsed by, or sponsored by Meta Platforms, Inc. or WhatsApp LLC. "WhatsApp" and "Meta" are trademarks of their respective owners. Your use of the WhatsApp Cloud API is subject to Meta's terms and policies.

## Table of contents

- [Features](#features)
- [Components and frameworks used in manish](#components-and-frameworks-used-in-manish)
- [Limitations](#limitations)
- [Requirements](#requirements)
- [Installation](#installation)
- [Setting up the environment](#setting-up-the-environment)
- [Quick start](#quick-start)
- [Sending messages](#sending-messages)
- [Media management](#media-management)
- [Webhook](#webhook)
- [API reference](#api-reference)
- [Error handling](#error-handling)
- [Usage statistics](#usage-statistics)
- [Security notes](#security-notes)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Features

1. Sending text messages (with optional link preview)
2. Replying to a specific message (quoted reply)
3. Sending media (images, audio, video and documents) from a URL, a local file (uploaded automatically) or an existing media ID
4. Sending stickers from a media ID or a local image (local images are converted to WebP; see the [sticker notes](#sending-a-sticker))
5. Sending locations, either from coordinates or from a street address (geocoded with [geopy](https://pypi.org/project/geopy/))
6. Sending contacts
7. Sending interactive list messages (a button that opens a list of selectable rows)
8. Sending template messages (text, currency and image-header parameters)
9. Sending emoji reactions to a message
10. Marking a message as read
11. Uploading, querying, downloading and deleting media
12. Parsing messages and media received through the webhook (sender, name, text, location, media, interactive replies, delivery status)

## Components and frameworks used in manish

Used by the library:

* [Loguru](https://pypi.org/project/loguru/)
* [Requests](https://pypi.org/project/requests/)
* [requests-toolbelt](https://pypi.org/project/requests-toolbelt/)
* [validators](https://pypi.org/project/validators/)
* [geopy](https://pypi.org/project/geopy/)
* [Pillow](https://pypi.org/project/Pillow/)
* [dataclasses-json](https://pypi.org/project/dataclasses-json/)

Used by the webhook example (`webhook.py`):

* [FastAPI](https://pypi.org/project/fastapi/)
* [Uvicorn](https://pypi.org/project/uvicorn/)
* [python-dotenv](https://pypi.org/project/python-dotenv/)

All of the above (plus [Jinja2](https://pypi.org/project/Jinja2/)) are installed automatically when you install `ma-nish` from PyPI.

## Limitations

* Meta charges per message (or per conversation, depending on the pricing model in effect). Check the official [WhatsApp Business Platform pricing](https://developers.facebook.com/docs/whatsapp/pricing) for the current free tier and rates.
* You can only send non-template messages to a user within the 24-hour customer service window, which opens when that user messages you. Outside that window, use [template messages](#sending-template-messages).
* You can't send messages to a group; manish targets individual recipients.
* The Graph API version is fixed at **v15.0** in the code (`https://graph.facebook.com/v15.0`). It is hard-coded; check Meta's [Graph API versioning docs](https://developers.facebook.com/docs/graph-api/guides/versioning) for the status of that version.
* Interactive messages are always sent as **list** messages; reply-button, CTA-URL and other interactive types are not supported.
* Template media parameters support **images** only (`MediaParameter` has an `image` field).

## Requirements

* Python 3 (the publish workflow builds with Python 3.9; `setup.py` does not declare `python_requires`)
* A Meta developer account and a Meta app with the WhatsApp product (see [Setting up the environment](#setting-up-the-environment))
* An access token and the **Phone number ID** of your WhatsApp Business phone number
* A publicly reachable HTTPS URL if you want to receive messages through a webhook
* Outbound internet access to `graph.facebook.com` (and to OpenStreetMap Nominatim if you geocode addresses)

## Installation

### Installing from PyPI

```bash
# Windows
pip install --upgrade ma-nish

# Linux | macOS
pip3 install --upgrade ma-nish
```

### Installation from source

Use git to clone the repository, or download it manually, as shown below:

```bash
$ git clone https://github.com/t0mer/ma-nish/
$ cd ma-nish
ma-nish $ pip install .
```

## Setting up the environment

### Set up a Meta app

First, follow the [instructions on this page](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started) to:

* Register as a Meta developer
* Enable two-factor authentication for your account
* Create a Meta app (you need a **Business** app for WhatsApp)

The screenshots below walk through the process. Meta changes its developer console from time to time, so the screens you see may look a little different.

1. Go to [My Apps](https://developers.facebook.com/apps/) and click **Create App**.

2. Select the **Business** app type:

   ![Create app](https://raw.githubusercontent.com/t0mer/ma-nish/main/screenshots/create%20app.png)

3. Give the app a name and a contact email, then click **Create app**.

4. Re-enter your Facebook password when asked.

5. In the list of products, find **WhatsApp** and click **Set up**:

   ![Select WhatsApp](https://raw.githubusercontent.com/t0mer/ma-nish/main/screenshots/select%20whatsapp.png)

6. Create or select a Meta Business Account. You will receive a WhatsApp test phone number that can send messages to up to 5 phone numbers:

   ![Get test number](https://raw.githubusercontent.com/t0mer/ma-nish/main/screenshots/get%20test%20number.png)

[![New app](https://techblog.co.il/wp-content/uploads/2022/12/new-app.png "New App")](https://techblog.co.il/wp-content/uploads/2022/12/new-app.png "New App")

### Get the access token and Phone number ID

On the **Getting started** page you'll be given a temporary access token and a **Phone number ID**. Note these down, as you'll need them later. The temporary token expires after 24 hours; for anything long-lived, generate a permanent token (for example, with a System User in Meta Business Settings).

[![Getting started](https://techblog.co.il/wp-content/uploads/2022/12/test-number.png "Getting started")](https://techblog.co.il/wp-content/uploads/2022/12/test-number.png "Getting started")

### Add a recipient and send a test message

Set up your own phone number as a recipient, and you can have a go at sending yourself a test message:

1. Open the **To** drop-down and choose **Manage phone number list**.

2. Enter your phone number.

3. Enter the verification code that WhatsApp sends you.

4. Select the number and click **Send message**.

5. The **hello_world** template message arrives on your phone:

   ![Test message](https://raw.githubusercontent.com/t0mer/ma-nish/main/screenshots/test%20message.png)

### Set up a message template

In the test message above, you used the **hello_world** template. You'll need to set up your own templates for your own purposes. Go to [Message Templates](https://business.facebook.com/wa/manage/message-templates/) in WhatsApp Manager to build your own templates.

In the following example, I created a template for my smart home. The template header is fixed, and so is the footer. In the body, I added a variable for dynamic text:

[![Smart Home Template](https://techblog.co.il/wp-content/uploads/2022/12/my-template.png "Smart Home Template")](https://techblog.co.il/wp-content/uploads/2022/12/my-template.png "Smart Home Template")

Once you're done with the above, you're ready to start sending messages using **manish**.

## Quick start

### Authentication

Before you can send messages, create a `MaNish` object with your access token and the **Phone number ID** of your WhatsApp number:

```python
from manish import MaNish
manish = MaNish('TOKEN', phone_number_id='xxxxxxxxxx')
```

Keep the token out of your source code. For example, load it from environment variables:

```python
import os
from manish import MaNish

manish = MaNish(os.getenv("TOKEN"), phone_number_id=os.getenv("PHONE_NUMBER_ID"))
```

Once the object is created, you can start sending messages. As mentioned above, you can only send messages other than templates after the target phone has messaged you within the last 24 hours.

### Send your first message

```python
manish.send_message(
    message='Your message',
    recipient_id='97250xxxxxxx'
)
```

***The mobile number must include the country code, without the + symbol.***

## Sending messages

### Sending text messages

This method can be used for sending simple text messages. Link previews are on by default; pass `preview_url=False` to turn them off.

```python
manish.send_message(
    message='Your message',
    recipient_id='97250xxxxxxx'
)
```

### Replying to a message

Sends a text message as a quoted reply to an earlier message. You can get the message ID from the webhook with `get_message_id()`.

```python
manish.reply_to_message(
    message_id="wamid.HBgLM...",
    recipient_id="97250xxxxxxx",
    message="Got it, thanks!"
)
```

### Sending media

The following media types are supported:

* Images
* Video
* Audio
* Documents
* Stickers

For each one you can specify:

* A URL for the media (any value that `validators.url()` accepts).
* A local file path. The file is uploaded to WhatsApp first, and the returned media ID is used.
* An existing WhatsApp media ID (anything that is neither a URL nor an existing file).

### Sending an image

```python
manish.send_image(
    image="https://i.imgur.com/COXQuEz.jpeg",
    recipient_id="97250xxxxxxx",
    caption="Optional caption",
)
```

### Sending a video

```python
manish.send_video(
    video="https://user-images.githubusercontent.com/4478920/200173402-8a8343c3-afc2-4341-86ea-c833bed98a9a.mp4",
    recipient_id="97250xxxxxxx",
)
```

### Sending audio

```python
manish.send_audio(
    audio="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-9.mp3",
    recipient_id="97250xxxxxxx",
)
```

### Sending a document

```python
manish.send_document(
    document="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
    recipient_id="97250xxxxxxx",
)
```

### Sending a sticker

Cloud API: static and animated third-party outbound stickers are supported, in addition to all types of inbound stickers. A static sticker needs to be 512x512 pixels and cannot exceed 100 KB. An animated sticker must be 512x512 pixels and cannot exceed 500 KB.

The most reliable way to send a sticker is with the media ID of a WebP image that you have already uploaded:

```python
media_id = manish.upload_media("sticker.webp")
manish.send_sticker(sticker=media_id, recipient_id="97250xxxxxxx")
```

> **Notes on the current code:**
>
> * **Local files:** manish converts a local image to WebP before uploading it (it does not resize it). The converted file name is built as `str(os.path.splitext(path)) + ".webp"`. With a bare file name such as `img2.png` this works, but it leaves a file literally named `('img2', '.png').webp` in the current working directory. With a path that includes a directory (for example `images/img2.png`), the conversion fails and the sticker is not sent. Sending a local sticker also creates a `./temp` directory in the current working directory.
> * **URLs:** a sticker given as a URL is sent as an **`image`** message, not as a sticker:
>
>   ```python
>   # Sent as an image message, not a sticker
>   manish.send_sticker(sticker="https://i.imgur.com/COXQuEz.webp", recipient_id="97250xxxxxxx")
>   ```

### Sending a location

The location message object requires **longitude** and **latitude**, but you can also send a real address, and manish will translate the address into coordinates (using the OpenStreetMap Nominatim geocoder) and send the message.

```python
from manish.location import *
location = Location(address="Champ de Mars, 5 Avenue Anatole France, Paris", name="Eiffel Tower")
manish.send_location(location=location, recipient_id="97250xxxxxxx")
```

Or with coordinates (no geocoding):

```python
location = Location(name="Eiffel Tower", latitude="48.8584", longitude="2.2945")
manish.send_location(location=location, recipient_id="97250xxxxxxx")
```

### Sending contact(s)

Build the contact with the classes in `manish.contact`, encode it with `ContactEncoder`, and pass the result to `send_contacts`. Wrapping the encoded JSON with `json.loads()` gives the API a real list of contact objects, which is what the `contacts` parameter expects.

```python
import json
from manish.contact import *
phones = [Phone(phone="97250xxxxxxx", type="CELL")]
name = Name(formatted_name="Jane Doe", first_name="Jane", last_name="Doe")
addresses = [Address(street="1600 Pennsylvania Avenue NW", city="Washington", state="DC", zip="20500", country="United States")]
emails = [Email("jane.doe@example.com")]
contact = Contact(name=name, addresses=addresses, emails=emails, phones=phones)
data = json.loads(ContactEncoder().encode([contact]))
manish.send_contacts(data, "97250xxxxxxx")
```

### Sending an interactive list (buttons)

`send_button` sends an interactive **list** message: a button (`Action.button`) that opens a list of sections, each with selectable rows. The user's choice comes back to your webhook as an `interactive` message (see `get_interactive_response`).

```python
from manish.button import *
rows = []
rows.append(Row("row 1", "Send Money", ""))
rows.append(Row("row 2", "Withdraw Money", ""))
sections = []
sections.append(Section("iBank", rows))
action = Action("Button Testing", sections)
button = Button("Header Testing", "Body Testing", "Footer Testing", action)
data = ButtonEncoder().encode(button)
manish.send_button(data, "97250xxxxxxx")
```

`send_button` expects the **JSON string** produced by `ButtonEncoder().encode(...)`; it parses the string itself.

### Sending template messages

This method lets you send template-based messages, which bypass the 24-hour customer service window limitation.

Template messages can either be:

* Text templates (which can also include a currency object)
* Media templates (same as text, but with media in the header)

The default language code is `en_US`.

#### Sending a simple text template

```python
import json
from manish.template import *
parameter = Parameter(type="text", text="Your Text Message")
body = Component(type="body", parameters=[parameter])
components = json.loads(TemplateEncoder().encode([body]))
manish.send_template(template="smart_home", recipient_id="97250xxxxxxx", lang="he", components=components)
```

#### Sending a media template

**Media can only be attached to the header!**

```python
import json
from manish.template import *
parameter = Parameter(type="text", text="Your Text Message")
img = Media(link="https://raw.githubusercontent.com/t0mer/broadlinkmanager-docker/master/screenshots/Devices%20List.png")
iparam = MediaParameter(type="image", image=img)
body = Component(type="body", parameters=[parameter])
header = Component(type="header", parameters=[iparam])
components = json.loads(TemplateEncoder().encode([body, header]))
manish.send_template(template="smart_home_media", recipient_id="97250xxxxxxx", lang="he", components=components)
```

#### Sending a template with a currency parameter

```python
currency = Currency(fallback_value="$100.99", code="USD", amount_1000=100990)
cparam = CurrencyParameter(type="currency", currency=currency)
body = Component(type="body", parameters=[cparam])
components = json.loads(TemplateEncoder().encode([body]))
manish.send_template(template="your_template", recipient_id="97250xxxxxxx", components=components)
```

### Sending a reaction

```python
manish.send_reaction(
    emoji="\U0001F600",
    message_id="wamid.HBgLM...",
    recipient_id="97250xxxxxxx"
)
```

### Marking a message as read

```python
manish.set_status("wamid.HBgLM...")
```

## Media management

```python
media_id = manish.upload_media("/path/to/image.jpg")   # returns the media ID
url = manish.query_media_url(media_id)                 # returns a short-lived download URL
path = manish.download_media(url, "image/jpeg", "downloads/photo")  # saves downloads/photo.jpeg (downloads/ must already exist)
manish.delete_media(media_id)
```

`download_media` adds the file extension from the MIME type. With no `file_path`, the file is saved as `temp.<extension>` in the current working directory (and overwritten on every call). The target directory must already exist: if the file can't be written, `download_media` returns `None`.

## Webhook

Well, until now you were only able to send messages. But what if you need to respond to incoming messages?
So I created a [webhook](https://github.com/t0mer/ma-nish/blob/main/webhook.py) using [FastAPI](https://fastapi.tiangolo.com/). Feel free to customize and change it to fit your needs.

With this webhook you can:

* **Verify the webhook** (the WhatsApp Cloud API requires webhook token verification)
* **Get the sender's mobile number**
* **Get the message text from the sender**
* **Get a location sent by the sender**
* **Get media (image, video, audio) sent by the user** (documents too, with the fix shown in the [usage example](#webhook-usage-example); the shipped `webhook.py` does not handle them)
* **Get the delivery status**

### Running the example webhook

`webhook.py` reads its settings from environment variables (or a `.env` file, loaded with `python-dotenv`):

| Variable | Description |
|----------|-------------|
| `TOKEN` | WhatsApp Cloud API access token |
| `PHONE_NUMBER_ID` | Phone number ID of your WhatsApp Business number |
| `VERIFY_TOKEN` | Any secret string you choose; enter the same value as the **Verify token** when you configure the webhook in your Meta app |

It exposes two routes on `/`:

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/` | Webhook verification: echoes `hub.challenge` when `hub.mode=subscribe` and `hub.verify_token` matches `VERIFY_TOKEN` |
| `POST` | `/` | Receives webhook events (messages and delivery statuses) |

`webhook.py` is not part of the PyPI package. Clone the repository (or download [`webhook.py`](https://github.com/t0mer/ma-nish/blob/main/webhook.py) on its own), then run it:

```bash
git clone https://github.com/t0mer/ma-nish
cd ma-nish
pip install ma-nish
export TOKEN=... PHONE_NUMBER_ID=... VERIFY_TOKEN=...
python webhook.py   # listens on 0.0.0.0:7020
```

The server must be reachable over public HTTPS (for example, behind a reverse proxy or a tunnel). In your Meta app, open **WhatsApp > Configuration**, set the callback URL and verify token, and subscribe to the **messages** webhook field.

### Verify token example

```python
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

@app.get("/", include_in_schema=False)
async def verify(request: Request):
    if request.query_params.get('hub.mode') == "subscribe" and request.query_params.get("hub.challenge"):
        if not request.query_params.get('hub.verify_token') == VERIFY_TOKEN:
            return PlainTextResponse("Verification token mismatch", status_code=403)
        return int(request.query_params.get('hub.challenge'))
    return "Hello world"
```

> `webhook.py` returns `"Verification token mismatch", 403` as a tuple. FastAPI does not treat a returned tuple as a status code, so it answers with HTTP 200. The snippet above returns a real 403.

### Webhook usage example

```python
@app.post("/", include_in_schema=False)
async def webhook(request: Request):
    data = await request.json()
    changed_field = manish.changed_field(data)
    if changed_field == "messages":
        new_message = manish.get_mobile(data)
        if new_message:
            mobile = manish.get_mobile(data)
            name = manish.get_name(data)
            message_type = manish.get_message_type(data)
            logger.info(
                f"New Message; sender:{mobile} name:{name} type:{message_type}"
            )
            if message_type == "text":
                message = manish.get_message(data)
                logger.info(f"Message: {message}")
                manish.send_message(f"Hi {name}, nice to connect with you", mobile)
            elif message_type == "interactive":
                message_response = manish.get_interactive_response(data)
                interactive_type = message_response.get("type")
                message_id = message_response[interactive_type]["id"]
                message_text = message_response[interactive_type]["title"]
                logger.info(f"Interactive Message; {message_id}: {message_text}")
            elif message_type == "location":
                message_location = manish.get_location(data)
                message_latitude = message_location["latitude"]
                message_longitude = message_location["longitude"]
                logger.info(f"Location: {message_latitude}, {message_longitude}")
            elif message_type == "image":
                image = manish.get_image(data)
                image_id, mime_type = image["id"], image["mime_type"]
                image_url = manish.query_media_url(image_id)
                image_filename = manish.download_media(image_url, mime_type)
                logger.info(f"{mobile} sent image {image_filename}")
            elif message_type == "video":
                video = manish.get_video(data)
                video_id, mime_type = video["id"], video["mime_type"]
                video_url = manish.query_media_url(video_id)
                video_filename = manish.download_media(video_url, mime_type)
                logger.info(f"{mobile} sent video {video_filename}")
            elif message_type == "audio":
                audio = manish.get_audio(data)
                audio_id, mime_type = audio["id"], audio["mime_type"]
                audio_url = manish.query_media_url(audio_id)
                audio_filename = manish.download_media(audio_url, mime_type)
                logger.info(f"{mobile} sent audio {audio_filename}")
            elif message_type == "document":
                file = manish.get_document(data)
                file_id, mime_type = file["id"], file["mime_type"]
                file_url = manish.query_media_url(file_id)
                file_filename = manish.download_media(file_url, mime_type)
                logger.info(f"{mobile} sent file {file_filename}")
            else:
                logger.info(f"{mobile} sent {message_type} ")
                logger.info(data)
        else:
            delivery = manish.get_delivery(data)
            if delivery:
                logger.info(f"Message : {delivery}")
            else:
                logger.info("No new message")
    return "ok"
```

> The `webhook.py` in the repository still handles documents with `message_type == "file"` and `manish.get_file(data)`. WhatsApp reports documents as type `document`, and `MaNish` has no `get_file` method, so use `get_document` as shown above.

## API reference

All methods live on the `MaNish` class unless noted otherwise. `recipient_id` is always the phone number with country code and without `+`.

### `MaNish(token=None, phone_number_id=None)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `token` | `str` | WhatsApp Cloud API access token (sent as `Authorization: Bearer <token>`) |
| `phone_number_id` | `str` | Phone number ID of the sending number |

Attributes: `base_url` (`https://graph.facebook.com/v15.0`), `url` (`{base_url}/{phone_number_id}/messages`), `headers`.

### Sending

| Method | Parameters (defaults) | Description |
|--------|-----------------------|-------------|
| `send_message` | `message`, `recipient_id`, `recipient_type="individual"`, `preview_url=True` | Text message |
| `reply_to_message` | `message_id`, `recipient_id`, `message`, `preview_url=True` | Text message sent as a reply to `message_id` |
| `send_image` | `image`, `recipient_id`, `recipient_type="individual"`, `caption=None` | Image from URL, local path or media ID |
| `send_video` | `video`, `recipient_id`, `caption=None` | Video from URL, local path or media ID |
| `send_audio` | `audio`, `recipient_id` | Audio from URL, local path or media ID |
| `send_document` | `document`, `recipient_id`, `caption=None` | Document from URL, local path or media ID |
| `send_sticker` | `sticker`, `recipient_id`, `recipient_type="individual"`, `caption=None` | Sticker; local files are converted to WebP (URLs are sent as images) |
| `send_location` | `location` (`Location`), `recipient_id` | Location message |
| `send_contacts` | `contacts` (list of contact dicts), `recipient_id` | Contacts message |
| `send_button` | `button` (JSON string from `ButtonEncoder`), `recipient_id` | Interactive list message |
| `send_template` | `template`, `recipient_id`, `lang="en_US"`, `components={}` | Template message |
| `send_reaction` | `emoji`, `message_id`, `recipient_id`, `recipient_type="individual"` | Emoji reaction to a message |
| `set_status` | `message_id` | Marks a received message as read |

### Media

| Method | Parameters (defaults) | Returns |
|--------|-----------------------|---------|
| `upload_media` | `media` (local file path) | Media ID, or `None` on an API error |
| `query_media_url` | `media_id` | Download URL, or `None` on an API error |
| `download_media` | `media_url`, `mime_type`, `file_path=""` | Path of the saved file (`<file_path>.<ext>` or `temp.<ext>`), or `None` if the file can't be written (for example, the directory doesn't exist) |
| `delete_media` | `media_id` | API response, or `None` on an API error |

### Webhook parsing

Each method takes the parsed webhook JSON (`data`) and reads the first entry/change/message in it.

| Method | Returns |
|--------|---------|
| `changed_field(data)` | The changed field, for example `"messages"` |
| `get_mobile(data)` | Sender's WhatsApp ID (phone number) |
| `get_name(data)` | Sender's profile name |
| `get_message_type(data)` | Message type (`text`, `image`, `video`, `audio`, `document`, `location`, `interactive`, …) |
| `get_message(data)` | Text body of a text message |
| `get_message_id(data)` | Message ID (`wamid...`) |
| `get_message_timestamp(data)` | Message timestamp |
| `get_interactive_response(data)` | The `interactive` object of a list/button reply |
| `get_location(data)` | The `location` object (`latitude`, `longitude`, …) |
| `get_image(data)` / `get_video(data)` / `get_audio(data)` / `get_document(data)` | The media object (`id`, `mime_type`, …) |
| `get_delivery(data)` | Delivery status string (`sent`, `delivered`, `read`, …) from a status update |
| `preprocess(data)` | Internal: returns `data["entry"][0]["changes"][0]["value"]` |

### Helper classes

| Module | Class | Constructor |
|--------|-------|-------------|
| `manish.location` | `Location` | `Location(name=None, address=None, latitude=None, longitude=None)`; geocodes `address` when `latitude` or `longitude` is missing |
| `manish.contact` | `Contact` | `Contact(name, addresses=[], emails=[], phones=[])` |
| | `Name` | `Name(formatted_name, first_name="", last_name="", middle_name="", suffix="", prefix="")` |
| | `Phone` | `Phone(phone="", type="", wa_id="")` |
| | `Email` | `Email(email="", type="")` |
| | `Address` | `Address(street="", city="", state="", zip="", country="", country_code="", type="")` |
| | `Url` | `Url(url="", type="")` |
| | `ContactEncoder` | JSON encoder for the classes above |
| `manish.button` | `Row` | `Row(id, title, description)` |
| | `Section` | `Section(title, rows)` |
| | `Action` | `Action(button, sections)` |
| | `Button` | `Button(header, body, footer, action)` |
| | `ButtonEncoder` | JSON encoder for the classes above |
| `manish.template` | `Parameter` | `Parameter(type, text)` |
| | `Currency` | `Currency(fallback_value, code, amount_1000)` |
| | `CurrencyParameter` | `CurrencyParameter(type, currency)` |
| | `Media` | `Media(id="", link="")` |
| | `MediaParameter` | `MediaParameter(type, image)` |
| | `Component` | `Component(type, parameters)` |
| | `Components` | `Components(components)` |
| | `TemplateEncoder` | JSON encoder for the classes above |

`Url` is defined but is not part of `Contact`'s constructor.

## Error handling

Most methods do not raise exceptions for API errors, but the behaviour differs by method group.

**Send and media methods** (`send_*`, `reply_to_message`, `set_status`, `upload_media`, `query_media_url`, `download_media`, `delete_media`):

* On success, the send methods return the parsed JSON response from the Graph API (a `dict` that contains the message ID).
* On an API error (HTTP status other than 200), the send methods log the status and response, and return the parsed error response (also a `dict`, with an `error` key). `set_status` returns `None` instead; `upload_media`, `query_media_url` and `delete_media` also return `None`.
* If an exception is raised (network error, missing file, …), it is logged and a **string** like `'{"error":"..."}'` is returned.

**Webhook parsing methods:**

* Most of them (`get_name`, `get_message`, `get_message_id`, `get_message_timestamp`, `get_location`, `get_image`, `get_video`, `get_audio`, `get_message_type`, `get_delivery`, `changed_field`) log the exception and return `None`.
* `get_interactive_response` returns the `'{"error":"..."}'` string instead.
* `get_mobile` and `get_document` have no exception handling, so a malformed payload raises (for example `IndexError` or `KeyError`).

**`Location(...)`** raises `AttributeError` in its constructor when the address can't be geocoded.

Check the result before relying on it:

```python
result = manish.send_message("Hello", "97250xxxxxxx")
if not isinstance(result, dict) or "error" in result:
    print("Sending failed:", result)
```

All logging goes through [Loguru](https://github.com/Delgan/loguru).

## Usage statistics

Every time a `MaNish` object is created, the library sends an anonymous HTTP `GET` request to a pixel on `analytics.techblog.co.il` to count usage. The request carries no message data, token or phone number, but the analytics server does see your IP address and user agent. There is currently no option to turn it off; block the host if your environment requires that. The request has no timeout, so if you block it by silently dropping packets, every `MaNish()` call will hang. Block it at the DNS level or with a firewall rule that rejects the connection instead.

## Security notes

* **Access token:** treat it like a password. Load it from environment variables or a secrets manager, never commit it, and prefer a System User token with only the permissions you need. Rotate it if it leaks.
* **`.env` file:** the repository contains a committed `.env` with empty `VERIFY_TOKEN`, `TOKEN` and `PHONE_NUMBER_ID` entries as a template. Don't put real values into a tracked `.env` file.
* **Verify token:** choose a long, random `VERIFY_TOKEN`. It is only used during the webhook subscription handshake.
* **Webhook signatures:** neither the library nor `webhook.py` checks the `X-Hub-Signature-256` header that Meta signs with your app secret. If you expose a webhook publicly, validate that signature before trusting the payload.
* **Downloaded media:** `download_media` writes files to disk (by default `temp.<ext>` in the current directory). Treat files received from users as untrusted.
* Serve the webhook over HTTPS only.

## Troubleshooting

* **Messages other than templates are not delivered:** the 24-hour customer service window is closed. Send a template message first, or wait for the user to message you.
* **`(#131030) Recipient phone number not in allowed list`:** with the test number, you can only message recipients you added and verified (up to 5).
* **Authentication errors after a day:** the temporary access token from the Getting started page expires after 24 hours. Generate a permanent token.
* **Webhook verification fails:** make sure `VERIFY_TOKEN` matches the value entered in the Meta app, and that the callback URL is publicly reachable over HTTPS.
* **`Location(address=...)` raises `AttributeError`:** the address could not be geocoded by Nominatim, so the constructor fails before anything is sent. Pass `latitude` and `longitude` instead.
* **A local sticker in a subdirectory fails to send, or a file named like `('img2', '.png').webp` appears:** this comes from the WebP conversion; see the notes in [Sending a sticker](#sending-a-sticker). Upload a WebP file with `upload_media` and send its media ID instead.
* **A `temp/` directory appears:** sending a local sticker creates `./temp` in the current working directory.

## Development

```bash
git clone https://github.com/t0mer/ma-nish
cd ma-nish
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
pip install -r requirements-dev.txt   # pylint, mypy, black
```

Project layout:

```
manish/
  __init__.py   # MaNish class: sending, media and webhook parsing
  button.py     # Row, Section, Action, Button, ButtonEncoder
  contact.py    # Contact, Name, Phone, Email, Address, Url, ContactEncoder
  helpers.py    # WebP conversion and file download helpers
  location.py   # Location (with geopy geocoding), LocationEncoder
  template.py   # Template parameters, components and TemplateEncoder
webhook.py      # FastAPI webhook example
screenshots/    # Setup guide screenshots
```

There is no automated test suite. Releases are published to PyPI by the [Publish pypi package](https://github.com/t0mer/ma-nish/blob/main/.github/workflows/python-publish.yml) workflow when a GitHub release is published (or when the workflow is run manually). The package version is set in `setup.py`.

## Contributing

Issues and pull requests are welcome at [github.com/t0mer/ma-nish](https://github.com/t0mer/ma-nish). Please describe the change, and include an example of the WhatsApp payload involved when fixing webhook parsing.

## License

manish is released under the [MIT License](https://github.com/t0mer/ma-nish/blob/main/LICENSE). Copyright (c) 2022 Tomer Klein.
