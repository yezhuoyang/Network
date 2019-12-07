#!/usr/bin/env python


from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.node import OVSController


class AssignmentNetworks(Topo):
    def __init__(self, **opts):
        Topo.__init__(self, **opts)
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')
        h7 = self.addHost('h7')
        h8 = self.addHost('h8')
        h9 = self.addHost('h9')
        h10 = self.addHost('h10')
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')
        s6 = self.addSwitch('s6')
        self.addLink(h1, s1)
        self.addLink(h7, s1)
        self.addLink(h8, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s3)
        self.addLink(h4, s4)
        self.addLink(h9, s4)
        self.addLink(h10, s4)
        self.addLink(h5, s5)
        self.addLink(h6, s6)
        self.addLink(s1, s2, bw=20, delay='40ms')
        self.addLink(s2, s3, bw=40, delay='10ms')
        self.addLink(s3, s4, bw=30, delay='30ms')
        self.addLink(s2, s5, bw=25, delay='5ms')
        self.addLink(s3, s6, bw=25, delay='5ms')



def Q1(net):
    def H(x):
        return net.hosts[x-1]
    def S(x):
        return net.switches[x-1]    
    S(1).cmd("ping %s -c 20 >latency_L1.txt"%S(2).IP())
    S(2).cmd("ping %s -c 20 >latency_L2.txt"%S(3).IP())
    S(3).cmd("ping %s -c 20 >latency_L3.txt"%S(4).IP())
    S(2).cmd("ping %s -c 20 >latency_L4.txt"%S(5).IP())
    S(3).cmd("ping %s -c 20 >latency_L5.txt"%S(6).IP())
    
    S(2).cmd("java Iperfer -s -p 5000")
    S(1).cmd("java Iperfer -c -h %s -p 5000 -t 20 > throughput_L1.txt"%S(2).IP())
    
    S(3).cmd("java Iperfer -s -p 5000")
    S(2).cmd("java Iperfer -c -h %s -p 5000 -t 20 > throughput_L2.txt"%S(3).IP())

    S(4).cmd("java Iperfer -s -p 5000")
    S(3).cmd("java Iperfer -c -h %s -p 5000 -t 20 > throughput_L3.txt"%S(4).IP())

    S(5).cmd("java Iperfer -s -p 5000")
    S(2).cmd("java Iperfer -c -h %s -p 5000 -t 20 > throughput_L4.txt"%S(5).IP())

    S(6).cmd("java Iperfer -s -p 5000")
    S(3).cmd("java Iperfer -c -h %s -p 5000 -t 20 > throughput_L5.txt"%S(6).IP())
    return



if __name__ == '__main__':
    setLogLevel( 'info' )
    # Create data network
    topo = AssignmentNetworks()
    net = Mininet(topo=topo, controller=OVSController, link=TCLink, autoSetMacs=True,
           autoStaticArp=True)
    # Run network
    net.start()
    Q1(net)
    net.stop()

