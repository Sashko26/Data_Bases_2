import ctypes
import subprocess

from . import message
from . import globalValue
from . import staticData
from . import client





r= client.r
def send_a_message():
    print("klapan:::::::: ")
    print(globalValue.loginedUser)
    print("someone that need to get:::::")
    print(globalValue.userThatNeedToGetMessage)
    print("send_a_message")
    our_message = input()
    message.create_message(globalValue.loginedUser,globalValue.userThatNeedToGetMessage,our_message)



def read_income_messages():

    print("read_income_messages")
    #длина списка доставленных сообщении
    end = r.llen(staticData.delivered_messages)
    # получить весь список доставленных сообщении, то есть ихние логины (мы получили весь список из диапазона)
    listOfDeliveredMessages = r.lrange(staticData.delivered_messages,0,end)

    listOfMessagesThatYouNeedToRead = []
    for el in listOfDeliveredMessages:
         #добавление логина сообщения, которые адресованы нам
         if "_to_"+globalValue.loginedUser in el:
             listOfMessagesThatYouNeedToRead.append(el)
             #добавление логина прочитаного сообщения в список прочитаних сообщений
             r.rpush(staticData.read_messages,el)
             # удаление логина прочитаного сообщения из списка доставленых, которые непрочитаны
             r.lrem(staticData.delivered_messages, 1, el)
    listOfMessagesThatYouNeedToReadWithMessageBody =[]
    # получить тело всех сообщении, которые мы с сейчас прочитаем
    for el in listOfMessagesThatYouNeedToRead:
        ourMessageObj = r.hgetall(el)
        message_obj_as_an_dict = {"_from":ourMessageObj["_from"],"_to":ourMessageObj["_to"],"body":ourMessageObj["body"],"date":ourMessageObj["dataOfCreating"]}
        listOfMessagesThatYouNeedToReadWithMessageBody.append(message_obj_as_an_dict)
    #удаление всех сообщений из списка доставленых, что адресованы нашему получателю
    for el in listOfMessagesThatYouNeedToReadWithMessageBody:
        print("from: " +el['_from'])
        print("to: " + el['_to'])
        print("date of sending: " + el['date'])
        print("message: "+el['body'])
    input()
    #//trem/ LREM


def messages_are_checking_for_spam():
    print("messages_are_checking_for_spam")
    # длина списка доставленных сообщении
    end = r.llen(staticData.checking_on_spam) #changed
    # получить весь список доставленных сообщении, то есть ихние логины (мы получили весь список из диапазона)
    listOfDeliveredMessages = r.lrange(staticData.checking_on_spam, 0, end)

    listOfMessagesThatYouNeedToRead = []
    for el in listOfDeliveredMessages:
        # добавление логина сообщения, которые мы отправили на проверку
        if "_from_" + globalValue.loginedUser in el:
            listOfMessagesThatYouNeedToRead.append(el) #changed
    listOfMessagesThatYouNeedToReadWithMessageBody = []
    # получить тело всех сообщении, которые мы с сейчас прочитаем
    for el in listOfMessagesThatYouNeedToRead:
        ourMessageObj = r.hgetall(el)
        message_obj_as_an_dict = {"_from": ourMessageObj["_from"], "_to": ourMessageObj["_to"],
                                  "body": ourMessageObj["body"], "date": ourMessageObj["dataOfCreating"]}
        listOfMessagesThatYouNeedToReadWithMessageBody.append(message_obj_as_an_dict)

    for el in listOfMessagesThatYouNeedToReadWithMessageBody:
        print("from: " + el['_from'])
        print("to: " + el['_to'])
        print("date of sending: " + el['date'])
        print("message: " + el['body'])

    input()


def messages_are_blocked_due_to_spam():
    print("messages_are_blocked_due_to_spam")
    # длина списка доставленных сообщении
    end = r.llen(staticData.blocked_messages)  # changed changed
    # получить весь список доставленных сообщении, то есть ихние логины (мы получили весь список из диапазона)
    listOfDeliveredMessages = r.lrange(staticData.blocked_messages, 0, end)

    listOfMessagesThatYouNeedToRead = []
    for el in listOfDeliveredMessages:
        # добавление только сообщении которые были отправлены нашим пользователем и быди заблокированы
        if "_from_" + globalValue.loginedUser in el:
            listOfMessagesThatYouNeedToRead.append(el)  # changed
    listOfMessagesThatYouNeedToReadWithMessageBody = []
    # получить тело всех сообщении, которые были заблокированы
    for el in listOfMessagesThatYouNeedToRead:
        ourMessageObj = r.hgetall(el)
        message_obj_as_an_dict = {"_from": ourMessageObj["_from"], "_to": ourMessageObj["_to"],
                                  "body": ourMessageObj["body"], "date": ourMessageObj["dataOfCreating"]}
        listOfMessagesThatYouNeedToReadWithMessageBody.append(message_obj_as_an_dict)

    for el in listOfMessagesThatYouNeedToReadWithMessageBody:
        print("from: " + el['_from'])
        print("to: " + el['_to'])
        print("date of sending: " + el['date'])
        print("message: " + el['body'])


    input()


def sent_but_not_read_messages():
    print("sent_but_not_read_messages")
    # длина списка доставленных сообщении
    end = r.llen(staticData.delivered_messages)  # changed changed
    # получить весь список доставленных сообщении, то есть ихние логины (мы получили весь список из диапазона)
    listOfDeliveredMessages = r.lrange(staticData.delivered_messages, 0, end)

    listOfMessagesThatYouNeedToRead = []
    for el in listOfDeliveredMessages:
        # добавление только сообщении которые были отправлены нашим пользователем и быди непрочитаны
        if "_from_" + globalValue.loginedUser in el:
            listOfMessagesThatYouNeedToRead.append(el)  # changed
    listOfMessagesThatYouNeedToReadWithMessageBody = []
    # получить тело всех сообщении, которые были непрочитаны
    for el in listOfMessagesThatYouNeedToRead:
        ourMessageObj = r.hgetall(el)
        message_obj_as_an_dict = {"_from": ourMessageObj["_from"], "_to": ourMessageObj["_to"],
                                  "body": ourMessageObj["body"], "date": ourMessageObj["dataOfCreating"]}
        listOfMessagesThatYouNeedToReadWithMessageBody.append(message_obj_as_an_dict)

    for el in listOfMessagesThatYouNeedToReadWithMessageBody:
        print("from: " + el['_from'])
        print("to: " + el['_to'])
        print("date of sending: " + el['date'])
        print("message: " + el['body'])

    input()


