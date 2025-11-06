# main.py
from core.asr import transcribe_from_microphone

if __name__ == "__main__":
    text = transcribe_from_microphone()
    print ("Асистент:", text)