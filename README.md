# iperf3_with_python3
Use iperf3 from python3 to measure Internet speed

The tool first finds the iperf3 server with the lowest ping time, and then uses the iperf3 server to measure IPv4 and IPv6 speed

```
$ ./iperf3_with_python3.py 
Starting
ams.speedtest.clouvider.net 10 msec
la.speedtest.clouvider.net 133 msec
fra.speedtest.clouvider.net 10 msec
ash.speedtest.clouvider.net 87 msec
speedtest.uztelecom.uz 96 msec
proof.ovh.net 9 msec
Fastest iperf3 server: proof.ovh.net
iptype 4
iperf3 -p 5200 -t3 -4 --connect-timeout 300 --format m -c proof.ovh.net
ERROR: iperf3: error - unable to send control message: Bad file descriptor

next loop
iperf3 -p 5203 -t3 -4 --connect-timeout 300 --format m -c proof.ovh.net
SPEED: 2289 Mbps
iptype 6
iperf3 -p 5206 -t3 -6 --connect-timeout 300 --format m -c proof.ovh.net
SPEED: 2261 Mbps
Done
```
