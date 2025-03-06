import pyttsx3 # https://pypi.org/project/pyttsx3/

engine = pyttsx3.init()

# Get the list of voices
voices = engine.getProperty('voices')
for voice in voices:
    print(f"Voice ID: {voice.id}")
    print(f"Name: {voice.name}")
    print(f"Gender: {voice.gender}")
    print(f"Language: {voice.languages}\n")   


engine.setProperty('rate', 150)  # Speech rate
engine.setProperty('volume', 1)  # Volume level 0.0 to 1.0
engine.setProperty('voice','com.apple.speech.synthesis.voice.Alex')
engine.say("Hello, I am your voice assistant.")

engine.setProperty('voice','com.apple.voice.compact.zh-CN.Tingting')
engine.say("你好，我是你的语音助手。")

engine.setProperty('voice','com.apple.voice.compact.zh-HK.Sinji')
engine.say("你好，我係你嘅語音助手。")

engine.runAndWait()


