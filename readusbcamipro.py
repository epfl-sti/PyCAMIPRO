from usbcamiprolib import open_usb_camipro

baltec = open_usb_camipro("Baltec")
print baltec
print "baltec.read"
baltec.read()

elatec = open_usb_camipro("Elatec")
print elatec
print "elatec.read"
elatec.read()
