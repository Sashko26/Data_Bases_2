from datetime import datetime, date, time

from . import client
from . import staticData
from . import globalValue

r = client.r

def create_message(login_from,login_to,body):
    p = r.pipeline()
    login_of_messages = "_from_"+login_from+"_to_"+login_to+"_"+str(datetime.today())
    p.hset(login_of_messages, '_from', login_from)
    p.hset(login_of_messages, '_to', login_to)
    p.hset(login_of_messages, 'dataOfCreating', str(datetime.today()))
    p.hset(login_of_messages, 'body', body)
    p.zincrby(staticData.list_of_active_user, 1, login_from)
    p.lpush(staticData.listOfCreatedMessages, login_of_messages)
    p.rpush(staticData.Queue,login_of_messages)

    p.publish(staticData.listOfCreatedMessages, login_of_messages)



    #if globalValue.isAdmin == True:
    #    p.hset(globalValue.login, 'password', globalValue.password)
    p.execute()
