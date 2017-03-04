# -*- coding: utf-8 -*-
################################################################################
#
#    Chat client_kor ver 1.0
#    released under CC-BY-NC License
#
#
#    By Shinyoung kim
#    tttllshin@gmail.com
#
#    Localized korean version
#
#
################################################################################
from tkinter import *
from tkinter.messagebox import *  # Just in case upper line fails

import socket, sys, time, os, zipfile, codecs, multiprocessing, threading, ast
import _thread as thread

from urllib.request import urlretrieve, urlopen

from contextlib import closing
global helptext, server_add, firstmsg, productversion



#server_add = ("112.149.79.39", 8080) #김창민이 서버 열때
server_add = ("127.0.0.1", 8080) #localhost
productversion = 1.1
defaultsetupfile = """
# Setup script for chatclient.\n
########################################\n
global server_add, usedebug, text_istrue, defaultdir, isadmin, ossystem, tmpdir, usrnm, usrpw, session_id, authcode, key # DO NOT MODIFY!!!!\n
########################################\n
server_add = ("127.0.0.1", 8080) # Server connection tuple. [0] is server address(or domain), [1] is port\n
########################################\n
usedebug = False #Is it in debug mode?\n
text_istrue = True\n
########################################\n
\n
defaultdir = os.getcwd()\n
\n
isadmin = False\n
\n
ossystem = sys.platform #operating system. At default is is set to automatically detect it.\n
tmpdict = "\tmp"\n
dirdict = []\n
dirdict.append(defaultdir)\n
dirdict.append(tmpdict)\n
tmpdir = "".join(dirdict)\n
"""

helptext = """
/exit 서버로부터 접속을 끊은 후 프로그램을 종료합니다.

/banrequest id (id)를 가진 사용자를 신고합니다.(현제 페쇄)

/private`id`msg (id)를 가진 사용자에게 (msg)라는 내용의 비밀 문자를 보냅니다. 주의! 꼭 구분 사이에 `를 넣어주세요. 예를 들면 bob이라는 사람에게 hello world를 보내고 싶으면 /private`bob`hello world를 입력하면 됩니다.현제로서는 비밀 메세지를 보낸 사람은 보낸 내용이 안 보여집니다. 현제 고치려고 노력줌.

/cls 창을 리셋합니다(클리어)
"""

def nothing():
    pass
def now():
    return time.asctime(time.localtime())

def credits_about():
    creditwindow = Toplevel(bg="black")
    creditwindow.title("정보")
    creditwindow.resizable(0,0)
    creditwindow.focus_set()
    creditwindow.grab_set()
    bub = Canvas(creditwindow, bg="black")
    bub.pack(expand=YES, fill=BOTH)
    photo = PhotoImage(file = 'C:/Users/Nitro/Desktop/download.gif')
    label = Label(bub,image=photo)
    label.image = photo
    label.pack(expand=YES, fill=BOTH)
    Button(creditwindow, text = "더 많은 정보를 원한다면 이 버튼을 클릭하세요.", fg="orange", bg="black", command = viewadvancedhelp).pack(side=BOTTOM)
    Label(creditwindow, text="   I AM A SUPPORTER OF BATTLEFIELD PLAY4FREE!   ", fg="orange", bg="black").pack(side=BOTTOM)
    Label(creditwindow, text="프로그래밍: Dashadower, jakads(thank you for testing)", fg="orange", bg="black").pack(side=BOTTOM)


    pass

def viewadvancedhelp():
    helptext = """
    이 Python 채팅 클라이언트는 제가 처음으로 개발한, 게임과 관련되지 않은 소켓 프로그램입니다.
    사실 이언 방송이 필요한 소켓은 UDP를 사용하는 것이 효율적이지만, UDP가 너무 복잡해서 제가
    TCP와 배열, 쓰레드를 이용한 방송 기법을 시용하여(그 기법은 서버에 있음 ㅇㅅㅇ) 한번 시험
    해봤습니다.
    잘 써보세요. 물론 쓸 데가 없겠지만..."""
    showinfo("", helptext)
