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
#-------------------- CONSTANTS --------------------

def create_blocked_url_list():
    usomurlhelper = UsomUrlHelper()
    usomurlhelper.get_blocked_urls_from_usom()
    usomurlhelper.set_ip()

def topo_test():
    topo = MyToplogy(4)
    net = Mininet(topo, build=False)
   
    net.addController(name='c0', controller=RemoteController, link=OVSLink, ip=CONTROLLER_IP, port=CONTROLLER_PORT)
    net.start()
    #net.addNAT().configDefault()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    net.pingAll()
    CLI(net)
    net.stop()

if __name__ == "__main__":
    setLogLevel('info')
    topo_test()

    