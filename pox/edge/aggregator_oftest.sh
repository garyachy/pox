#!/bin/bash
num=8
echo Adding $num veth interfaces

ip link add type veth

for x in $(seq 0 $((num-1))); do
  ifconfig veth$x up
  ifconfig veth$x 192.16.0.1$x
done

ovs-vsctl add-port s1 veth0
ovs-vsctl add-port s1 veth2
ovs-vsctl add-port s2 veth4
ovs-vsctl add-port s2 veth6

