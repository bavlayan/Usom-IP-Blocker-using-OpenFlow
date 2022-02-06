from subprocess import call

from UsomUrlHelper import UsomUrlHelper
from MyToplogy import MyToplogy

#-------------------- Mininet packages --------------------
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
#-------------------- Mininet packages --------------------

def create_blocked_url_list():
    usomurlhelper = UsomUrlHelper()
    usomurlhelper.get_blocked_urls_from_usom()
    usomurlhelper.set_ip()

def topo_test():
    topo = MyToplogy(4)
    net = Mininet(topo)
    net.start()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    net.pingAll()
    h1 = net.get('h1')
    print( "Host", h1.name, "has IP address", h1.IP(), "and MAC address", h1.MAC() )
    net.stop()

if __name__ == "__main__":
    call(["mn", "-c"])

    setLogLevel('info')
    topo_test()

    