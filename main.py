from subprocess import call

from UsomUrlHelper import UsomUrlHelper
from MyToplogy import MyToplogy

#-------------------- Mininet packages --------------------
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.link import TCLink, OVSLink
#-------------------- Mininet packages --------------------


#-------------------- CONSTANTS --------------------
CONTROLLER_IP = '127.0.0.1'
CONTROLLER_PORT = 6653
OPENFLOW_PROTOCOL = 'OpenFlow13'
IP_BASE = "10.0.88.0/24"
#-------------------- CONSTANTS --------------------

def create_blocked_url_list():
    usomurlhelper = UsomUrlHelper()
    usomurlhelper.get_blocked_urls_from_usom()
    usomurlhelper.set_ip()

def topo_test():
    topo = MyToplogy(4)
    net = Mininet(topo, ipBase=IP_BASE, build=False)
    net.addController(name='c0', controller=RemoteController, link=TCLink, ip=CONTROLLER_IP, port=CONTROLLER_PORT)

    net.start()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    net.pingAll()
    h1 = net.get('h1')
    CLI(net)
    #print( "Host", h1.name, "has IP address", h1.IP(), "and MAC address", h1.MAC() )
    net.stop()

if __name__ == "__main__":
    setLogLevel('info')
    topo_test()

    