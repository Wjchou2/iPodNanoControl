from nanobtcontrol import IPodNano
import time

ipod = IPodNano()
ipod.scan("hi")
print("found ipod: " + ipod.get_name)
time.sleep(2)
# ipod.connect()
while True:
    ipod.play()
    time.sleep(1)
    ipod.pause()
    time.sleep(1)
