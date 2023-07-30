#!/usr/bin/env python3

# Use iperf3 to measure downstream Internet speed
# needed binaries: iperf3, ping, python3
# works on Linux

import os, random, sys

from subprocess import Popen, PIPE


iperf3_servers = [
    "ams.speedtest.clouvider.net",
    "la.speedtest.clouvider.net",
    "fra.speedtest.clouvider.net",
    "ash.speedtest.clouvider.net",
    "nyc.speedtest.clouvider.net",
    "speedtest.uztelecom.uz",
    "proof.ovh.net",
    # "iperf.worldstream.nl",
]


def run_cmd(cmd):
    try:
        process = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
    except:
        return None, None
    (output, err) = process.communicate()
    output = output.decode("utf-8")
    if err:
        err = err.decode("utf-8")
    exit_code = process.wait()
    return output, err


def run_iperf3_speedtest(servername, iptype=4):
    if iptype not in [4, "4", 6, "6"]:
        # wrong input
        iptype = 4
    print("iptype", iptype)
    speed = 0
    ports = list(range(5200, 5210))  # not including 5210
    for _ in range(5):  # max 5 tries
        serverport = random.choice(ports)
        ports.remove(serverport)  # do not try that port again
        # print(ports)
        """
        cmd = "iperf3 -R -P15 -p {port} -t3 -{ipv46} --connect-timeout 300 --format m -c {server}".format(
            port=serverport, ipv46=iptype, server=servername
        )
        """
        # run iperf3: Reverse (as receiver) 15 processes, p, max 3 seconds, format m (MBps)
        cmd = "iperf3 -R -P15 -p {port} -t3 -{ipv46} --format m  -c {server}".format(
            port=serverport, ipv46=iptype, server=servername
        )
        print(cmd)
        output, err = run_cmd(cmd)
        if not err:
            for thisline in output.split("\n"):
                """
                [SUM]   3.00-4.00   sec  12.2 MBytes   102 Mbits/sec
                [SUM]   4.00-5.00   sec  11.2 MBytes  94.4 Mbits/sec
                [SUM]   0.00-5.15   sec  65.2 MBytes   106 Mbits/sec  242             sender
                [SUM]   0.00-5.00   sec  58.3 MBytes  97.8 Mbits/sec                  receiver
                """
                if "SUM" in thisline and "receiver" in thisline:
                    speed = thisline.split()[5]
                    return speed  # speed found, so we're done
        else:
            # print("ERROR:", err)
            # print("output", output)
            if "unable to send control message: Bad file descriptor" in err:
                # network problem. to do: what if no IPv6?
                print("next loop")
            elif "the server is busy running a test. try again later" in err:
                print("next loop")
    return speed


def pingtime(servername):
    cmd = "ping -c5 -i0.1 -4 " + servername  # 5 pings, with 0.1 sec interval, ipv4
    output, err = run_cmd(cmd)
    if err:
        print("ping error:", err)
    else:
        output = output.split("\n")
        output.reverse()
        for line in output:
            if line.startswith("rtt"):
                # rtt min/avg/max/mdev = 9.456/11.311/14.155/1.599 ms
                pingtime = float(line.split("/")[-3])  # pick avg (average)
                break
    return pingtime


def quickest_server():
    # find iperf3 servers with smallest ping time ... probably closest to client
    fastest_pingtime = 1000000.0
    for server in iperf3_servers:
        server_pingtime = pingtime(server)
        print(server, int(server_pingtime), "msec")
        if server_pingtime < fastest_pingtime:
            fastest_pingtime = server_pingtime
            fastest_server = server
    return fastest_server


### Main


# To do: check iperf3 and ping are there


if (None, None) == run_cmd("ping"):
    print("no ping found")
    sys.exit(0)

if (None, None) == run_cmd("iperf3"):
    print("no iperf3 found")
    sys.exit(0)


print("Starting")
fastest_server = quickest_server()
print("Fastest iperf3 server:", fastest_server)
ipv4_speed = run_iperf3_speedtest(fastest_server)
ipv6_speed = run_iperf3_speedtest(fastest_server, 6)
print("Speeds (Mbps), IPv4 resp IPv6:", ipv4_speed, ipv6_speed)
print("Done")
