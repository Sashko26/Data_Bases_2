import msvcrt
from . import globalValue
from . import menu
from . import staticData
from . import adminUserLogic
from . import simpleUserLogic
from . import authorization
from . import window
import os
from . import window
from datetime import datetime, date
from . import client
r = client.r
def up():
    if globalValue.currentWindow == window.getNameOfActiveWindow():
        while msvcrt.kbhit():
            msvcrt.getch()
        if globalValue.selected == 0:
            menu.show_menu()
            return
        globalValue.selected -= 1
        menu.show_menu()



def down():
    if globalValue.currentWindow == window.getNameOfActiveWindow():
        while msvcrt.kbhit():
            msvcrt.getch()
        if globalValue.isListForSending == True:
            if globalValue.selected == len(globalValue.listOfUsers) - 1:
                menu.show_menu()
                return
            globalValue.selected += 1
            menu.show_menu()
            return
        if globalValue.isAdmin == True:
            if globalValue.selected == len(staticData.adminDealsArray)-1:
                menu.show_menu()
                return
            globalValue.selected += 1
            menu.show_menu()
            return
        if globalValue.isSimpleUser == True:
            if globalValue.selected == len(staticData.simpleUserDealsArray)-1:
                menu.show_menu()
                return
            globalValue.selected += 1
            menu.show_menu()
            return
        if globalValue.isStartMenu == True:
            if globalValue.selected == len(staticData.startMenuArray)-1:
                menu.show_menu()
                return
            globalValue.selected += 1
            menu.show_menu()
            return

def shift():
    if globalValue.currentWindow == window.getNameOfActiveWindow():
       # global selected
        if globalValue.isAdmin == True and staticData.adminDealsArray[globalValue.selected]!='Exit':
                if staticData.adminDealsArray[globalValue.selected] == 'log events':
                   adminUserLogic.log_events()
                if staticData.adminDealsArray[globalValue.selected] == 'List of Users these are online':
                    adminUserLogic.List_of_Users_these_are_online()
                if staticData.adminDealsArray[globalValue.selected] == 'Rating of active users':
                    adminUserLogic.Rating_of_active_users()
                if staticData.adminDealsArray[globalValue.selected] == 'Rating of active spamers':
                    adminUserLogic.Rating_of_active_spamers()
                menu.show_menu()
        elif globalValue.isAdmin == True and staticData.adminDealsArray[globalValue.selected]=='Exit':

             menu.changeMenu('start')
             globalValue.selected = 0
             menu.show_menu()
        elif globalValue.isSimpleUser == True and staticData.simpleUserDealsArray[globalValue.selected]!='Exit':
            #selected = 0
            if staticData.simpleUserDealsArray[globalValue.selected] == 'Send a message':
                menu.changeMenu('send_message')
                menu.show_menu()

            if staticData.simpleUserDealsArray[globalValue.selected] == 'Read income messages':
                simpleUserLogic.read_income_messages()
            if staticData.simpleUserDealsArray[globalValue.selected] == 'messages are checking for spam':
                simpleUserLogic.messages_are_checking_for_spam()
            if staticData.simpleUserDealsArray[globalValue.selected] == 'messages are blocked due to spam':
                simpleUserLogic.messages_are_blocked_due_to_spam()
            if staticData.simpleUserDealsArray[globalValue.selected] == 'Sent but not read messages':
                simpleUserLogic.sent_but_not_read_messages()
            menu.show_menu()
        elif globalValue.isSimpleUser == True and staticData.simpleUserDealsArray[globalValue.selected]=='Exit':
             date = str(datetime.today())
             log = globalValue.loginedUser + " " + date + " user logged out!"
             r.rpush(staticData.log_events, log)
             menu.changeMenu('start')
             globalValue.selected = 0
             menu.show_menu()

        elif globalValue.isStartMenu == True and staticData.startMenuArray[globalValue.selected]!='Exit':
            if staticData.startMenuArray[globalValue.selected] == 'Admin':
                    menu.changeMenu('admin')
                    authorization.enteringUser()
                    globalValue.selected = 0
                    menu.show_menu()
            elif staticData.startMenuArray[globalValue.selected] == 'Simple User':
                    menu.changeMenu('simple')
                    authorization.enteringUser()
                    globalValue.selected = 0
                    menu.show_menu()
            elif staticData.startMenuArray[globalValue.selected] == 'Worker':
                    menu.changeMenu('worker')
                    globalValue.selected = 0
                    menu.show_menu()
        elif globalValue.isStartMenu == True and staticData.startMenuArray[globalValue.selected] == 'Exit':
            os.abort()
        elif globalValue.isListForSending == True:
            simpleUserLogic.send_a_message()
            menu.changeMenu("simple")

            menu.show_menu()
