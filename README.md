# manish
WhatsApp has now opened up its API so you no longer have to go through a partner to send and receive WhatsApp messages!
MaNish is an Unofficial python wrapper to [WhatsApp Cloud API](https://developers.facebook.com/docs/whatsapp/cloud-api)

## Features supported
1. Sending Messages
2. Sending Media (images, audio, video and documents)
3. Sending Stickers
3. Sending Location
4. Sending Contacts
5. Sending Buttons
6. Sending Template messages
7. Parsing messages and media received (Webhook)

## Components and Frameworks used in Voicy
* [Loguru](https://pypi.org/project/loguru/)
* [Requests ](https://pypi.org/project/requests/)
* [requests-toolbelt](https://pypi.org/project/requests-toolbelt/)
* [python-dotenv](https://pypi.org/project/python-dotenv/)
* [validators](https://pypi.org/project/validators/)
* [geopy](https://pypi.org/project/geopy/)
* [Pillow](https://pypi.org/project/Pillow/)
* [Uvicorn](https://pypi.org/project/uvicorn/)
* [fastapi](https://pypi.org/project/fastapi/)
* [jinja2](https://pypi.org/project/Jinja/)


## Limitations
* 1000 free messages per month (Free tier)
* It is only possible to send messages other than templates after the target phone responds to an initial message (Unless you use Template messages)
* You can't send message to a group


## Getting started
To get started with **manish**, you have to firstly install the libary either directly or using *pip*.

### Installation from source

Use git to clone or you can also manually download the project repository just as shown below;

```bash
$ git clone https://github.com/t0mer/ma-nish/
$ cd heyoo
heyoo $ python setup.py install 
```

### Installing from PyPi

```bash
# For Windows 

pip install  --upgrade manish

#For Linux | MAC 

pip3 install --upgrade manish
```


## Setting up the environment
### Set Up Meta App

First you’ll need to follow the (instructions on this page)[https://developers.facebook.com/docs/whatsapp/cloud-api/get-started] to:

* Register as a Meta Developer
* Enable two-factor authentication for your account
* Create a Meta App – you need to create a Business App for WhatsApp

Once you’ve done that, go to your app and set up the WhatsApp product.

[![New app](https://techblog.co.il/wp-content/uploads/2022/12/new-app.png "New App")](https://techblog.co.il/wp-content/uploads/2022/12/new-app.png "New App")

You’ll be given a temporary access token and a Phone Number ID, note these down as you’ll need them later. Set up your own phone number as a recipient and you can have a go at sending yourself a test message:

[![Getting started](https://techblog.co.il/wp-content/uploads/2022/12/test-number.png "Getting started")](https://techblog.co.il/wp-content/uploads/2022/12/test-number.png "Getting started")

### Set Up Message Template

In the test message above, you used the **hello_world** template. You’ll need to set up your own template for your own purposes. If you go to [“Message Templates”](https://business.facebook.com/wa/manage/message-templates/) in the WhatsApp manager you can build your own templates.

In the following example, i created a template for my smat home. The template header if fixed and so is the footer. in the body i added variable for dynamic text:

[![Smart Home Template](https://techblog.co.il/wp-content/uploads/2022/12/my-template.png "Smart Home Template")](https://techblog.co.il/wp-content/uploads/2022/12/my-template.png "Smart Home Template")


Once you're done with the above ,you're ready to start send messages using **manish**.

## Authentication
Before you can send messages, you need to authenticate your application using the **```phone_number_id```** and **```Token```** of your test number.

```python
>>> from manish import MaNish
>>> manish = MaNish('TOKEN',  phone_number_id='xxxxxxxxxx')
```

One your app is authenticated, you can start sending messages.
As mentioned above, it is only possible to send messages other than templates after the target phone responds to an initial message.

## Sending Messanges

This method can be used for sending simple text messages.

```python
>>> manish.send_message(
        message='Your message',
        recipient_id='97250xxxxxxx'
     )
```
***Mobile should include country code without the + symbol***

## Sending Media
When sending media:
* Images
* Video
* Audio
* Document
* Gif

You can either specify:
* URL for the media.
* Local file.

## Sending Image

```python
>>> manish.send_image(
        image="https://i.imgur.com/COXQuEz.jpeg",
        recipient_id="97250xxxxxxx",
    )
```

## Sending Video
```python

>>> manish.send_video(
        video="https://user-images.githubusercontent.com/4478920/200173402-8a8343c3-afc2-4341-86ea-c833bed98a9a.mp4",
        recipient_id="97250xxxxxxx",
    )
```

## Sending Audio

```python
>>> manish.send_audio(
        audio="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-9.mp3",
        recipient_id="97250xxxxxxx",
    )
```

## Sending Document

```python
>>> messenger.send_document(
        document="https://www.africau.edu/images/default/sample.pdf",
        recipient_id="97250xxxxxxx",
    )
```

## Sending Sticker
Cloud API: Static and animated third-party outbound stickers are supported in addition to all types of inbound stickers. A static sticker needs to be 512x512 pixels and cannot exceed 100 KB. An animated sticker must be 512x512 pixels and cannot exceed 500 KB.

When sending from local file, the app will automatically convert the image to the supported format.


```python
>>> manish.send_sticker(
        image="https://i.imgur.com/COXQuEz.webp",
        recipient_id="97250xxxxxxx",
    )
```

## Sending Location
The Location message object requires **longitude** and **latitude**, but you can also send real address and manish will translate the address to coordinates and send thr message.

```python
>>> from manish.location import *
>>> location = Location(address="10 Hagalil street, raanana",name="Home")
>>> manish.send_location(location = location,recipient_id="97250xxxxxxx")

```

## Sending Contact(s)
```python
>>> from manish.contact import *
>>> phones = [Phone(phone="97250xxxxxxx",type="CELL")]
>>> name = Name(formatted_name="Tomer Klein", first_name="Tomer", last_name="Klein")
>>> addresses = [Address(street="Hagalil 10", city="Raanana", zip ="123456", country="Israel")]
>>> emails = [Email("jhon.c@gmail.com")]
>>> contact = Contact(name=name,addresses=addresses,emails=emails,phones=phones)
>>> data = ContactEncoder().encode([contact])
>>> manish.send_contacts(data,"97250xxxxxxx")

```

## Sending Button(s)
```python
>>> from manish.button import *
>>> rows = []
>>> rows.append(Row("row 1","Send Mony",""))
>>> rows.append(Row("row 2","Withdraw Mony",""))
>>> sections = []
>>> sections.append(Section("iBank",rows))
>>> action = Action("Button Testing",sections)
>>> button = Button("Header Testing", "Body Testing", "Footer Testing",action)
>>> data = ButtonEncoder().encode(button)
>>> manish.send_button(data,"97250xxxxxxx")
```

## Sending Template Messages
This method allows you to send template based messages (and bypass the limitation of the ability to send message outside the 24 hours window).

Template messages can either be:
* Text Template (Can also include currency object)
* Media Template (Same as Text but with media in the header)

### Sending simple text template
```python
>>> from manish.template import *
>>> def send_template():
>>> parameter = Parameter(type="text",text = "Your Text Message")
>>> parameters = []
>>> parameters.append(parameter)
>>> body = Component(type="body",parameters=[parameter])
>>> manish.send_template(components=TemplateEncoder().encode([body]),recipient_id="97250xxxxxxx",template="smart_home_media",lang="he")
```

### Sending media template
**Media can only be attached to the header!**
```python
>>> parameter = Parameter(type="text",text = "Your Text Message")
>>> img = Media(link="https://raw.githubusercontent.com/t0mer/broadlinkmanager-docker/master/screenshots/Devices%20List.png")
>>> iparam = MediaParameter(type="image",image=img)
>>> parameters = []
>>> parameters.append(parameter)
>>> body = Component(type="body",parameters=[parameter])
>>> header = Component(type="header",parameters=[iparam])
>>> manish.send_template(components=TemplateEncoder().encode([body,header]),recipient_id="97250xxxxxxx",template="smart_home_media",lang="he")
```