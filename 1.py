import usb.core
from subprocess import call
import subprocess

# Baltech:
# idVendor  = 0x13ad
# idProduct = 0x9cab
# Elatec:
idVendor = 0x09d8
idProduct = 0x0406
interface = 0
timeout_secs = 5

dev = usb.core.find(idVendor=idVendor, idProduct=idProduct)
if dev.is_kernel_driver_active(interface) is True:
    #print "but we need to detach kernel driver"
    dev.detach_kernel_driver(interface)

dev.set_configuration()
cfg = dev.get_active_configuration()
intf = list(cfg)[0]
ep = usb.util.find_descriptor(
            intf,
            # match the first IN endpoint
            custom_match = \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_IN
        )
assert ep is not None
while True:
    try:
                    data = ep.read(ep.wMaxPacketSize, timeout_secs * 1000)
                    o = []
                    i = "".join([ (chr(d) if d >= 32 else '') for d in data])
                    o.append(i)
                    file = open("pyusb","w")
                    file.write(i)
                    file.close()
                    print o[0]
                    #   print o[1]

    except usb.core.USBError as e:
        print e
        break
    #break
