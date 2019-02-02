#! /usr/bin/python

import re
import sys
import socket

host = 'coremud.org'
port = 4000
user = ''
passwd = ''

class Director:
    def __init__(self):
        self.directions = []
        self.con = ''

    def connect(self,host,port):
        self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print "Trying %s..." % str(socket.gethostbyname(host))
            self.con.connect((host,port))
            print "Connected to " + host + " on port " + str(port) + "."
        except Exception as e:
            print 'error: ' + e

    def login(self,host,port,user,passwd):
        self.connect(host,port)
        print self.con.recv(4096)
        print self.con.recv(4096)
        self.con.send('%s\n' % user)
        print user
        print self.con.recv(4096),
        self.con.send('%s\n' % passwd)
        print self.con.recv(4096)
        print self.con.recv(4096)
#        self.con.send('get sword\n')
#        print self.con.recv(4096)
#        self.con.send('wield sword\n')
#        print self.con.recv(4096)
#        print 'down'
#        self.con.send('down\n')
#        print self.con.recv(4096)

    def logout(self):
#        self.con.send('drop sword\n')
#        print self.con.recv(4096)
        self.con.send('quit\n')
        print self.con.recv(4096)
        self.con.close()

    def info_pull(self,text):
        longd = re.search('', text)
        shortd = re.search('', text)
        coords = re.search('', text)
        moblong = re.search('', text)
        mobshort = re.search('', text)
        exits = re.search('', text)
        return longd, shortd, coords, moblong, mobshort, exits

    def battle_bot(self,cmd):
        npc = cmd[5:]
        self.con.send('%s\n' % cmd)
        while True:
            text = self.con.recv(4096)
            print text
            kill = re.search('(?i)%s falls to' % npc, text)
            die = re.search('You have died.', text)
            if kill:
                self.con.send('get potion from corpse\n')
                print self.con.recv(4096)
                self.con.send('drink potion\n')
                print self.con.recv(4096)
                break
            elif die:
                self.con.send('pray\n')
                print self.con.recv(4096)
                break

    def navigate_bot(self):
        for entry in self.directions:
            self.con.send('%s\n' % entry)
            print self.con.recv(4096)
        while True:
            cmd = raw_input('>')
            if 'kill' in cmd:
                self.battle_bot(cmd)
            elif 'quit' in cmd:
                self.logout()
                sys.exit()
            else:
                self.con.send('%s\n' % cmd)
                print self.con.recv(4096)

director = Director()
try:
    director.login(host,port,user,passwd)
    director.navigate_bot()
except (KeyboardInterrupt,Exception) as e:
    print 'Hit exception:'
    print e
    explore.logout()
