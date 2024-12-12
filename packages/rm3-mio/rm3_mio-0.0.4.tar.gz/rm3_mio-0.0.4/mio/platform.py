#########################
# PLATFORM MODULE
# (system threading, shell commands, popups)
#########################

import threading
from subprocess import DEVNULL, STDOUT, call

# run a function on a separate thread
def startDaemon(process):
    t = threading.Thread(target=process)
    t.daemon = True
    t.start()


# run a terminal command
def shell(command, silent=False):
    if type(command)==str and "\"" not in command and "\'" not in command:
        command = command.split()
    if type(command)!=list:
        raise ValueError("mio.shell() expects a list strings")
    if silent:
        return call(command, stdout=DEVNULL, stderr=STDOUT)
    else:
        return call(command)


# send an notification popup Zenity (GTK Linux notify)
def popupInfo(title="Listen Up!", message="An error occurred", level=1):
    alert = ["info", "warning", "error"][level]
    command = [
        'zenity',
        f'--{alert}',
        f'--text=\"{message}\"',
        f'--title=\"{title}\"'
    ]
    shell(command, silent=True)

# send an Y/N popup Zenity (GTK Linux alert)
def popupQuestion(question):
    command = f'zenity --question --text=\"\"{question}\"\"'
    command = [
        'zenity',
        f'--question',
        f'--text=\"{question}\"'
    ]
    response = shell(command, silent=True)
    if response == 0:
        return True
    elif response==1:
        return False
    else:
        return None


# ZENETY POPUP TYPES
# --calendar
# --entry
# --error
# --info
# --file-selection
# --list               <<<< def popupList(...)
# --notification
# --progress
# --question
# --warning
# --scale
# --text-info
# --color-selection
# --password
# --forms
# --display=DISPLAY