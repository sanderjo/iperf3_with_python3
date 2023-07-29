# iperf3_with_python3
Use iperf3 from python3 to measure Internet speed

The tool first finds the iperf3 server with the lowest ping time, and then uses the iperf3 server to measure IPv4 and IPv6 speed


Example, on a 2500 Mbps connection:

```
$ ./iperf3_with_python3.py 
Starting
ams.speedtest.clouvider.net 11 msec
la.speedtest.clouvider.net 134 msec
fra.speedtest.clouvider.net 10 msec
ash.speedtest.clouvider.net 87 msec
speedtest.uztelecom.uz 96 msec
proof.ovh.net 10 msec
Fastest iperf3 server: fra.speedtest.clouvider.net
iptype 4
iperf3 -p 5207 -t3 -4 --connect-timeout 300 --format m -c fra.speedtest.clouvider.net
SPEED: 2285 Mbps
iptype 6
iperf3 -p 5201 -t3 -6 --connect-timeout 300 --format m -c fra.speedtest.clouvider.net
SPEED: 2220 Mbps
Done
```

To use on UbuntuDocker:

```
apt update
apt install python3 iperf3 wget iputils-ping -y
wget https://raw.githubusercontent.com/sanderjo/iperf3_with_python3/main/iperf3_with_python3.py
python3 iperf3_with_python3.py
```
