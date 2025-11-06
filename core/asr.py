# core/asr.py

import speech_recognition as sr
import pyaudio
import wave
import os
import whisper

# Настройки записи
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Whisper рекомендует 16kHz
RECORD_SECONDS = 5
TEMP_AUDIO_FILE = "temp/recording.wav"

# Глобальная переменная для модели (загружаем один раз)
_model = None

def get_whisper_model(model_name="small"):
    """Загружает модель Whisper один раз и кэширует её."""
    global _model
    if _model is None:
        print("Загрузка модели Whisper... (это займёт 10–30 секунд)")
        _model = whisper.load_model(model_name)
    return _model

def record_audio_to_file(filename=TEMP_AUDIO_FILE):
    """Записывает аудио с микрофона в WAV-файл (16kHz для Whisper)."""
    p = pyaudio.PyAudio()

    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    print("🎤 Говорите...")
    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("✅ Запись завершена")

    stream.stop_stream()
    stream.close()
    p.terminate()

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return filename

def transcribe_from_microphone():
    """Записывает речь и распознаёт её через Whisper (оффлайн, русский)."""
    audio_file = record_audio_to_file()
    
    try:
        model = get_whisper_model("small")  # small — баланс скорости и точности
        result = model.transcribe(audio_file, language="ru")
        return result["text"].strip()
    except Exception as e:
        return f"Ошибка Whisper: {e}"