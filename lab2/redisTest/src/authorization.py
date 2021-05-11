from . import globalValue
from . import menu
import time
from . import client
r= client.r
from. import UserObject
from.  import staticData
from . import window
from datetime import datetime, date




def enteringUser(string=""):
    if string!="":
        print(string)

    print("enter your username:")
    if globalValue.isAdmin ==True:
        print(", Admin")
    login = input()
    globalValue.loginedUser =login
    if globalValue.isAdmin == True:
        print("enter your password,admin:")
        password = input()
    userObject = r.hgetall(login)
    if userObject == {} or userObject is None:
        print("You  have just registered in a chat and we have created your account!!! You are welcome...")
        if globalValue.isAdmin ==True:
            UserObject.createUser(globalValue.loginedUser,globalValue.isAdmin,password)
            menu.changeMenu('admin')
        if globalValue.isAdmin == False:
            UserObject.createUser(globalValue.loginedUser,globalValue.isAdmin)
            p = r.pubsub()
            p.subscribe("get_" + globalValue.loginedUser)
            menu.changeMenu('simple')
            date = str(datetime.today())
            log = globalValue.loginedUser + " " + date + " user logged in!"
            r.rpush(staticData.log_events, log)

    else:
        if globalValue.isAdmin == True:
            try:
                if userObject['password']!= password:
                    enteringUser("You entered not correct password!!!")

                else:
                    menu.changeMenu('admin')

                    return True
            except KeyError:
                menu.changeMenu('simple')
                print("You are not admin, you are simple user!")
                p = r.pubsub()
                menu.changeMenu('simple')
                date = str(datetime.today())
                log = globalValue.loginedUser + " " + date + " user logged in!"
                r.rpush(staticData.log_events, log)

        else:
            p = r.pubsub()
            time.sleep(3)
            menu.changeMenu('simple')
            date = str(datetime.today())
            log = globalValue.loginedUser + " " + date + " user logged in!"
            r.rpush(staticData.log_events, log)
            return True