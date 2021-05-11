from . import client
from . import staticData
r = client.r
def log_events():
    end = r.llen(staticData.log_events)
    listOfSpamers =  r.lrange(staticData.log_events,0,end)
    for el in listOfSpamers:
       print(el)
    input()
def List_of_Users_these_are_online():
    print("List_of_Users_these_are_online")
    input()
def Rating_of_active_users():
    print("Rating_of_active_users")
    amount = r.zcard(staticData.list_of_active_user)
    listOfActiveUsers = r.zrange(staticData.list_of_active_user, 0, amount, True, True)
    for el in listOfActiveUsers:
        print(el)
    input()

    input()
def Rating_of_active_spamers():
    print("Rating_of_active_spamers")
    amount = r.zcard(staticData.listOfSpamers)
    listOfSpamers = r.zrange(staticData.listOfSpamers,0,r.zcard(staticData.listOfSpamers),True,True)
    for el in listOfSpamers:
        print(el)
    input()