def add_widget():
    global userlistmenu, last_msg
    last_msg = StringVar()
    last_msg.set("")
    userlistmenu = Menu(root, tearoff=0)
    userlistmenu.add_command(label="비밀 문자 보내기", command=lambda: getuserprivate(onlinelistbox.curselection()))
    menubar = Menu(root)
    menubar.add_command(label="파일", command=credits_about)
    root.config(menu=menubar)
    global textfield, umtext, totext, onlinelistbox
    umtext = StringVar()
    totext = Entry(root, textvariable = umtext, relief=SUNKEN)
    totext.bind("<Down>", setlastcommand)

    totext.pack(side=BOTTOM, fill=X)

    textfield = Text(root, relief=SUNKEN)
    ysbar = Scrollbar(root)
    ysbar.config(command=textfield.yview)
    textfield.config(yscrollcommand=ysbar.set)
    onlinelistbox = Listbox(root)
    onlinelistbox.pack(fill=BOTH, side=RIGHT,anchor=S)
    onlinelistbox.bind("<Button-3>",getusermenu)
    ysbar.pack(side=RIGHT, fill=Y, anchor=NE)
    textfield.pack(fill=BOTH,expand=YES)
    textfield.config(state=DISABLED)

def setlastcommand(event1):
    umtext.set(last_msg.get())
def getuserprivate(username):

    umtext.set("/private`{0}`".format(onlinelistbox.get(username[0])))
    totext.focus_set()
    last_msg.set("/private`{0}`".format(onlinelistbox.get(username[0])))
def getusermenu(event):
    try:
        selecteduser = onlinelistbox.curselection()
    except:
        pass
    else:
        print("got menu spawn")
        userlistmenu.post(event.x_root, event.y_root)

def retry_connect():
    start_client()
def checkmsg(adsf):
    ufds = umtext.get()
    try:
        cmd = ufds.split("`")[0]
        arg1 = ufds.split("`")[1]
        arg2 = ufds.split("`")[2]
    except:


        if ufds == "/?":
            textfield.config(state=NORMAL)
            textfield.insert(END, helptext)
            textfield.insert(END, "\n")
            textfield.config(state=DISABLED)
            umtext.set("")
            last_msg.set("/?")
        elif ufds == "fuck":
            sendmsg("****(SENSORED)")
        elif ufds == "/exit":
            doexit()
        elif ufds == "/cls":
            textfield.config(state=NORMAL)
            textfield.delete(1.0, END)
            textfield.config(state=DISABLED)
            umtext.set("")
            last_msg.set("/cls")
        elif ufds == "exits":
            textfield.config(state=NORMAL)

            textfield.insert(END, "경고! 불법 키워드입니다. 도움을 원하신다면 /?를 쳐보세요.")
            textfield.config(state=DISABLED)


        elif cmd != "/ban" or "/warn" or "/private" or "/kick":


            sendmsg(ufds)
            last_msg.set(ufds)
    else:
        if cmd == "/warn":
            sendmsg("[WARN]`%s`%s`%s"%(arg1,arg2,userid))

        elif cmd == "/kick":
            sendmsg("[KICK]`%s`%s`%s"%(arg1, arg2, userid))
        else:
            textfield.config(state=NORMAL)
            textfield.insert(END,"존재하지 않는 명령입니다. 도움을 언하신다면 /?를 쳐보세요")
            textfield.config(state=DISABLED)

def now():
    return time.asctime(time.localtime())

def sendmsg(asd):


    msg2 = "%s"%(asd)
    realmsg = msg2.encode("utf-8")

    ucs2.send(realmsg)
    umtext.set("")
    print("msg sent")


def doexit():
    sendmsg("exits")
    textfield.config(state=NORMAL)
    textfield.insert(END, "Exiting...\n")
    textfield.config(state=DISABLED)
    time.sleep(2)
#    fads.terminate()
    ucs2.close()
    root.quit()

