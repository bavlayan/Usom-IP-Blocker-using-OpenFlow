import Constants
from MyToplogy import MyToplogy

#-------------------- Mininet packages --------------------
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.link import TCLink, OVSLink
#-------------------- Mininet packages --------------------

def run_topo():
    topo = MyToplogy(4)
    net = Mininet(topo, build=False)
   
    net.addController(name='c0', controller=RemoteController, link=OVSLink, ip=Constants.CONTROLLER_IP, port=Constants.CONTROLLER_PORT)
    net.start()
    net.addNAT().configDefault()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    net.pingAll()
    CLI(net)
    net.stop()

if __name__ == "__main__":
    setLogLevel('info')
    run_topo()
