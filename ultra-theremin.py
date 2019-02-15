from gpiozero import DistanceSensor
from time import sleep
from pythonosc import osc_message_builder
from pythonosc import udp_client

sensor = DistanceSensor(echo=17, trigger=4, max_distance=1)
sender = udp_client.SimpleUDPClient('127.0.0.1', 4559)
while True:
    print("distance : ", sensor.distance, "m")
    pitch = round(sensor.distance * 100 + 27)
    print(pitch)
    sender.send_message('/play_this', pitch)
    sleep(0.2)
