#!/usr/bin/env python

from mididings import *

config(
  backend='jack-rt',
)

Class Hdsp(object):

  def __init__(self):

    self.port = 0

    # input: 0-7 (analog), 16-23 (adat), 
    #     24-25 (spdif), 26-43 (playback)
    # output: 0-7 (analog), 16-23 (adat) 
    #     24-25 (spdif), 26-27 (line out)

    # multiface
    self.mbase = [0,0]
    self.minibrute = [1,1]
    self.lxr = [2,3]
    self.ot = [4,5]
    self.mm = [6,7]
    self.monitor = [26,27]

    # adat (adcon)
    self.emx = [16,17]
    self.restyler = [18,19]
    self.vortex = [20,21]
    self.main = [22,23]

    # in and out, same connections
    self.channels = [self.mbase, self.minibrute, self.lxr, self.ot, self.mm, self.emx, self.restyler, self.vortex]

    # playback, mirrors input
    self.playback = [[]]
    for i,c in enumerate(self.channels):
      for n in (0,1):
        self.playback[i][n] = c[n] + 26

    # start in a defined state
    self.mute
    self.playback(63) #0dB
    self.record(63)   #0dB
    self.listen

  def mute(self): # mute everything
    for i in range(43):
      for o in range(27):
        call = "amixer cset numid=5 " + i + "," + o + ",0"
        print(call)
        System(call)

  def playback(self,vol):
    # route all playback channels to main and monitor
    for channel in self.playback:
      self.volume(channel,self.main,vol)
      self.volume(channel,self.monitor,vol)

  def record(self,vol):
    # route all record channels to main and monitor
    for channel in self.channels:
      self.volume(channel,self.main,vol)
      self.volume(channel,self.monitor,vol)

  def volume(self,i,o,vol):
    #first value: input source
    #second value: output source
    #third value: gain (0 - 65535 where 32767 is 0db)
    for n in (0,1):
      call = "amixer cset numid=5 " + i[n] + "," + o[n] + "," + vol*65535/127
      print(call)
      System(call)
      # update encoder
      Ctrl(self.port, i, o, vol)

  def listen(self,ev):
    if ev.type == CTRL:
      self.volume(ev.channel,ev.ctrl,ev.value)

run(Hdsp())
