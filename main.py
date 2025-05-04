import google.generativeai as genai
from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()


# Türkçe ses seçimi
voice = texttospeech.VoiceSelectionParams(
    language_code="tr-TR",
    ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
)

# Ses özellikleri (sesli yanıtın hızı ve tonunu ayarlayabilirsiniz)
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)


# API anahtarını buraya yaz (Google AI Studio üzerinden alınıyor)
genai.configure(api_key="AIzaSyBRtVTPJdhPG-G-ywr96_niK-R6CSJeSI0")

model = genai.GenerativeModel("gemini-2.0-flash")

# Modelin davranışını kontrol eden metin
system_prompt = "Sen kısa ve öz yanıt veren bir asistansın, adın AKÜBOT."


while True:
    ask_text = input(": ")
    # Kullanıcıdan gelen soru ile birlikte system prompt'u da ekliyoruz
    prompt = system_prompt + "\nKullanıcı: " + ask_text
    
    response = model.generate_content([{"role": "user", "parts": [prompt]}])
    print("Gemini:", response.text)

    #tts ile sesli yanıt 
    synthesis_input = texttospeech.SynthesisInput(text=response.text)

        # Sentezleme
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
