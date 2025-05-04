import os
import threading
import speech_recognition as sr
from flask import Flask, render_template, jsonify, request
import google.generativeai as genai
from speak import speak_text  # Yeni eklenen satır

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

#chd
def generate_smart_reply(question):
    # Zorluk seviyesini tahmin et
    eval_prompt = f"Soru: \"{question}\"\nBu soru karmaşık mı? Eğer öyleyse 'ZOR' yaz, değilse 'KOLAY' yaz."
    eval = model.generate_content(eval_prompt).text.strip().upper()

    if "ZOR" in eval:
        # Chain of Draft uygula
        draft_prompt = f"Soruya cevap vermeden önce düşünce taslağı üret.\nSoru: {question}\nTaslak:"
        draft = model.generate_content(draft_prompt).text

        final_prompt = f"""Aşağıda bir soru ve bu soruya yönelik bir düşünce taslağı verilmiştir.
Bu taslağı kullanarak açık, net ve mantıklı bir nihai cevap üret.

Soru: {question}

Taslak:
{draft}

Nihai cevap:"""
        answer = model.generate_content(final_prompt).text.strip()
    else:
        # Basit soru, direkt cevap
        full_prompt = f"{system_prompt}\nKullanıcı: {question}"
        answer = model.generate_content([{"role": "user", "parts": [full_prompt]}]).text.strip()

    return answer


#chd


with microphone as source:
    print("🔧 Kalibrasyon yapılıyor...")
    recognizer.adjust_for_ambient_noise(source, duration=2)

def play_audio(filename):
    if os.name == 'nt':
        os.system(f'start {filename}')
    else:
        os.system(f'mpg123 {filename}')  # Linux için mp3 çalıcı komutu

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
            answer = generate_smart_reply(user_input)


            print("🤖 AKÜBOT:", answer)

            # XTTS ile ses üret ve çal
            output_path = speak_text(answer, output_path="static/output.wav")
            play_audio(output_path)

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
