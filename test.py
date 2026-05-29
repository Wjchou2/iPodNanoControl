from nanobtcontrol import IPodNano
import time

ipod = IPodNano()
# search = input("ipodname")
ipod.scan("iPod")
if ipod.get_mac():
    print(ipod.get_name())
    time.sleep(2)
    ipod.connect()
    ipod.stop()
    print("Stopping")
    time.sleep(2)

    while True:
        ipod.next()
        print(ipod.track())
        time.sleep(0.1)

else:
    print("failed to find ipod with name: ")
