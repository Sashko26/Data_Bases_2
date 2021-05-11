import datetime
from src import staticData
from src import globalValue
from src import client
from src import events
from src import window
from threading import Thread
r= client.r
import keyboard
from src import menu

globalValue.listOfUsers = r.smembers(staticData.listOfUsers)
def key_subscibe():
    keyboard.add_hotkey('up',events.up)
    keyboard.add_hotkey('down',events.down)
    keyboard.add_hotkey('shift',events.shift)
    keyboard.wait()



def prescript(income_to):
    p = r.pubsub()
    p.subscribe(income_to)
    while True:
        message = p.get_message()
        if message:
            print(message)




currentWindow = window.getNameOfActiveWindow()
menu.show_menu()
key_subscibe()








































