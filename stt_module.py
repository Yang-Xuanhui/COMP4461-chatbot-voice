import speech_recognition as sr # requirement: pyaudio
# for mac users: brew install portaudio, then pip install pyaudio

# Initialize recognizer class (for recognizing the speech)
recognizer = sr.Recognizer()

# Reading Microphone as source
with sr.Microphone() as source:
    print("Talk")
    audio = recognizer.listen(source, timeout=20)

    # recoginze_() method will throw a request error if the API is unreachable,
    # hence using exception handling
    try:
        # Using google speech recognition
        print("Text: "+recognizer.recognize_google(audio, language='en-US'))
        print("Text: "+recognizer.recognize_google(audio, language='zh-CN'))
        # print("Text: "+recognizer.recognize_google(audio, language='zh-HK'))
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.WaitTimeoutError:
        print("Listening timed out while waiting for phrase to start")