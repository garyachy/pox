#!/bin/bash
num=$1
echo Adding tunnels for $num switches
rmmod dummy
modprobe dummy numdummies=$((num+1)) 

for x in $(seq 1 $1); do
  ifconfig dummy$x 172.16.0.$x
  ovs-vsctl del-port s$x tun$x 2> /dev/null
  ovs-vsctl add-port s$x tun$x -- set Interface tun$x type=gre \
    options:remote_ip=flow options:local_ip=172.16.0.$x options:key=flow
done



