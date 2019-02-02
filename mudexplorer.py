#! /usr/bin/python

import re
import time
import random
import socket

host = ''
port = 4000
user = ''
passwd = ''

class MudExplorer:
    def __init__(self):
        self.con = ''
        self.curr_dir = ''
        self.last_dir = ''
        self.last_txt = ''
        self.constr_track = 0
        self.downtrack = 0
        self.down_room = []
        self.path_taken = []
        self.lvl_dict = {
            "the uninitiated":1,
            "Uninitiated":1,
            "the newbie":2,
            "Newbie":2,
            "is getting the hang of things":3,
            "Meh":3,
            "mediocre":4,
            "Mediocre":4,
            "Sub-average":5,
            "Average":6,
            "Strong":7,
            "Great":8,
            "Baroness":9,
            "Titan":10,
            "Conquerer":11,
            "Famous":12,
            "Awe-inspiring":13,
            "Battle Hardened":14,
            "More than Adequate":15,
            "Grand Baroness":16,
            "Great Titan":17,
            "Mighty Conquerer":18,
            "High and Mighty":19,
            "Grand Wizard!!!":20
            }

    def connect(self,host,port):
        self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print "Trying %s..." % str(socket.gethostbyname(host))
            self.con.connect((host,port))
            print "Connected to " + host + " on port " + str(port) + "."
        except Exception as e:
            print "error: " + e

    def login(self,host,port,user,passwd):
        self.connect(host,port)
        print self.con.recv(4096)
        self.con.send('%s\n' % user)
        print user
        print self.con.recv(4096),
        self.con.send('%s\n' % passwd)
        print self.con.recv(4096)
        #self.con.send('get sword\n')
        #print self.con.recv(4096)
        #self.con.send('wield sword\n')
        #print self.con.recv(4096)
        print 'down'
        self.con.send('down\n')        
        print self.con.recv(4096)

    def logout(self):
        #self.con.send('drop sword\n')
        #print self.con.recv(4096)
        self.con.send('quit\n')
        print self.con.recv(4096)
        self.con.close()
        print 'Path taken:'
        print self.path_taken
        print '\n100 series rooms visited:'
        print self.down_room

    def find_stuff(self):
        exits = []
        self.con.send('look\n')
        text = self.con.recv(4096)

        #sword = re.search('A short sword', text)
        #if sword:
        #    self.con.send('get sword\n')
        #    print self.con.recv(4096)
        #    self.con.send('wield sword\n')
        #    print self.con.recv(4096)

#        exits = re.search('Obvious exits: (.+?) ]', text)
#        if exits:
#            print 'entered exits if'
#            found = exits.group(1).strip().split()
#            if len(found) == 1 and found == 'up':
#                print 'entered exits len check'
#                exits = found
#            else:
#                exits = [ s for s in found if 'up' not in s ]
#        else:
#            print exits
#            print 'No exits found.  Logging out.'
#            self.logout()

        room = re.search(' - (.+?)\n', text)
        if room:
            room = room.group(1)
        else:
            print 'Cannot determine room position.  Logging out.'
            self.logout()

        npc = re.search('  (.+?)\n', text)
        if npc:
            npc = npc.group(1).strip().split()
            if len(npc) > 2:
                self.con.send('get potion\n')
                print self.con.recv(4096)
                self.con.send('drink potion\n')
                print self.con.recv(4096)
                npc = False
        else:
            npc = False

        #self.con.send('who %s\n' % user)
        #who = self.con.recv(4096)
        #player = re.search('(?i)%s the (.+?)\n' % user, who)
        #if player:
        #    player = player.group(0).strip().split()
        #    lvl = self.lvl_dict[player[2][:-1]]
        #else:
        #    lvl = 'Cannot find player level.  Logging out.'
        #    self.logout()

        exits = re.search('Obvious exits: (.+?) ]', text)
        if exits:
            found = exits.group(1).strip().split()
            if '4-e' in room:
                exits = [ s for s in found if 'up' not in s ]
            else:
                exits = found
        else:
            print 'No exits found.  Logging out.'
            self.logout()

        #return exits,room,npc,lvl
        return exits,room,npc

    def compare_lvl(self,npc,lvl):
        curr_lvl = lvl
        tar_lvl = ''
        if npc is not False and len(npc) == 2:
            tar_lvl = self.lvl_dict[npc[0][10:]]
        else:
            return False
        print 'Player level: %i' % curr_lvl
        print 'NPC level: %i' % tar_lvl
        if curr_lvl >= tar_lvl:
            return True
        else:
            return False

    def attack_npc(self,npc):
        if npc is not False:
            self.con.send('look\r\n')
            print self.con.recv(4096)
            self.con.send('attack %s\n' % npc[1][:-4])
            print 'attack %s' % npc[1][:-4]
            while True:
                text = self.con.recv(4096)
                print text
                kill = re.search('(?i)%s falls to' % npc[1][:-4], text)
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
                    raw_input('You have died, continue?')
                    break

    def bot(self):
        while True:
            #exits,room,npc,lvl = self.find_stuff()
            exits,room,npc = self.find_stuff()
