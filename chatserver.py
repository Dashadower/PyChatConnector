# -*- coding: utf-8 -*-
import _thread as thread
import time, shelve, logging, traceback, os, json, traceback, codecs, ast
import socket
from tkinter import *
from tkinter.simpledialog import askstring
from _thread import start_new_thread
from tkinter.messagebox import *
from urllib.request import urlopen
import pickle
global defaultsetupfile
defaultsetupfile = """
# -*- coding:utf-8 -*-
# Setup script for chatserver.\n
########################################\n
global restrictcountry, loginmessage
########################################\n
restrictcountry = ["ALL"] # Please write the ISO country code in which only countries listed within this list can join. For country codes, please visit countrycode.org.
\n
loginmessage = "서버에 접속하셨습니다."
"""
fsdf = "close_from_Server_fhaheAfsdhF"
global closecommand
closecommand = fsdf.encode("utf-8")
def now():
    return time.asctime(time.localtime())

def handleclient(connection, ADDR):
    if 1 == 0:
        ats ="Forbidden country".encode()
        connection.send(ats)
        connection.send(fsdf)
        connection.close()
    else:
        recievedcreds = connection.recv(1024)
        recievedcreds_d = recievedcreds.decode("utf-8")
        conn2 = conn.open()
        root = conn2.root()
        global isuser

        isuser = False
        try:
            commandtype, recievedid, recievedpass = recievedcreds_d.split("`")
        except:

            connection.send(closecommand)
            connection.close()
            print("%s disconnected"%(ADDR))
        if commandtype == "Register":


            root[recievedid] = recievedpass
            transaction.get().commit()
            print("Performed registeration process for", ADDR)
            fasdf3fds = "[MSG]`회원가입 완료. 클라이언트를 종료후 로그인해주세요`fd"
            connection.send(fasdf3fds.encode("utf-8"))
            connection.send(closecommand)
            connection.close()


        elif commandtype == "Login":


            haveid = recievedid in root
            if haveid == False:

                print(ADDR, " failed to login.")
                fsdf = "[MSG]`로그인 실패`asdf"
                connection.send(fsdf.encode("utf-8"))
                connection.send(closecommand)
                connection.close()
            else:
                shelvepass = root[recievedid]
                if recievedpass == shelvepass:
                    isbanlist = shelve.open("banlist")
                    amiinbanlist = recievedid in isbanlist


                    if amiinbanlist == False:
                        fsdffsd = "[MSG]`로그인 성공!`asd"
                        connection.send(fsdffsd.encode("utf-8"))
                        isuser = True
                        print(ADDR, "logged in as ", recievedid)
                    else:
                        isinbannedstate = isbanlist[recievedid]
                        isbanlist.close()
                        if isinbannedstate == "True":
                            print("Banned user %s attempted to connect."%(recievedid))
                            dgfa = "[MSG]`User %s, has been banned.asf`as"%(recievedid)
                            connection.send(dgfa.encode("utf-8"))
                            connection.send(closecommand)
                            connection.close()
                        else:
                            fsdffsd = "[MSG]`로그인 성공!`as"
                            connection.send(fsdffsd.encode("utf-8"))
                            isuser = True
                            print(ADDR, "logged in as ", recievedid)


                else:

                    print(ADDR, " failed to login.")
                    fsdfsadf = "[MSG]`로그인 실패`as"
                    connection.send(fsdfsadf.encode("utf-8"))
                    connection.send(closecommand)
                    connection.close()
        if isuser == True:
            global userstatus
            if checkadm(recievedid) == True:
                userstatus = "Admin"
            else:
                userstatus = "User"
            connections.append(connection)
            users.append(recievedid)

            sod = str(ADDR)
            msg = "[MSG]`[Server] %s %s 님이 채팅방에 입장하셨습니다.`aft"%(now(),recievedid)
            logmessage = loginmessage.encode("utf-8")
            connection.send(logmessage)
            loginmessage2 = "현재 접속인원:%d\n"%(len(connections))
            connection.send(loginmessage2.encode("utf-8"))
            msg2 = msg.encode("utf-8")
            broadcast(msg2)

            while True:

                iscommand = False

                try:
                    recieved = connection.recv(1024)
                except Exception:

                    break
                adsf = recieved.decode("utf-8")

                try:
                    cmd = adsf.split("`")[0]
                    arg1 = asdf.split("`")[1]
                    arg2 = asdf.split("`")[2]
                    arg3 = asdf.split("`")[3]
                except:

                    pass
                else:



                    if cmd == "[KICK]":
                        if checkadm(arg3) == True:
                            kickmsg = "[KICK]`%s`%s"%(arg1, arg2)
                            broadcast(kickmsg.encode())
                            print("%s kicked %s for %s"%(arg3, arg1, arg2))
                            iscommand = True
                        else:
                            print("non-admin %s tried to use kick command"%(arg3))
                            heosdf = "[WARN]`%s`%s not an admin"%(arg3,arg3)
                            broadcast(heosdf.encode())
                            iscommand = True
                if adsf == "exits":
                    try:
                        connection.close()
                    except:
                        pass

                    connections.remove(connection)
                    users.remove(recievedid)

                    fdf = "[MSG]`[Server] %s %s 님이 채팅방을 퇴장하셨습니다.`as"%(now(), recievedid)

                    print("remaining connections:", connections)
                    print(fdf)
                    broadcast(fdf.encode("utf-8"))

                elif adsf != "exits" and iscommand != True:

                    print("%s %s:%s" % (now(), recievedid, recieved))
                    output = "[MSG]`%s [%s]%s:%s`as"%( now(),userstatus,recievedid, recieved.decode("utf-8"))
                    message = output.encode("utf-8")
                    broadcast(message)
            else:
                pass