def warningissuer(msgs):
    print("Attempted to warn in warningissuer function. Recieved", msgs)
    showwarning("Warning from server", "You have recieved a warning from the server:\n%s"%(msgs))
def new_msg():
    try:


        while True:

            msg = ucs2.recv(2096)

            msg2 = msg.decode("utf-8")
            print(msg2)
            iscmd = False
            try:
                cmd = msg2.split("`")[0]
                arg1 = msg2.split("`")[1]
                arg2 = msg2.split("`")[2]
                print(cmd+","+arg1+","+arg2)
            except:
                try:
                    iscmd = True
                    fds = json.loads(msg2)
                    print("try json loop")
                    onlinelistbox.delete(0,END)
                    for i in fds:
                        onlinelistbox.insert(END, i)
                except:
                    pass

            else:



                if cmd == "[KICK]":
                    iscmd = True
                    if userid == arg1:
                        textfield.config(state=NORMAL)
                        textfield.insert(END, "서버(혹은 관리자)으로부터 강퇴당했습니다. 이유: %s\n"%(arg2))

                        sendmsg("exits")
                        ucs2.close()

                        textfield.insert(END, "이 창은 5초 후 종료됩니다.\n")
                        textfield.config(state=DISABLED)
                        time.sleep(5)
                        root.quit()
                elif cmd == "[WARN]":
                    iscmd = True
                    if userid == arg1:
                        print("Reached(warn)")
                        thread.start_new_thread(warningissuer, (arg2))
                    else:
                        pass
                elif cmd == "[MSG]":

                    iscmd = True


                    textfield.config(state=NORMAL)

                    textfield.insert(END, arg1+"\n")
                    textfield.config(state=DISABLED)
                elif cmd == "[idkidkidkidkidk]":
                    print("reachednew_msg handler")
                    iscmd = True

                    print(arg1)
                    asd = json.loads(arg1)
                    #f = arg1.strip("[")
                    #bg = f.strip("]")
                    onlinelistbox.delete(0,END)
                    print("reached userlist")
                    for i in asd:
                        print("reached")
                        onlinelistbox.insert(END, i)

                    #for fd in bg:
                        #lsitnum = 0
                        #fd = bg.split(", ")[lsitnum]

                       # lsitnum += 1





                    print("passed spawn of getuserslist")






                else:
                    pass
            print(iscmd)
            if msg2 == "close_from_Server_fhaheAfsdhF":
                print("Recieved close")
                sendmsg("exits")
                ucs2.close()
                textfield.config(state=NORMAL)
                textfield.insert(END, "서버로부터 종료. 2초후 클라이언트는 종료됩니다.")
                textfield.config(state=DISABLED)
                time.sleep(2)
                root.quit()

            if iscmd != True:
                textfield.config(state=NORMAL)
                print(msg2)
                textfield.insert(END, msg2+"\n")
                textfield.config(state=DISABLED)
    except:
        pass

def listen():
    textfield.insert(END, "Message listner ready. Use enter to submit. Type /? for commands.\n")
    totext.bind("<Return>", checkmsg)

def warnexit():
    showerror("종료 경고", "/exit 명령을 이용하여 종료해주세요")
def start_server():
    try:
        global ucs2
        textfield.config(state=NORMAL)
        textfield.insert(END, "채팅서버에 연결중\n")
        textfield.config(state=DISABLED)
        ucs2 = socket.socket()
        ucs2.connect(server_add)
    except Exception:

        showerror("","%s 서버 접속에 실패했습니다. 다시 시도해주세요."%(str(server_add)))



        root.quit()

    else:
        textfield.config(state=NORMAL)
        textfield.insert(END, "Success!\n")
        textfield.config(state=DISABLED)
        get_creds()
        root.protocol("WM_DELETE_WINDOW", warnexit)
        listen()
        thread.start_new_thread(new_msg, ())
