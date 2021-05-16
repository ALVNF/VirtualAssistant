import speech_recognition
import pyttsx3
import threading
import datetime
import time
import queue


#import pyaudio
#from vosk import Model, KaldiRecognizer

"""
# Vosk recognition es más rápido pero el resultado no es tan bueno, la ventaja es que no necesitas internet
def takeCommand():
    model = Model("model")
    rec = KaldiRecognizer(model, 16000)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1,
                    rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()
    while True:
        data = stream.read(4000)
        if(len(data)) == 0:
            break
        if rec.AcceptWaveform(data):
            print(rec.Result())
        else:
            print(rec.PartialResult())
    print(rec.FinalResult())
"""

status = True
recognizer = speech_recognition.Recognizer()
engine = pyttsx3.init()


def getStatus():
    return status


def setStatus(statusType):
    global status
    status = statusType


def getVoices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        print(voice, voice.id)
        engine.setProperty('voice', voice.id)
        engine.say("Hello World!")
        engine.runAndWait()
        engine.stop()


rate = engine.getProperty('rate')
engine.setProperty('rate', rate-10)


def talk(verb, text):
    if engine._inLoop:
        engine.endLoop()

    sentence = verb + " " + text
    #engine = pyttsx3.init()
    engine.say(sentence)
    engine.runAndWait()


# Goolge es más lento pero el resultado es más acertado, la desventaja es que necesitas internet


def takeCommand():
    try:
        with speech_recognition.Microphone() as mic:
            talk("", "¿Qué es lo que desea?")
            recognizer.adjust_for_ambient_noise(mic, duration=1)
            audio = recognizer.listen(mic)

            command = recognizer.recognize_google(
                audio, key=None, language='es-ES', show_all=False)
            command = command.lower()

            print(f"[Recoginized] {command}")
            engine.say("Procesando...")
            engine.runAndWait()
            return command

    except Exception:
        command = ""
        return command


def voiceWriting(file):
    try:
        with speech_recognition.Microphone() as mic:
            talk("", "Preparado para escribir")
            recognizer.adjust_for_ambient_noise(mic, duration=1)
            audio = recognizer.listen(mic)

            command = recognizer.recognize_google(
                audio, key=None, language='es-ES', show_all=False)
            command = command.lower()

            file.write(command)
            file.write("\n")
            file.close()
            talk("Guardando", "")
            return command

    except Exception:
        return ""


def newReminder(list):
    # Se debe crear un nuevo hilo para el recordatorio pasnadole el tiempo restante para que finalize la tarea, es decir los minutos que va dormir el hilo
    # antes de hacer la llamada a la voz para que envie la tarea, la cual también se la pasamos.

    ahora = datetime.datetime.now()
    fecha = list[0]
    hora = list[1]
    tiempo = fecha + " " + hora
    time_obj = datetime.datetime.strptime(tiempo, '%Y-%m-%d %H:%M')
    restante = time_obj - ahora
    segundos = int(restante.total_seconds())

    threading.Thread(target=reminder, args=(segundos, list[2],)).start()


def returnData(dataReceived):
    data = dataReceived
    talk("", data)


def reminder(stopTime, task):
    time.sleep(stopTime)
    returnData("Recordatorio de la tarea." + task)


q = queue.Queue()


def speedRate():
    for thread in threading.enumerate():
        print("Hilos activos orden", thread.name)
    if engine._inLoop:
        engine.endLoop()

    engine.say(q.get())
    engine.runAndWait()
    q.task_done()


def callspeed():
    q.put("Recordatorio de la tarea 1")
    process = threading.Thread(target=speedRate).start()
    time.sleep(2)
    q.put("Recordatorio de la tarea 2")
    process2 = threading.Thread(target=speedRate).start()


callspeed()
