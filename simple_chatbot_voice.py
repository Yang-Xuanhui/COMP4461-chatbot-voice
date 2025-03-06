import streamlit as st
from openai import AzureOpenAI
import pyttsx3
import speech_recognition as sr
import threading

model_name = "gpt-35-turbo"

# STT
def speech_to_text():
    recognizer = sr.Recognizer()                                    # Initialize recognizer class (for recognizing the speech)
    with sr.Microphone() as source:
        st.info("Listening... Speak now.")
        try:
            audio = recognizer.listen(source, timeout=5)            # Reading Microphone as source
            st.success("Processing your voice...")
            return recognizer.recognize_google(audio)               # Using google speech recognition
        except sr.UnknownValueError:
            st.error("Unknown Value Error")
        except sr.RequestError:
            st.error("Request Error from Google Speech Recognition")
        except sr.WaitTimeoutError:
            st.warning("Wait Timeout Error. No speech detected")
    return None


# Initialize TTS engine
tts_engine = pyttsx3.init() 
tts_engine.setProperty('rate', 150)      # set speech property
# TTS
def text_to_speech(text):
    tts_engine.say(text)
    tts_engine.runAndWait()              # Run and wait for the speech to finish
    if tts_engine._inLoop:               # End the loop (keep the engine running will cause runtime error)
        tts_engine.endLoop()

# Use OpenAI API
def chat_with_openai():
    try:
        # setting up the OpenAI model
        client = AzureOpenAI(
            api_key=openai_api_key,
            api_version="2023-12-01-preview",
            azure_endpoint="https://hkust.azure-api.net/",
        )
        response = client.chat.completions.create(
            model=model_name,
            messages=st.session_state.messages
        )
        msg = response.choices[0].message.content
        return msg
    except Exception as e:
        st.error(f"Error: {e}")
        return "I encountered an issue. Please try again later."

def handle_user_input(prompt):
    if not openai_api_key:
        st.info("Please add your Azure OpenAI API key to continue.")
        st.stop()
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    msg = chat_with_openai()
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
    return msg

# Streamlit UI
with st.sidebar:
    openai_api_key = st.text_input("Azure OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an Azure OpenAI API key](https://itsc.hkust.edu.hk/services/it-infrastructure/azure-openai-api-service)"

st.title("🎙️ Voice Chat Agent")

# Input options
input_option = st.radio("Choose Input Method", ("Voice", "Text"))

if "messages" not in st.session_state:
    greeting = "How can I help you?"
    st.session_state["messages"] = [{"role": "assistant", "content": greeting}]
    text_to_speech(greeting)

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if input_option == "Voice":
    st.write("Click the button below and start speaking.")
    if st.button("Speak"):
        if prompt := speech_to_text():
            msg = handle_user_input(prompt)
            text_to_speech(msg)
else:
    if prompt := st.chat_input():
        msg = handle_user_input(prompt)
        if st.button("Hear the Response"):
            text_to_speech(msg)
        