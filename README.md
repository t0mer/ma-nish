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
