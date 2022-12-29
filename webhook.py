import io
import os
import sys
import json
import uvicorn
from loguru import logger
from manish import MaNish
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse


app = FastAPI()
load_dotenv()
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
manish = MaNish(os.getenv("TOKEN"), phone_number_id=os.getenv("PHONE_NUMBER_ID"))


@app.get("/", include_in_schema=False)
async def verify(request: Request):
    if request.query_params.get('hub.mode') == "subscribe" and request.query_params.get("hub.challenge"):
        if not request.query_params.get('hub.verify_token') == VERIFY_TOKEN: #os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return int(request.query_params.get('hub.challenge'))
    return "Hello world", 200



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
                name = manish.get_name(data)
                logger.info("Message: %s", message)
                manish.send_message(f"Hi {name}, nice to connect with you", mobile)

            elif message_type == "interactive":
                message_response = manish.get_interactive_response(data)
                intractive_type = message_response.get("type")
                message_id = message_response[intractive_type]["id"]
                message_text = message_response[intractive_type]["title"]
                logger.info(f"Interactive Message; {message_id}: {message_text}")

            elif message_type == "location":
                message_location = manish.get_location(data)
                message_latitude = message_location["latitude"]
                message_longitude = message_location["longitude"]
                logger.info("Location: %s, %s", message_latitude, message_longitude)

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
                
            elif message_type == "file":
                file = manish.get_file(data)
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

if __name__ == '__main__':
    logger.info("Whatsapp Webhook is up and running")
    uvicorn.run(app, host="0.0.0.0", port=7020)