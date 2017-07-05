
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


class CamiproAbstract(object):
    def __init__(self):
        self._endpoint = None

    def read(self):

        while True:
            try:
                i = self._read_low_level()
                o = []
                writeline('pyusb',i )
                o.append(i)
                print o[:]

            except usb.core.USBError as e:
                print e
                break

    def open_endpoint(self):
        if self._endpoint is None:
            self._endpoint = self._really_open_endpoint()
        return self._endpoint

    def _really_open_endpoint(self):
        interface = 0

        dev = usb.core.find(idVendor=self._idVendor, idProduct=self._idProduct)
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
        return ep

    def _read_low_level(self):
        """Read one CAMIPRO number out of the reader

        The result is in colon-separated hex form e.g.: "31:0f:2e:0a:00:10:05:ed"
        """
        raise NotImplementedError

class Elatec(CamiproAbstract):

    _idVendor = 0x09d8
    _idProduct = 0x0406

    def _read_low_level(self):
        timeout_secs = 10
        data = self.open_endpoint().read(self.open_endpoint().wMaxPacketSize, timeout_secs * 1000)
        elatec = "".join([ (chr(d) if d >= 31 else "") for d in data])
        elatec = ":".join([elatec[len(elatec)-2*i:][:2] for i in range(1,8)])
        return elatec



class Baltec(CamiproAbstract):

    _idVendor  = 0x13ad
    _idProduct = 0x9cab

    def _read_low_level(self):
        timeout_secs = 5
        data = self.open_endpoint().read(self.open_endpoint().wMaxPacketSize * 4, timeout_secs * 1000)
        baltec_decimal = int("".join([ (chr(d) if d >= 31 else "") for d in data]))
        baltec_hexa = "%016x" % baltec_decimal

        return ":".join([baltec_hexa[2*i:2*i+2] for i in range(0,7)])
