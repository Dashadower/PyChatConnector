# -*- coding:utf-8 -*-

from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter.messagebox import *
import threading,random,sys
from tkinter.simpledialog import *
from urllib.request import urlopen
class Chatclient(Tk):
    def __init__(self,parent=None):
        Tk.__init__(self)
        self.parent = parent
        self.svr_addr = StringVar()
        self.svr_port = StringVar()

        self.chattext = StringVar()
        self.line = 1.0
        sys.path.append("Lang")
        self.language = "English"
        try:
            __import__(self.language)

        except ImportError:
            self.language = "English"
            showerror("Chatclient",self.get_localization("ERR_LANG_IMPORT_FAIL"))

        self.entry = Entry(self,textvariable=self.chattext)
        self.entry.pack(side=BOTTOM,fill=X)
        self.text = Text(self,relief=SUNKEN)
        self.scrollbar = Scrollbar(self)
        self.scrollbar.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y, anchor=NE)
        self.text.pack(fill=BOTH,expand=YES)
        self.entry.bind("<Return>",self.handler)


        self.menubar = Menu(self)
        self.FileMenu = Menu(self.menubar,tearoff=0)
        self.FileMenu.add_command(label=self.get_localization("Connect"),command=self.connectdialog)
        self.menubar.add_cascade(label=self.get_localization("File"), menu=self.FileMenu)
        self.config(menu=self.menubar)
    def connectdialog(self):
        global ctopLevel
        ctopLevel = Toplevel()
        ctopLevel.title("Chatclient")
        ctopLevel.attributes("-toolwindow",1)
        ctopLevel.protocol("WM_DELETE_WINDOW",self.nothing)
        ctopLevel.focus_set()
        ctopLevel.grab_set()

        Label(ctopLevel,text=self.get_localization("Connect_Description")).grid(row=1,column=1,columnspan=2)
        Label(ctopLevel,text=self.get_localization("Address")).grid(row=2,column=1)
        Entry(ctopLevel,textvariable=self.svr_addr).grid(row=2,column=2)
        Label(ctopLevel,text=self.get_localization("Port")).grid(row=3,column=1)
        Entry(ctopLevel,textvariable=self.svr_port).grid(row=3,column=2)
        Button(ctopLevel,text=self.get_localization("Cancel"),command=self.cancelconnection).grid(row=4,column=1)
        Button(ctopLevel,text=self.get_localization("Confirm"),command=self.OnConnect).grid(row=4,column=2)
    def get_localization(self,key):
        return str(__import__(self.language).Langdata[key])
    def cancelconnection(self):
        pass
    def OnConnect(self):
        ctopLevel.destroy()
        if self.svr_addr.get() == "httpchat":
            self.inserttext("Connecting to the official http chat server...")
            self.httpserver_ask_username()
    def httpserver_ask_username(self):
        while True:
            uname = askstring("Chatclient",self.get_localization("ASK_HTTP_USERNAME"))
            if uname != None:
                break

        self.server_type = "http"
        self.httpserver_username = uname
        self.sendmsg_handler = self.http_sendmsg_handler
        self.httpserver_lastrecvmsg = None
        self.httpserver_initiate()

    def httpserver_initiate(self):
        g = CommonThreadHandler(self.http_msg_reciever)
        g.start()
    def http_msg_reciever(self):
        data = urlopen("http://dashadower-1.appspot.com/chatget")
        if data == self.httpserver_lastrecvmsg:
            pass
        else:
            self.inserttext(data.read())

        time.sleep(0.5)
    def http_sendmsg_handler(self,msg):
        urlopen("http://dashadower-1.appspot.com/chatrecieve?q=%s"%("[MSG] %s %s"%(self.httpserver_username,str(msg))))
    def nothing(self):
        passs
    def inserttext(self,msg):
        self.text.config(state=NORMAL)
        self.text.insert(END,msg.decode("utf-8")+"\n")
        self.text.see(END)
        self.text.config(state=DISABLED)
    def insert(self,msg):
        self.text.config(state=NORMAL)
        fg = msg.split(" ")[0]
        bg= msg.split(" ")[1]
        mgs = msg.split(" ")[2:]
        print("fg:"+fg+" bg:"+bg+" message is:"+str(mgs))
        mgs2 = " ".join(mgs)
        length = len(mgs2)
        tag_name = str(random.randint(1,1000000000))
        self.text.insert(END,mgs2+"\n")
        self.text.tag_add(tag_name,self.line,float(self.line+float("0.%s"%(str(length)))))
        self.text.tag_config(tag_name,foreground=fg,background=bg)
        self.text.see(END)
        self.text.config(state=DISABLED)
        self.chattext.set("")
        self.line += 1.0
        self.update()



    def handler(self,event):
        self.http_sendmsg_handler(self.chattext.get())
        self.chattext.set("")





################################################################################
class CommonThreadHandler(threading.Thread):
    def __init__(self,function):
        threading.Thread.__init__(self)
        self.function = function

    def run(self):

        self.function()

a = Chatclient()
a.mainloop()

