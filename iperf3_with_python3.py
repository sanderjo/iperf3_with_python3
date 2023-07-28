#!/usr/bin/env python3

# Use iperf3 (if installed) to measure Internet speed

import os, random, sys

from subprocess import Popen, PIPE


def run_cmd(cmd):
    process = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
    (output, err) = process.communicate()
    output = output.decode("utf-8")
    if err:
        err = err.decode("utf-8")
    exit_code = process.wait()
    return output, err


def run_speedtest(servername):
    for iptype in [4, 6]:
        print("iptype", iptype)
        ports = list(range(5200, 5210))  # not including 5210
        for _ in range(5):  # max 5 tries
            serverport = random.choice(ports)
            ports.remove(serverport)  # do not try that port again
            # print(ports)
            cmd = "iperf3 -p {port} -t3 -{ipv46} --connect-timeout 300 --format m -c {server}".format(
                port=serverport, ipv46=iptype, server=servername
            )
            print(cmd)
            output, err = run_cmd(cmd)
            if err:
                print("ERROR:", err)
                # print("output", output)
                if "unable to send control message: Bad file descriptor" in err:
                    # network problem. to do: what if no IPv6?
                    print("next loop")
                    # break
                    pass
            else:
                for thisline in output.split("\n"):
                    print(
                        "SPEED:", thisline.split()[-4], "Mbps"
                    ) if "sender" in thisline else None
                break


def pingtime(servername):
    cmd = "ping -c1 -4 " + servername
    output, err = run_cmd(cmd)
    if err:
        print("ping error:", err)
    else:
        # print(output.split("\n")[-2])
        output = output.split("\n")
        output.reverse()
        for line in output:
            if line.startswith("rtt"):
                pingtime = float(line.split("/")[-3])
    return pingtime


### Main


print("Starting")

# find iperf3 servers with smalled ping time ... probably closes to client
fastest_pingtime = 1000000.0
servers = [
    "ams.speedtest.clouvider.net",
    "la.speedtest.clouvider.net",
    "fra.speedtest.clouvider.net",
    "ash.speedtest.clouvider.net",
    "speedtest.uztelecom.uz",
    "proof.ovh.net",
]
for server in servers:
    server_pingtime = pingtime(server)
    print(server, int(server_pingtime), "msec")
    if server_pingtime < fastest_pingtime:
        fastest_pingtime = server_pingtime
        fastest_server = server

print("Fastest iperf3 server:", fastest_server)

run_speedtest(fastest_server)

print("Done")
