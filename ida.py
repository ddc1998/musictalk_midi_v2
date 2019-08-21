import random
from mido import MidiFile
from mido import Message
import time, os, sys, requests, random
import threading
import numpy as np
import pygame as pg
import dan
import dai
### The register server host, you can use IP or Domain.
host = 'iottalk2.tw'

### [OPTIONAL] The register port, default = 9992
# port = 9992

### [OPTIONAL] If not given or None, server will auto-generate.
# device_name = 'Dummy_Test'

### [OPTIONAL] If not given or None, DAN will register using a random UUID.
### Or you can use following code to use MAC address for device_addr.
# from uuid import getnode
# device_addr = "{:012X}".format(getnode())
#device_addr = "aa8e5b58-8a9b-419b-b8d5-72624d61108d"

### [OPTIONAL] If not given or None, this device will be used by anyone.
username = 'A'

### The Device Model in IoTtalk, please check IoTtalk document.
device_model = 'Music_midi'

### The input/output device features, please check IoTtalk document.
idf_list = ['Note']
odf_list = ['Note_o']

### Set the push interval, default = 1 (sec)
### Or you can set to 0, and control in your feature input function.
usr_interval = 0

push_interval = 0  # global interval
interval = {
    'Note': 0,  # assign feature interval
}

def register_callback():
    print('register successfully')

music_file = "魔法公主主題曲-VK.mid"

class ColorMapping:
    def __init__(self):
        """
        F#: (145, 25, 62) -> purple-red(?), 6
        G: (174, 0, 0) -> dark read, 7
        G#: (255, 0, 0) -> red, 8
        A: (255, 102, 0) -> orange-red, 9
        B-: (255, 239, 0) -> yello, 10
        B: (155, 255, 0) -> chartreuse, 11
        C: (40, 255, 0) -> lime, 0
        C#: (0, 255, 242) -> aqua, 1
        D: (0, 122, 255) -> sky blue, 2
        D#: (5, 0, 255) -> blue, 3
        E: (71, 0, 237) -> blue-indigo, 4
        F: (99, 0, 178) -> indigo, 5
        """
        note = []
        for i in range(128):
            note.append(i % 12)
        self.note_color_map = note.copy()
        self.color_map = [[40, 255, 0], [0, 255, 242], [0, 122, 255], [
            5, 0, 255
        ], [71, 0, 237], [99, 0, 178], [145, 25, 62], [174, 0, 0], [255, 0, 0],
                          [255, 102, 0], [255, 239, 0], [155, 255, 0]]

    def get_note_color(self, note):
        note_to_color = self.note_color_map[note]
        return self.color_map[note_to_color]


class MidiMessage:
    def __init__(self, msg_str):
        self.msg = msg_str.split()  #split string into a list
        # self.msg = msg_str

    def channel(self):
        """ Get channel attribute """
        if (self.msg[0] != 'program_change'):
            target = self.msg[1]
            idx = target.find('=')
            # print(target[idx + 1:])
            return int(target[idx + 1:])

    def note(self):
        """ Get note attribute """
        if (self.msg[0] != 'program_change'):
            target = self.msg[2]
            idx = target.find('=')
            # print(target[idx + 1:])
            return int(target[idx + 1:])

    def velocity(self):
        """ Get velocity attribute """
        if (self.msg[0] != 'program_change'):
            target = self.msg[3]
            idx = target.find('=')
            # print(target[idx + 1:])
            return int(target[idx + 1:])

    def time(self):
        """ Get time attribute """
        if (self.msg[0] != 'program_change'):
            target = self.msg[4]
            idx = target.find('=')
            # print(target[idx + 1:])
            return float(target[idx + 1:])

""" fetch message from music file and get music features """


time_sleep_list = []
color_list =[]
time_tmp = 0
def ToDoList(music_file):
    global time_tmp
    midi_file = MidiFile(music_file)
    note_color = ColorMapping()
    for msg in midi_file:
        # print(dir(msg))
        # exit()
        #time_sleep_list.append(msg.time)
        time_tmp += msg.time
        if not msg.is_meta:
            # print(msg)
            str_msg = str(msg)
            mid = MidiMessage(str_msg)
            if mid.channel() == 0:
                # print(str_msg)
                # print('note:', mid.note())
                # print('velocity: ', mid.velocity())
                if mid.velocity() > 0:
                    #print('total time:', time_tmp)
                    time_sleep_list.append(time_tmp)
                    time_tmp = 0
                    color = note_color.get_note_color(mid.note())
                    #print('color:', color)
                    color_list.append(color)

ToDoList(music_file)
                    
seq = 0
def Note():    	
    global time_sleep_list, color_list, seq
    while (seq < len(color_list)):
        time.sleep(time_sleep_list[seq])
        seq += 1
        #print (color_list[seq-1])
        # str1 = ','.join(str(i) for i in color_list[seq-1])
        print('color list:', color_list[seq-1])
        # print([i for i in color_list[seq-1]])
        # str2 = str(time_sleep_list[seq-1])+','+str1
        # print (str2)
        #return color_list[seq-1]
        # seq += 1
        return color_list[seq-1]
        # return 1

'''
def Dummy_Sensor():
    return random.randint(0, 100)
    # return NoData
'''

def Note_o(data):  # data is a list
    print (data)
    return 0
'''

    while (DAN.state != 'SET_DF_STATUS'):
        # wait for DAN ready
        time.sleep(0.1)
    """ play music """
    
    """ push feature data """
    job_of_music_feature(music_file)
'''