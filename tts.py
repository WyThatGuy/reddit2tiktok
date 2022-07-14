from gtts import gTTS


text = input("Text to say: ")
tts = gTTS(text)
tts.save('recording.mp3')
print('Text Converted')