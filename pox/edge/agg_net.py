#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf

def aggNet():

    NODE1_IP='172.16.0.1'
    NODE2_IP='172.16.0.2'
    CONTROLLER_IP='127.0.0.1'

    net = Mininet( topo=None,
                   build=False)

    net.addController( 'c0',
                      controller=RemoteController,
                      ip=CONTROLLER_IP,
                      port=6633)

    h1 = net.addHost( 'h1', ip='10.0.0.1' )
    h2 = net.addHost( 'h2', ip='10.0.0.2' )
    s1 = net.addSwitch( 's1' )
    s2 = net.addSwitch( 's2' )


    net.addLink( h1, s1 )
    net.addLink( h2, s2 )

    # Create GRE tunnels
    s1.cmd('ovs-vsctl add-port s1 tun1 -- set Interface tun1 type=gre options:remote_ip=NODE2_IP options:local_ip=NODE1_IP')
    Intf( 'tun1', node=s1 )

    s2.cmd('ovs-vsctl add-port s2 tun2 -- set Interface tun2 type=gre options:remote_ip=NODE1_IP options:local_ip=NODE2_IP')
    Intf( 'tun2', node=s2 )

    net.start()
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    aggNet()
