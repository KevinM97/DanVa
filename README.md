# DanVa Proyecto Final ABC
DanVa es un chatBot reconocimiento de voz que utiliza la biblioteca de reconocimiento de voz "SpeechRecognition", la API de inteligencia artificial "OpenAI", y la biblioteca de síntesis de voz "gTTS" para responder a las preguntas del usuario.

Primero, el programa importa las bibliotecas necesarias, define la clave de la API de OpenAI y define dos funciones principales: "transformar_audio_texto()" y "hablar()".

La función "transformar_audio_texto()" utiliza la biblioteca "SpeechRecognition" para convertir la entrada de audio en texto. Primero, la función inicializa un objeto de tipo "Recognizer()" y utiliza el micrófono del dispositivo para escuchar la entrada de audio del usuario. Luego, utiliza el método "recognize_google()" de la biblioteca "Recognizer()" para convertir el audio en texto. Si el reconocimiento de voz no es exitoso, la función devuelve un mensaje de error.

La función "hablar()" utiliza la biblioteca "gTTS" para sintetizar un mensaje de texto en voz. El mensaje se guarda en un archivo de audio temporal, se carga en la biblioteca "pygame.mixer" y se reproduce a través de los altavoces del dispositivo.

La función principal del programa es "main()". Primero, se inicializa una variable "conversation" con una descripción del chatbot y su función. Luego, el chatbot saluda al usuario con un mensaje de bienvenida. A continuación, el programa entra en un bucle while para escuchar continuamente las preguntas del usuario utilizando la función "transformar_audio_texto()".

Cada vez que el usuario hace una pregunta, el programa utiliza la API de OpenAI para generar una respuesta a través del método "Completion.create()". Se proporciona un modelo de lenguaje pre-entrenado ("text-davinci-003"), y se le da una cadena de texto ("conversation") como contexto para generar una respuesta. La respuesta generada se agrega a la variable "conversation" y se habla a través de la función "hablar()".

El bucle continúa hasta que el usuario dice la palabra "Adiós". 
