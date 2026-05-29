from nanobtcontrol import IPodNano
import time

ipod = IPodNano()
search = input("ipodname")
ipod.scan(search)
if ipod.get_mac:
    print("found ipod: " + ipod.get_name())
    time.sleep(2)
    ipod.connect()
    while True:
        ipod.play()
        time.sleep(1)
        ipod.pause()
        time.sleep(1)
else:
    print("failed to find ipod with name: " + search)