#            if self.compare_lvl(npc,lvl):
#                self.attack_npc(npc)
            for entry in exits:
                if 'down' == entry and self.downtrack == 0:
                    print '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'
                    print 'Found down'
                    print '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'
                    self.curr_dir = 'down'
                    print 'down'
                    self.con.send('%s\n' % self.curr_dir)
                    print self.con.recv(4096)
                    self.last_dir = 'down'
                    #exits,room,npc,lvl = self.find_stuff()
                    exits,room,npc = self.find_stuff()
                    print room
                    self.down_room.append(room[:-5])
                    self.downtrack += 1
                    
            if len(exits) == 1:
                self.curr_dir = exits[0]
                print self.curr_dir
                self.con.send('%s\n' % self.curr_dir)
                self.last_txt = self.con.recv(4096)
                print self.last_txt
            else:
                init_dir = random.choice(exits)
                mod = self.move_logic(init_dir,exits)
                if mod != exits:
                    if len(mod) == 1:
                        self.curr_dir = mod[0]
                        print self.curr_dir
                        self.con.send('%s\n' % self.curr_dir)
                        self.last_txt = self.con.recv(4096)
                        print self.last_txt
                    else:
                        self.curr_dir = random.choice(exits)
                        print self.curr_dir
                        self.con.send('%s\n' % self.curr_dir)
                        self.last_txt = self.con.recv(4096)
                        print self.last_txt
                else:
                    self.curr_dir = init_dir
                    print self.curr_dir
                    self.con.send('%s\n' % self.curr_dir)
                    self.last_txt = self.con.recv(4096)
                    print self.last_txt

            construction = re.search('Construction blocks your path', self.last_txt)
            if construction:
                if self.constr_track == 0:
                    self.last_dir = 'west'
                elif self.constr_track == 1:
                    self.last_dir = 'east'
                elif self.constr_track == 2:
                    self.last_dir = 'north'
                elif self.constr_track == 3:
                    self.last_dir = 'south'
                elif self.constr_track == 4:
                    self.last_dir = 'northwest'
                elif self.constr_track == 5:
                    self.last_dir = 'northeast'
                elif self.constr_track == 6:
                    self.last_dir = 'southwest'
                elif self.constr_track == 7:
                    self.last_dir = 'southeast'
                elif self.constr_track == 8:
                    self.logout()
                self.constr_track += 1
            else:
                self.last_dir = self.curr_dir
                self.constr_track = 0
            self.path_taken.append(self.curr_dir)

    def move_logic(self,init_dir,exits):
        if 'north' == init_dir and 'south' == self.last_dir:
            exits = [ s for s in exits if init_dir != s ]
            return exits
        elif 'south' == init_dir and 'north' == self.last_dir:
            exits = [ s for s in exits if init_dir != s ]
            return exits
        elif 'west' == init_dir and 'east' == self.last_dir:
            exits = [ s for s in exits if init_dir != s ]
            return exits
        elif 'east' == init_dir and 'west' == self.last_dir:
            exits = [ s for s in exits if init_dir != s ]
            return exits
        elif 'northwest' == init_dir and 'southeast' == self.last_dir:
            exits = [ s for s in exits if init_dir != s ]
            return exits
        elif 'southeast' == init_dir and 'northwest' == self.last_dir:
            exits = [ s for s in exits if init_dir != s ]
            return exits
        elif 'northeast' == init_dir and 'southwest' == self.last_dir:
            exits = [ s for s in exits if init_dir != s ]
            return exits
        elif 'southwest' == init_dir and 'northeast' == self.last_dir:
            exits = [ s for s in exits if init_dir != s ]
            return exits
        else:
            return exits
            
explore = MudExplorer()
try:
    explore.login(host,port,user,passwd)
    explore.bot()
    explore.logout()
except (KeyboardInterrupt,Exception) as e:
    print 'Hit exception:'
    print e
    explore.logout()
