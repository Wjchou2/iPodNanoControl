from nanobtcontrol import IPodNano
import time

ipod = IPodNano()
# search = input("ipodname")
ipod.scan("iPod")
if ipod.get_mac():
    print(ipod.get_name())

    ipod.connect()
    
    # ipod.stop()
    # print("Stopping")
    # time.sleep(2)

    while True:
        # ipod.next()
        ipod.play()
        time.sleep(1)
        ipod.pause()
        time.sleep(1)

        # print(ipod.track())

else:
    print("failed to find ipod with name: ")
