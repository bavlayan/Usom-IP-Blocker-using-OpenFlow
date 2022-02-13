# Usom IP Blocker using OpenFlow

### What is OpenFlow Protocol?
The OpenFlow (OF) protocol is a standard in software-defined networking (SDN) architecture. This protocol defines the communication between an SDN controller and the network device/agent. 

### What is SDN?
Software-Defined Networking (SDN) is an approach to networking that uses software-based controllers or application programming interfaces (APIs) to communicate with underlying hardware infrastructure and direct traffic on a network.

### The Aim of Project
The aim of Usom IP Blocker project prevents all packets that request from host to blocked urls in topology which pictured below. 

### Topology Structure
![Topo Image](Topo.png)


## Start Setup

### SDN Controller
```bash
sudo ryu-manager SDNSwitch.py
```

### Mininet Topology
```bash
sudo python3 MyTopology.py
```
