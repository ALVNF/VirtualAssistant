import speech_recognition
import pyttsx3
import pc_commands
import os
import re
import ast
import webbrowser
import win32.win32api as win32api
import ctypes

import threading

import pytz
import datetime

from subprocess import call


recognizer = speech_recognition.Recognizer()
engine = pyttsx3.init()


def activateCommand():
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=1)
            audio = recognizer.listen(mic)

            command = recognizer.recognize_google(
                audio, key=None, language='es-ES', show_all=False)
            command = command.lower()

            if 'ordenador' in command:
                print("[WAITING]")
                for thread in threading.enumerate():
                    print("Hilos activos orden", thread.name)
                command = pc_commands.takeCommand()
                return command
            else:
                command = ""
                return command

    except Exception:
        command = ""
        return command


def tellCommands():
    source = open('commands.py').read()
    functions = [f.name for f in ast.parse(source).body
                 if isinstance(f, ast.FunctionDef)]

    pc_commands.talk("Los comandos son:", "")
    for i in range(0, len(functions)):
        pc_commands.talk("", functions[i])


def cleanMail():
    path = "../../GoogleBot/e-mail_manager/main.py"
    print("Limpiando el correo")
    pc_commands.talk("Limpiando", "la bandeja de entrada")
    call(["python", path])


def openTerminal():
    print("Abriendo terminal")
    pc_commands.talk("Abriendo", "la terminal")
    os.system("start cmd /k")


def openTaskMng():
    print("Abriendo Administrador")
    pc_commands.talk("Abriendo", "Administrador de Tareas")
    os.system("start Taskmgr")


def openBrowser():
    print("Abriendo navegador")
    pc_commands.talk("Abriendo", "el navegador")
    webbrowser.open("https://google.com")


"""
def browserSearch():
    print("Buscando en navegador")
    talk("Buscando", "en el navegador")
    webbrowser.open("https://google.com")
"""


def sessionLock():
    print("Bloquear sesión")
    pc_commands.talk("Bloqueando", "la sesión")
    ctypes.windll.user32.LockWorkStation()


def pcHibernate():
    print("Suspendiendo sistema ")
    pc_commands.talk("Suspendiendo", "el sistema")

    os.system("shutdown /h")  # hibernate


def shutDown():
    print("Apagando al asistente")
    pc_commands.talk("Apagando", "al asistente, buenas noches")
    os._exit(0)


def writeFile():
    print("Abriendo nuevo archivo")
    pc_commands.talk("Abriendo", "nuevo archivo de texto")
    file = open("new_file.txt", "a+")
    pc_commands.voiceWriting(file)


def readFile():
    with open('./new_file.txt') as file:
        lines = file.readlines()
        engine.say(lines)
        engine.runAndWait()


def reminder():
    # key = fecha y hora (): value = la tarea a realizar
    tasks = []
    file = open("recordatorio.txt", "a+")
    voiceTask = pc_commands.voiceWriting(file)
    # print(voiceTask)

    if 'hoy' in voiceTask:
        fecha = datetime.datetime.today().strftime('%Y-%m-%d')
        #print("La fecha es ", fecha)
    elif 'mañana' in voiceTask:
        fecha = datetime.datetime.now() + datetime.timedelta(days=1)
        fecha = fecha.strftime('%Y-%m-%d')
        #print("La fecha es ", fecha)
    else:
        fecha = datetime.datetime.today().strftime('%Y-%m-%d')
        #print("La fecha es ", fecha)

    d = re.findall('[\d]{1,2}:[\d]{1,2}|[\d]{1,2}:[\d]{1,2} [aApP][mM]', voiceTask)[
        0].strip()

    time = datetime.datetime.strptime(d, "%H:%M")

    task = voiceTask.split(d)

    tasks.append(fecha)
    tasks.append(f'{time.hour}:{time.minute}')
    tasks.append(task[0])

    # print(tasks)
    # Llamas a la función para crear un nuevo hilo para el recordatorio y se limpia el diccionario, ya que la tarea ya ha sido asignada
    pc_commands.newReminder(tasks)

    tasks.clear()


def test(i, hora):

    ahora = datetime.datetime.now()
    fecha = '2021-05-11'

    tiempo = fecha + " " + hora
    time_obj = datetime.datetime.strptime(tiempo, '%Y-%m-%d %H:%M')
    restante = time_obj - ahora
    segundos = int(restante.total_seconds())
    tarea = "Tarea " + i
    print(segundos)
    pc_commands.reminder(segundos, tarea)
