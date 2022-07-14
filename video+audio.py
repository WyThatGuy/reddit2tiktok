from gtts import gTTS
import moviepy.editor as mpe
from mutagen.mp3 import MP3
import os
from numpy import concatenate
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager as CM
from time import sleep
import urllib.request
import json
from PIL import Image
import praw

# Comments can be up to ~35 seconds

# Variables:
fromTop = 1 # The post number after the top post
url = 'https://reddit.com/r/askreddit/hot.json' # Replace askreddit with whatever subreddit you want
clientID = "" # https://praw.readthedocs.io/en/stable/getting_started/quick_start.html
clientSecret = "" # https://praw.readthedocs.io/en/stable/getting_started/quick_start.html
userAgent = "Comment Extractor by /u/wywessels" # What you are doing and your username
maxCom = 20 # The amount of comments to pull
audioLength = 35 # The length of your background video in seconds
bckgName = 'loop.mp4' # The name of your background video
otpName = 'out.mp4' # The name of the outputted file

# Delete old files
if os.path.exists(otpName):
    os.remove(otpName)
if os.path.exists('screenshot.png'):
    os.remove('screenshot.png')

# Get reddit link
page = urllib.request.urlopen(url)
content = json.loads(page.read())
redditURL = content['data']['children'][fromTop]['data']['url']
redditTitle = content['data']['children'][fromTop]['data']['title']

# Get reddit screenshot
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get(redditURL)
sleep(1)
try:
    clickable = driver.find_element_by_class_name('i2sTp1duDdXdwoKi1l8ED')
    ActionChains(driver)\
        .click(clickable)\
        .perform()
except Exception:
    pass
sleep(2)
driver.get_screenshot_as_file("screenshot.png")
driver.quit()

# Crop image
im = Image.open('screenshot.png')
im = im.crop((26, 240, 888, 440))
im.save('screenshot.png')

# Pull Comments
reddit = praw.Reddit(
    client_id=clientID,
    client_secret=clientSecret,
    user_agent=userAgent
)

comments = []

submission = reddit.submission(url=redditURL+'?sort=top')

from praw.models import MoreComments

for top_level_comment in submission.comments:
    if len(comments) > maxCom:
        break
    if isinstance(top_level_comment, MoreComments):
        continue
    comments = comments + [top_level_comment.body]

# Make audio files
text = [redditTitle] + comments
spokenText = []
titleLength = 5
c = 0
length = 0
for x in text:
    tts = gTTS(x)
    try:
        tts.save(str(x).replace('/', '').replace('<', '').replace('>', '').replace('"', '').replace('|', '').replace(':', '').replace('?', '').replace('*', '').replace("\\", '')[:15] + '.mp3')
        length += MP3(str(x).replace('/', '').replace('<', '').replace('>', '').replace('"', '').replace('|', '').replace(':', '').replace('?', '').replace('*', '').replace("\\", '')[:15] + '.mp3').info.length
        if c == 0:
            titleLength = length
            c = 1
        if length < audioLength:
            spokenText += [[str(x), MP3(str(x).replace('/', '').replace('<', '').replace('>', '').replace('"', '').replace('|', '').replace(':', '').replace('?', '').replace('*', '').replace("\\", '')[:15] + '.mp3').info.length]]
            print('Text Converted')
            print('Length: ' + str(length))
        else:
            length -= MP3(str(x).replace('/', '').replace('<', '').replace('>', '').replace('"', '').replace('|', '').replace(':', '').replace('?', '').replace('*', '').replace("\\", '')[:15] + '.mp3').info.length
            os.remove(str(x).replace('/', '').replace('<', '').replace('>', '').replace('"', '').replace('|', '').replace(':', '').replace('?', '').replace('*', '').replace("\\", '')[:15] + '.mp3')
    except Exception:
        pass

# Combine audio w/ video
clips = []
for x in text:
    try:
        clips += [mpe.AudioFileClip(str(x).replace('/', '').replace('<', '').replace('>', '').replace('"', '').replace('|', '').replace(':', '').replace('?', '').replace('*', '').replace("\\", '')[:15] + '.mp3')]
    except Exception:
        pass
audio = mpe.concatenate_audioclips(clips)
clip = mpe.VideoFileClip(bckgName)
video = clip.set_audio(audio)
video.write_videofile(otpName)

# Delete audio file
for x in text:
    if os.path.exists(str(x).replace('/', '').replace('<', '').replace('>', '').replace('"', '').replace('|', '').replace(':', '').replace('?', '').replace('*', '').replace("\\", '')[:15] + '.mp3'):
        os.remove(str(x).replace('/', '').replace('<', '').replace('>', '').replace('"', '').replace('|', '').replace(':', '').replace('?', '').replace('*', '').replace("\\", '')[:15] + '.mp3')

clip = mpe.VideoFileClip(otpName)

cat = (mpe.ImageClip("screenshot.png")
                .resize(0.70)
                .set_start(0)
                .set_duration(titleLength)
                .set_position(("center", "center")))

clip = mpe.CompositeVideoClip([clip, cat])

clip.write_videofile("out1.mp4")

os.remove(otpName)
os.rename("out1.mp4", otpName)

# Make text overlay
clip = mpe.VideoClip()
y = 0
for x in spokenText:
    o = 0
    txt = ''
    for w in x[0].split(' '):
        if o % 5 == 0:
            txt += '\n'
        txt += w + " " 
        o += 1
    textClip = mpe.TextClip(txt, fontsize = 30, color = 'black').set_position(('center', 'center')).set_duration(spokenText[y][1])
    if y < 2:
        clip = textClip
    else:
        clip = mpe.concatenate_videoclips([clip, textClip]).set_position(('center', 'center')).set_start(spokenText[0][1])
    y += 1

clip = mpe.CompositeVideoClip([mpe.VideoFileClip(otpName), clip])

clip.write_videofile("out1.mp4")

os.remove(otpName)
os.rename("out1.mp4", otpName)