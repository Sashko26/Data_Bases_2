import random
import os
from . import staticData
from . import globalValue
from . import client
from . import window
r=client.r
def changeMenu(mode):
    globalValue.selected =0
    globalValue.isAdmin = False
    globalValue.isSimpleUser = False
    globalValue.isStartMenu = False
    globalValue.isListForSending = False
    globalValue.isWorker = False
    if mode == 'admin':
        globalValue.isAdmin =True
    if mode == 'simple':
        globalValue.isSimpleUser = True
    if mode == 'start':
        globalValue.isStartMenu = True
    if mode == 'send_message':
        globalValue.isListForSending =True
    if mode == 'worker':
        globalValue.isWorker = True

    #["log events", "List of Users these are online", "Rating of active users", "Rating of active spamers", "Exit"]
def show_menu(str=""):

    os.system('cls||clear')
    import win32gui
    w = win32gui
    print(w.GetWindowText(w.GetForegroundWindow()))
    if str!="":
        print(str)
    print("Choose an option:")
    iterator=0
    if globalValue.isStartMenu == True:
        for el in staticData.startMenuArray:
            print("{1} {0}. {3} {0} {2}".format(iterator, ">" if globalValue.selected == iterator else " ", "<" if globalValue.selected == iterator else " ",el))
            iterator=iterator+1
        return
    if globalValue.isListForSending == True:
        globalValue.listOfUsers = r.smembers(staticData.listOfUsers)
        for user in globalValue.listOfUsers:
            if globalValue.selected == iterator:
                globalValue.userThatNeedToGetMessage = user
            print("{1} {0}. {3} {0} {2}".format(iterator, ">" if globalValue.selected == iterator else " ", "<" if globalValue.selected == iterator else " ",user))
            iterator=iterator+1
        return
    if globalValue.isSimpleUser == True:
        for el in staticData.simpleUserDealsArray:

            print("{1} {0}. {3} {0} {2}".format(iterator, ">" if globalValue.selected == iterator else " ",
                                                "<" if globalValue.selected == iterator else " ", el))
            iterator = iterator + 1
        return
    if globalValue.isAdmin == True:
        for el in staticData.adminDealsArray:
            print("{1} {0}. {3} {0} {2}".format(iterator, ">" if globalValue.selected == iterator else " ",
                                                "<" if globalValue.selected == iterator else " ", el))
            iterator = iterator + 1
        return

    if globalValue.isWorker == True:
        worker = r.pubsub()
        worker.subscribe(staticData.listOfCreatedMessages)
        while True:
            message = worker.get_message()
            if message:
                print(message['data'])
                end = r.llen(staticData.Queue)-1
                list_messages_for_checking = r.lrange(staticData.Queue,0,end)
                for el in list_messages_for_checking:
                    r.lpop(staticData.Queue)
                    r.lpop(staticData.listOfCreatedMessages)
                    r.rpush(staticData.checking_on_spam,el)
                end = r.llen(staticData.checking_on_spam)
                our_data_for_checking_on_spam = r.lrange(staticData.checking_on_spam,0,end)
                i = 0
                for element in our_data_for_checking_on_spam:
                    our_message = r.hgetall(our_data_for_checking_on_spam[i])
                    our_spamer = our_message['_from']
                    random.seed()

                    if random.randint(0,9)%2== 1:

                        r.rpush(staticData.delivered_messages,our_data_for_checking_on_spam[i])
                        print("Approved Message, "+our_data_for_checking_on_spam[i]+"!!!)")
                        r.lpop(staticData.checking_on_spam)
                        p = r.pipeline()

                        p.publish("get_"+our_message['_to'],"income message from "+our_message['_from']+"!!!!")

                    else:
                        print(random.random()%2)
                        r.rpush(staticData.blocked_messages, our_data_for_checking_on_spam[i])
                        r.lpop(staticData.checking_on_spam)
                        print("It is a spam, disrespect((( - message "+our_data_for_checking_on_spam[i])
                        r.zincrby(staticData.listOfSpamers,1,our_spamer)
                    i += 1