def Onregister():
    try:
        print(identered.get(), passentered.get())
        if identered.get() == "" or passentered.get() == "":
            raise SyntaxError

    except:
        showinfo("","회원가입은 입력창에 원하시는 ID와 비밀번호를 입력후 회원가입을 눌러주세요")
    else:
        fasdf = "Register`%s`%s"%(identered.get(),passentered.get())
        ucs2.send(fasdf.encode("utf-8"))
        loginwindow.destroy()
def Onlogin(fsdasd):
    global userid
    userid = identered.get()
    asdfa = "Login`%s`%s"%(identered.get(),passentered.get())
    ucs2.send(asdfa.encode("utf-8"))
    loginwindow.destroy()
#    global fads
#    fads = multiprocessing.Process(target=getusers, args=(ucs2,))
#    fads.start()





#def getusers(whatsthedefaultsocket):
#    while True:
#
#        time.sleep(5)
#        tfse = "gettheidbrofromtheserveryouknowthat`asd`asdf`asdf".encode()
#        whatsthedefaultsocket.sendall(tfse)


def get_creds():
    global loginwindow, identered
    loginwindow = Toplevel()

    loginwindow.title("chat login")
    loginwindow.grab_set()
    loginwindow.focus_set()
    loginwindow.resizable(0,0)
    loginwindow.protocol("WM_DELETE_WINDOW", nothing)
    global identered, passentered
    identered = StringVar()
    passentered = StringVar()
    Label(loginwindow, text="ID").grid(row=1,column=1)
    las = Entry(loginwindow, textvariable=identered)
    las.grid(row=1, column=2)
    Label(loginwindow, text="비밀번호").grid(row=2,column=1)
    openaswin = Entry(loginwindow, textvariable=passentered,show="*")
    openaswin.grid(row=2,column=2)
    openaswin.bind("<Return>", Onlogin)
    Button(loginwindow, text="회원가입", command = Onregister).grid(row=3,column=1)
    Button(loginwindow, text="로그인", command=lambda: Onlogin("as")).grid(row=3, column=2)
    las.focus_set()
def log_text(msg):
    # This function MUST be run after calling root and add_widget() or will throw a NameError
    textfield.config(state = DISABLED)
    textfield.insert(END, msg)
    textfield.config(state = NORMAL)

def get_setup():

    try:
        data_setup = codecs.open("clientsetup.properties", "r", "utf-8")
        data_setup.close()
    except:
        os.system("echo 셋업파일 생성중")
        asfd = open("clientsetup.properties", "w", encoding="utf-8")
        asfd.write(defaultsetupfile)
        asfd.close()
        try:
            os.mkdir("tmp")
        except:
            pass

        time.sleep(5)
        os.system("echo 완료했습니다. 프로그램을 재시작 해주세요.")
        os.system("pause")
        sys.exit()
    else:
        fdd  = open("clientsetup.properties", encoding="utf-8")
        fdas = fdd.read().replace(u'\ufeff', '')
        exec(fdas)

class myThread (threading.Thread):
    def __init__(self, threadID, name, lists):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.lists = lists

    def run(self):
        print("hey process worked!!")

        f = self.lists.strip("[")
        bg = f.strip("]")
        onlinelistbox.delete(0,END)
        print("reached userlist")

        for fd in bg:
            lsitnum = 0
            fd = bg.split(", ")[lsitnum]

            lsitnum += 1

if __name__ == "__main__":
    import json


    print("Chatclient v1.3")
    print("Initiating libraries")
    print("Downloading defenitions")

    fsd = socket.gethostbyname(socket.gethostname())
    print("Geolocating {0}".format(fsd))
    """print("Connecting to freegoip.net...")



    # Automatically geolocate the connecting IP
    url = 'http://freegeoip.net/json/'
    try:
        luk = urlopen(url)
        f = luk.read().decode()
        a = f.rstrip()
        g = ast.literal_eval(a)
        print(g["country_code"])
    except:
        print("Location could not be determined automatically")
    """
    print("Starting client... ")

    get_setup()
    global root

    root = Tk()
    root.after(3000, add_widget)
    root.after(5000, start_server)






    root.mainloop()