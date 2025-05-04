# speaker.py

from TTS.api import TTS
import torch
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsAudioConfig, XttsArgs
from TTS.config.shared_configs import BaseDatasetConfig

# Güvenli serileştirme için gerekli sınıflar
torch.serialization.add_safe_globals([
    XttsConfig,
    XttsAudioConfig,
    BaseDatasetConfig,
    XttsArgs
])

# TTS modeli yükleniyor
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False, gpu=False)

def speak_text(text, output_path="static/output.wav", speaker_path="static/female.wav", lang="tr"):
    """
    Verilen metni sese çevirip bir dosyaya kaydeder.
    """
    tts.tts_to_file(
        text=text,
        file_path=output_path,
        speaker_wav=speaker_path,
        language=lang
    )
    return output_path
