import os
import threading
import speech_recognition as sr
from gtts import gTTS
import google.generativeai as genai
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

status = "Hazır"
listening = False
listener_thread = None

# Google Gemini ayarı
genai.configure(api_key="AIzaSyBRtVTPJdhPG-G-ywr96_niK-R6CSJeSI0")
model = genai.GenerativeModel("gemini-2.0-flash")
system_prompt = """Sen bir sanal asistansın doğru cevaplar ver çok uzatma."""

recognizer = sr.Recognizer()
microphone = sr.Microphone()

with microphone as source:
    print("🔧 Kalibrasyon yapılıyor...")
    recognizer.adjust_for_ambient_noise(source, duration=2)

def play_audio(filename):
    if os.name == 'nt':
        os.system(f'start {filename}')
    else:
        os.system(f'mpg123 {filename}')

def recognize_and_respond():
    global status, listening
    while listening:
        with microphone as source:
            status = "Dinliyor"
            print("🎙️ Dinleniyor...")
            audio = recognizer.listen(source, phrase_time_limit=10)

        try:
            user_input = recognizer.recognize_google(audio, language="tr-TR")
            print(f"👤 Siz: {user_input}")

            if user_input.lower() in ["çık", "kapat", "görüşürüz", "bitir"]:
                status = "Durduruldu"
                listening = False
                break

            status = "Yanıtlanıyor"
            prompt = f"{system_prompt}\nKullanıcı: {user_input}"
            response = model.generate_content([{"role": "user", "parts": [prompt]}])
            answer = response.text.strip()

            print("🤖 AKÜBOT:", answer)
            tts = gTTS(text=answer, lang='tr',slow=False)
            tts.save("answer.mp3")
            play_audio("answer.mp3")
            status = "Hazır"

        except sr.UnknownValueError:
            print("❓ Anlaşılamadı.")
            status = "Anlaşılamadı"
        except sr.RequestError:
            print("🚫 STT hatası")
            status = "STT Hatası"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/status")
def get_status():
    return jsonify({"status": status})

@app.route("/start", methods=["POST"])
def start_listening():
    global listening, listener_thread, status
    if not listening:
        listening = True
        listener_thread = threading.Thread(target=recognize_and_respond)
        listener_thread.start()
        status = "Başlatıldı"
    return jsonify({"message": "Dinleme başlatıldı."})

@app.route("/stop", methods=["POST"])
def stop_listening():
    global listening, status
    listening = False
    status = "Durduruldu"
    return jsonify({"message": "Dinleme durduruldu."})

if __name__ == "__main__":
    app.run(debug=True)