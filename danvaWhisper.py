import openai
import requests
import json
import sounddevice as sd
import soundfile as sf
import os
import pyttsx3
import time
import voicerss_tts

# configuración de credenciales
openai.api_key = "your_api_key"
voicerss_api_key = "your_api_key"

# Función para transformar audio en texto usando Whisper Mode
def transformar_audio_texto(audio_data):
    url = "https://api.openai.com/v1/whisper"
    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "audio": audio_data,
        "config": {
            "language_code": "es-ES"
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    response_data = response.json()
    return response_data['text']

# Función para hablar usando VoiceRSS Text-to-Speech API
def hablar(texto):
    voice = voicerss_tts.Speech({
        'key': voicerss_api_key,
        'hl': 'es-mx',
        'src': texto,
        'r': '0',
        'c': 'mp3',
        'f': '44khz_16bit_stereo',
        'ssml': 'false',
        'b64': 'true'
    })
    voice_data = voice.to_base64()
    voice_file = "voice.mp3"
    with open(voice_file, 'wb') as f:
        f.write(voice_data)
    os.system(f"afplay {voice_file}")
    os.remove(voice_file)

# Función principal
def main():
    print("Presiona 'q' para salir.")
    while True:
        # grabar audio
        duration = 3  # duración de la grabación en segundos
        fs = 44100  # frecuencia de muestreo
        print("Escuchando...")
        audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        print("Procesando...")

        # transformar audio en texto
        try:
            texto = transformar_audio_texto(audio_data.tolist())
            print(f"Texto: {texto}")
        except:
            print("No se pudo transformar el audio en texto.")
            continue

        # procesar comando de voz
        if "hola" in texto.lower():
            hablar("Hola, ¿en qué puedo ayudarte?")
        elif "adiós" in texto.lower() or "chao" in texto.lower():
            hablar("Adiós, que tengas un buen día.")
            break
        elif "cómo estás" in texto.lower():
            hablar("Estoy bien, gracias. ¿Y tú?")
        elif "hora" in texto.lower():
            hora_actual = time.strftime("%I:%M %p")
            hablar(f"La hora actual es {hora_actual}.")
        else:
            hablar("No entendí lo que dijiste. Por favor, intenta de nuevo.")

        # esperar un segundo antes de volver a grabar
        time.sleep(1)

if __name__ == "__main__":
    main()
