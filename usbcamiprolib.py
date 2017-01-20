
import usb.core
import sys

def writeline(filename ,line):
    with open(filename, 'a') as file:
        file.write(line + '\n')
        file.close()









def open_usb_camipro(marque):
    if marque is "Baltec":
        return Baltec()
    if marque is "Elatec" :
        return Elatec()
    raise Error("Marque inconnue : " + marque)

class Elatec(object):

    def read(self):
        #Elatec
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
                            i = "".join([ (chr(d) if d >= 31 else "") for d in data])
                            writeline('pyusb',i )
                            o.append(i)
                            print o[:]

            except usb.core.USBError as e:
                print e
                break

class Baltec(object):
    def read(self):
            # Elatech:
            idVendor  = 0x13ad
            idProduct = 0x9cab
            interface = 0
            timeout_secs = 5

            dev = usb.core.find(idVendor=idVendor, idProduct=idProduct)
            if (dev is None):
                print ("Aucun lecteur !!!")
                sys.exit()
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
                            data = ep.read(ep.wMaxPacketSize * 4, timeout_secs * 1000)
                            o = []
                            i = "".join([ (chr(d) if d >= 31 else "") for d in data])
                            writeline('pyusb',i )
                            o.append(i)
                            print o[:]

                except usb.core.USBError as e:
                    print e
                    break
