import speech_recognition as sr #Biblioteca que realiza operaciones de reconocimiento de voz en tiempo real.
import openai                   #Biblioteca para interactuar con el servicio OpenAI API.
from gtts import gTTS           #Biblioteca para convertir texto en voz (text-to-speech).
from pygame import mixer        #Biblioteca para reproducir archivos de audio en Python.
import os                       #Biblioteca para realizar operaciones del sistema operativo como eliminar archivos.
import time as ti               #Biblioteca para manejar el tiempo.
import random                   #Biblioteca para generar números aleatorios.


#API Key de OpenAI
openai.api_key = "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"

#La función transformar_audio_texto() utiliza la biblioteca speech_recognition para convertir el audio capturado por el micrófono en texto. 
#La función también maneja posibles errores que pueden ocurrir durante el proceso de conversión.
def transformar_audio_texto():

    r = sr.Recognizer()                                           #crea una instancia del objeto Recognizer() de la biblioteca SpeechRecognition, que permite la conversión de audio a texto.

    with sr.Microphone() as origen:                               #Esta línea utiliza el micrófono del dispositivo como origen de audio.
        r.pause_threshold = 0.8                                   #Establece un tiempo de espera en segundos antes de considerar que la entrada de audio ha finalizado. Esto ayuda a reducir la cantidad de ruido de fondo que se convierte en texto.
        print("Escuchando")                                         #Imprime un mensaje en la consola para indicar que el programa está escuchando.
        audio = r.listen(origen)                                    #escucha la entrada de audio del micrófono y devuelve un objeto AudioData.
        try:
            pedido = r.recognize_google(audio, language="es-mx")
            print("Tu: " + pedido)
            return pedido
        except sr.UnknownValueError:
            print("Lo siento, no entendí")
            return "Sigo esperando"
        except sr.RequestError:
            print("Lo siento, no hay servicio de red")
            return "Sigo esperando"
        except:
            print("Algo salio mal")
            return "Sigo esperando"

#La función hablar() utiliza la biblioteca gtts para convertir el texto en voz, guardar el archivo de audio generado y reproducirlo utilizando la biblioteca mixer. 
#El archivo de audio se elimina después de ser reproducido.
def hablar(mensaje):
    volumen = 0.7 
    tts = gTTS(mensaje, lang="es" , slow=False)  #inicializa un objeto gTTS que recibe como parámetro el mensaje de texto a sintetizar y la configuración del lenguaje y velocidad de habla. La biblioteca gTTS genera un archivo de audio a partir del texto proporcionado.
    ran = random.randint(0,999)                  #Se almacena un numero randomico en ran
    filename = 'Temp' + format(ran) + '.mp3'     #Crea una cadena de caracteres con el nombre del archivo de audio que se va a generar, que consiste en la palabra "Temp" seguida del número aleatorio generado en la línea anterior y la extensión ".mp3".
    tts.save(filename)                           #Se guarda el archivo de audio con el nombre filename
    mixer.init()                                 #Se inicializa el objeto mixer de la biblioteca pygame
    mixer.music.load(filename)                   #Carga el archivo de audio generado en el objeto mixer.
    mixer.music.set_volume(volumen)              #Establece el volumen de salida del objeto mixer 
    mixer.music.play()                           #Reproducción del archivo de audio.

    while mixer.music.get_busy():                #Espera a que termine la reproducción del archivo de audio.
        ti.sleep(0.3)

    mixer.quit()                                 #La línea 13 cierra el objeto mixer.
    os.remove(filename)                          #Borra el archivo de audio generado


#La función main() es el punto de entrada del programa. 
#Primero define una variable conversation que contiene una introducción que explica el propósito del chatbot Danva, es decir, 
#proporcionar información turística sobre la ciudad de Latacunga en Ecuador.
#En la funcion main() definimos la comunicacion con OpenAI

def main():
    #Conversation es el preseteo que le damos a chatgpt para que tome el rol que queremos
    conversation = "Danva es un chatbot en el rol de una guia turstica muy amable y divertida." \
					"Ella propone proporciona información turistica sobre la ciudad de Latacunga y sus fiestas tradicionales" \
					"Ella conoce lugares turisticos donde puedan divertirse y distraerse" \
					"Ella recomienda la comida tipica de la ciudad de Latacunga." \
					"El objetivo principal es que los turistas conozcan un poco más sobre la ciudad de Latacunga de Cotopaxi Ecuador."
    
#En hablar() damos la bienvenida al usuario y pregunta cómo puede ayudar.
    hablar("Hola! Soy DanVa tu asistente turístico personal, ¿En qué puedo ayudarte?")

#En un bucle while True permite al usuario hacer preguntas a Danva mediante la función transformar_audio_texto() que convierte el audio del usuario en texto.
    while True:
        question = transformar_audio_texto().lower()

#conversation y se utiliza la API de OpenAI para generar una respuesta utilizando el modelo text-davinci-003. 
#La respuesta generada se agrega a la variable conversation, se muestra en la consola con la etiqueta "Danva:"
        conversation += "\nTu: " + question + "\nDanva:"            #Agrega la pregunta del usuario (almacenada en la variable question) a la conversación, que se almacena en la variable conversation, junto con un indicador de quién está hablando ("Tu" o "Danva").
        response = openai.Completion.create(
            model="text-davinci-003",                               #Utiliza la API de OpenAI para generar una respuesta a la pregunta del usuario. Se utiliza el modelo text-davinci-003 para generar la respuesta.
            prompt=conversation,
            temperature=0.5,
            max_tokens=200,
            top_p=0.3,
            frequency_penalty=0.5,
            presence_penalty=0.0,
            stop=["\n", " You:", " Danva:"]
        )
        answer = response.choices[0].text.strip()                    #Almacena la respuesta generada por el modelo en la variable answer, eliminando cualquier espacio en blanco al principio o al final de la respuesta.
        conversation += answer                                       #Agrega la respuesta generada por el modelo a la conversación.
        print("Danva: " + answer + "\n")                             #Imprime la respuesta generada por el modelo en la consola.
        hablar(answer)                                               #Convierte la respuesta generada por el modelo en una voz sintética y reproducirla a través de los altavoces.


main()
