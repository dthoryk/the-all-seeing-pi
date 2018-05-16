from gpiozero import Button
from picamera import PiCamera
from time import gmtime, strftime
from overlay_functions import *
from guizero import App, PushButton, Text, Picture
from twython import Twython
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
    )


def next_overlay():
    global overlay
    overlay = next(all_overlays)
    preview_overlay(camera,overlay)
    
def take_picture():
    global output
    output = strftime("/home/pi/photoBooth/images/image-%d-%m %H:%M.png",gmtime()) 
    camera.capture(output)
    camera.stop_preview()
    remove_overlays(camera)
    output_overlay(output,overlay)
    size = 400,400
    gif_img = Image.open(output)
    gif_img.thumbnail(size, Image.ANTIALIAS)
    gif_img.save(latest_photo, 'gif')
    
    your_pic.value = latest_photo

def new_picture():
    #camera.start_preview(alpha=128)
    camera.start_preview()
    preview_overlay(camera, overlay)

def send_tweet():
    twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
    )

    message = "CNY Regional Making and Innovation Conference #cnymakers18"
    with open(output, 'rb') as photo:
        image = twitter.upload_media(media=photo)
        twitter.update_status(status=message,media_ids=[image['media_id']])

pictureCount = 0

    
next_overlay_btn = Button(23)
take_pic_btn = Button(25)

next_overlay_btn.when_pressed = next_overlay
take_pic_btn.when_pressed = take_picture

camera = PiCamera()
camera.resolution = (800,480)
camera.hflip = True
camera.start_preview(alpha=128)


output = ""

latest_photo = '/home/pi/photoBooth/latest.gif'


app = App("Library Photo Booth", 800,480)
message = Text(app, "Post A Picture On Our Twitter Page!")
your_pic = Picture(app, latest_photo)

new_pic = PushButton(app, new_picture, text="New picture")

tweet_pic = PushButton(app, send_tweet, text="Tweet Picture")
app.display()


