#!/usr/bin/env python3
# encoding: UTF-8
"version à 2 capteurs, 1 pour la fréquence, et l'autre pour l'amplitude"
from gpiozero import DistanceSensor
from pyo import *
pyoserver = Server(sr=48000, nchnls=2, duplex=0, audio="jack", jackname="pyo")
pyoserver.setJackAuto(False, True)
#pyoserver.setJackAutoConnectOutputPorts(system:playback_1)
pyoserver.boot()
pyoserver.start()
pyoserver.amp = 0.3
sensor1 = DistanceSensor(echo=17, trigger=4, max_distance=1)
sensor2 = DistanceSensor(echo=22, trigger=27, max_distance=1)
amp = SigTo(value=0.3, time=0.025, init=0.3)
gliss = SigTo(value=200, time=0.025, init=200)
a = SineLoop(freq=gliss, feedback=0.08, mul=amp).out()
b = SineLoop(freq=gliss*1.005, feedback=0.08, mul=amp).out()
rev = Freeverb([a, b]).out()


def CapteurF():
    pitch = round(sensor1.distance * 80 + 30, 4)
    pitch = 110 - pitch
    print("dist1 : ", sensor1.distance, "m")    
   # if sensor1.distance > 1:
    #    amp.value = 0.0
    #amp.value = 0.3
    print(pitch)
    f = midiToHz(pitch)
    gliss.value = f

def CapteurA():
    env = round(sensor2.distance, 4)
    env = 1 - env
    print("dist2 : ", sensor2.distance)
    print("amp: ", env)
    if sensor2.distance > 1:
        amp.value = 0.0
    amp.value = env
    
pat1 = Pattern(CapteurA, 0.05).play()
pat2 = Pattern(CapteurF, 0.05).play()

