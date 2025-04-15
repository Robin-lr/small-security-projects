# **sniffer.py**

A simple Python-based network traffic sniffer using **Scapy**.
 Built for quick testing, learning, or basic traffic monitoring.

------

## **Usage**

```
bash


Copy code
sudo python3 sniffer.py [options]
```

------

## **Arguments**

- `-c`, `--count`
   **Number of packets to capture**.
   Default is `0` (sniff indefinitely).
- `-f`, `--filter`
   **BPF (Berkeley Packet Filter) string** to filter packets.
   Default is `"ip"`. Example values: `"tcp"`, `"udp"`, `"icmp"`.

------

## **Examples**

```
bashCopy code# Capture 100 TCP packets
sudo python3 sniffer.py -c 100 -f tcp

# Sniff all IP traffic indefinitely
sudo python3 sniffer.py
```

------

## **Features**

- Real-time packet display
- Shows protocol, source IP, and destination IP
- Lightweight and easy to modify
- No external dependencies beyond Scapy

------

## **Note**

This script requires root privileges to capture packets.
 Use responsibly and only on networks you are authorized to monitor.