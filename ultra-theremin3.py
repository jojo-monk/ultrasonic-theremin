from gpiozero import DistanceSensor
from pyo import *
pyoserver = Server(sr=48000, nchnls=2, duplex=0, audio="jack", jackname="pyo")
pyoserver.setJackAuto(False, True)
#pyoserver.setJackAutoConnectOutputPorts(system:playback_1)
pyoserver.boot()
pyoserver.start()
pyoserver.amp = 0.5
sensor = DistanceSensor(echo=17, trigger=4, max_distance=1, queue_len=10)


amp = SigTo(value=0.3, time=0.05, init=0.3)
gliss = SigTo(value=200, time=0.025, init=200)
a = SineLoop(freq=gliss, feedback=0.08, mul=amp).out()
b = SineLoop(freq=gliss*1.005, feedback=0.08, mul=amp).out()
rev = Freeverb([a, b]).out()


def capteur():
    pitch = round(sensor.distance * 80 + 30, 4)
    pitch = 110 - pitch
    print("distance : ", sensor.distance, "m")    
    if sensor.distance > 1:
        amp.value = 0.0
    amp.value = 0.3
    print(pitch)
    f = midiToHz(pitch)
    gliss.value = f

    
pat = Pattern(capteur, 0.025).play()

#pyoserver.gui(locals())

