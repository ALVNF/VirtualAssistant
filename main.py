import speech_recognition
import pyttsx3
import user_commands as commands

commandList = {'comandos': commands.tellCommands,
               'abrir terminal': commands.openTerminal,
               'abrir administrador': commands.openTaskMng,
               'abrir navegador': commands.openBrowser,
               'escribir archivo': commands.writeFile,
               'leer archivo': commands.readFile,
               'limpiar correo': commands.cleanMail,
               'nueva tarea': commands.reminder,
               # 'buscar': commands.browserSearch,
               'bloquear sesión': commands.sessionLock,
               'hibernar': commands.pcHibernate,
               'apagar': commands.shutDown}

# Próximo comando, intentar enviar un mensaje de whatsapp o telegram


def run_assistent():
    print("[SYSTEM LISTENING...]")

    myCommand = commands.activateCommand()

    for key in commandList:
        if key in myCommand:
            commandList.get(key)()


while True:
    run_assistent()