def broadcast(mssg):
    for i in connections:
        try:
            i.sendall(mssg)
        except:
            pass

def make_gui():
    roots = Tk()
    roots.title("server maintence module")
    Button(roots, text="kick", command=onkick).pack(side=LEFT)
    Button(roots, text="ban",command=onban).pack(side=LEFT)
    Button(roots, text="unban", command = unban).pack(side=LEFT)
    Button(roots, text="adminfy", command = onmakeadmin).pack(side=LEFT)
    Button(roots, text="advanced", command = onadvancedoptions).pack(side=LEFT)
    roots.mainloop()
def onkick():

    asd = askstring("","Which id will I kick?")
    fds = askstring("","What is the reason?")
    masdf = "[KICK]`%s`%s"%(asd, fds)
    broadcast(masdf.encode("utf-8"))
    showinfo("", "Succesfully kicked %s"%(asd))
def onban():
    fdsa = askstring("","Which id should I ban?")
    fasd = "[KICK]`%s`You have been banned."%(fdsa)
    broadcast(fasd.encode("utf-8"))
    rew = shelve.open("banlist")
    rew[fdsa] = "True"
    rew.close()
    showinfo("","succesfully banned %s"%(fdsa))
def unban():
    pwor = askstring("","Whick user should I unban?")
    fdasdf = shelve.open("banlist")
    if pwor in fdasdf:
        fdasdf[pwor] = "False"

        showinfo("","User %s has been succesfully unbanned"%(pwor))

    fdasdf.close()
def onmakeadmin():
    rew = askstring("","Which id should I make admin?")


    hys = shelve.open("admins")
    hys[rew] = "True"
    hys.close()
    showinfo("","succesfully made %s admin"%(rew))
def onadvancedoptions():
    advancedoptionsw = Toplevel()
    advancedoptionsw.title("Advanced options")
    advancedoptionsw.grab_set()
    advancedoptionsw.focus_set()
    Button(advancedoptionsw, text="Delete user databases",command=ondeletedb).pack(side=LEFT)
def ondeletedb():
    try:
        os.remove("users.fs")
        os.remove("users.fs.lock")
        os.remove("users.fs.tmp")
        os.remove("users.fs.index")
    except:
        fdas = traceback.format_exc()
        showerror("","An error has occured:.\n"+fdas)
    else:
        showinfo("","Succesfully deleted the user databases.")
def checkadm(idchecked):
    kqs = shelve.open("admins")
    asdf = idchecked in kqs
    if asdf == True:

        return True

    else:
        return False
def senduserdata():
    while True:

        fasd = json.dumps(users)
        ts = fasd.encode()
        broadcast(ts)
        print("sent user lists")
        time.sleep(5)

def get_setup():

    try:
        data_setup = codecs.open("clientsetup.properties", "r", "utf-8")

    except:
        print("We have a stack raised fom python.standard.codecs.open")
        print("Stack trace:\n")
        traceback.print_exc()
        print("Creating setup file")
        asfd = open("clientsetup.properties", "w", encoding="utf-8")
        asfd.write(defaultsetupfile)
        asfd.close()
        try:
            os.mkdir("tmp")
        except:
            pass

        time.sleep(5)
        print("Completed. Please restart the program")
        time.sleep(5)
        sys.exit()
    else:
        fdd  = open("clientsetup.properties", encoding="utf-8")
        fdas = fdd.read().replace(u'\ufeff', '')
        exec(fdas)
        data_setup.close()

def check_location(ip):
    url = 'http://freegeoip.net/json/'
    try:
        luk = urlopen(url+ip)
        f = luk.read().decode()
        a = f.rstrip()
        g = ast.literal_eval(a)
        country = g["country_code"]
    except:
        print("Location could not be determined automatically")
        print("Error details:\n")
        traceback.print_exc()
    else:
        for i in restrictcountry:
            if country == i:
                return True
            else:
                return False

if __name__ == "__main__":
    get_setup()
    try:
        print("Chatclient v1.3")
        from ZODB import DB
        from ZODB.FileStorage import FileStorage
        import transaction
    except:

        print("Failed to import ZODB")
        print("Failed to import ZODB.FileStorage")
        fsd = input("Would you like to install pip and ZODB?")
        if fsd == "Y" or"y":
            print("Supported python version: 3.3 Installed version: %d.%d"%(sys.version_info[0],sys.version_info[1]))
            if sys.version_info[0] and sys.version_info[1] == 3:
                print("Downloading/installing pip")
                try:
                    import Dashutils.installtools.Win32
                except:
                    print("Failed to download Dashutils.installtools")
                    time.sleep(5)
                    raise SystemExit
                else:

                    if Dashutils.installtools.Win32.getpip(install=False) == True:
                        Dashutils.installtools.Win32.installpip()
                        print("Finished installing pip")
                        print("Downloading/installing ZODB")
                        Dashutils.installtools.Win32.runpip("install ZODB")
                        print("Finished installing pip and ZODB. Please try restarting the application.\nIf this repeats, please try installing ZODB manually.")
            time.sleep(5)
            raise SystemExit
        else:
            time.sleep(2)
            raise SystemExit
    else:
        global conn
        storage = FileStorage("users.fs")
        conn = DB(storage)

    start_new_thread(make_gui, ())
    global connections, users
    users = []
    connections = []
    addr = ("", 8080)
    r =socket.socket()

    print("socket object created at", now())

    r.bind(addr)
    r.listen(5)
    thread.start_new_thread(senduserdata, ())
    while True:
        print("Waiting for clients...")
        connection, ADDR = r.accept()

        print("We have connection from ", ADDR)

        thread.start_new_thread(handleclient, (connection, ADDR))



