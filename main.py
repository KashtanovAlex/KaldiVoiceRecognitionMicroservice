from vosk import Model, KaldiRecognizer
import speech_recognition
import wave
import json
import os
from threading import Thread
import socket


def record_and_recognize_audio(*args: tuple):
    with microphone:
        recognized_data = ""


        recognizer.adjust_for_ambient_noise(microphone, duration=0)

        try:
            print("Listening...")
            audio = recognizer.listen(microphone, 5, 5)

            with open("microphone-results.wav", "wb") as file:
                file.write(audio.get_wav_data())

        except speech_recognition.WaitTimeoutError:
            print("Can you check if your microphone is on, please?")
            return


        try:
            print("Started recognition...")
            recognized_data = recognizer.recognize_google(audio, language="ru").lower()

        except speech_recognition.UnknownValueError:
            pass

        except speech_recognition.RequestError:
            print("Trying to use offline recognition...")
            recognized_data = use_offline_recognition()

        return recognized_data


def use_offline_recognition():
    recognized_data = ""

    if not os.path.exists("models/vosk-model-small-ru-0.4"):
        print("Please download the model from:\n"
                  "https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit(1)

    wave_audio_file = wave.open("microphone-results.wav", "rb")
    model = Model("models/vosk-model-small-ru-0.4")
    offline_recognizer = KaldiRecognizer(model, wave_audio_file.getframerate())

    data = wave_audio_file.readframes(wave_audio_file.getnframes())
    if len(data) > 0:
        if offline_recognizer.AcceptWaveform(data):
            recognized_data = offline_recognizer.Result()


            recognized_data = json.loads(recognized_data)
            recognized_data = recognized_data["text"]

    print(recognized_data)
    return recognized_data


if __name__ == "__main__":

    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()
    sock = socket.socket()
    sock.connect(('localhost', 1488))

    while True:
        voice_input = record_and_recognize_audio()
        print(voice_input)
        a = voice_input.encode(encoding="utf-8", errors="strict")
        sock.send(a)
