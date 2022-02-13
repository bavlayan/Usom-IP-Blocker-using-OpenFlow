import Constants

from mininet.topo import Topo
from mininet.node import OVSKernelSwitch
from functools import partial

class MyToplogy(Topo):
    def __init__(self, host_count=4, switch_count=3):
        Topo.__init__(self)
        self.host_count = host_count
        self.switch_count = switch_count
        self.host_list = []       
        self.switch_list =  []

        self.__create_switch()
        self.__create_host()
        self.__create_link()
    
    def __create_host(self):
        for i in range(self.host_count):
            created_host = self.addHost('h%s' % (i + 1))
            self.host_list.append(created_host)

    def __create_switch(self):
        OpenFlow14Switch = partial(OVSKernelSwitch, protocols='OpenFlow13')
        for i in range(self.switch_count):
            switch_name = 's%s' % (i + 1)
            switch_dpid = Constants.DPID_PREFIX + i + 1
            switch = self.addSwitch(switch_name, cls=OpenFlow14Switch, dpid="%x" % switch_dpid)
            self.switch_list.append(switch)

    def __create_link(self):
        self.addLink('h1', 's2')
        self.addLink('h2', 's2')
        self.addLink('h3', 's3')
        self.addLink('h4', 's3')

        self.addLink('s2', 's1')
        self.addLink('s3', 's1')   