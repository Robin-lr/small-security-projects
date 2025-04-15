import argparse
from scapy.all import sniff, IP, TCP, UDP, ICMP
from datetime import datetime

# Function to process each packet
def process_packet(pkt):
    if IP in pkt:
        proto = "OTHER"
        if pkt.haslayer(TCP):
            proto = "TCP"
        elif pkt.haslayer(UDP):
            proto = "UDP"
        elif pkt.haslayer(ICMP):
            proto = "ICMP"
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        src_ip = pkt[IP].src
        dst_ip = pkt[IP].dst

        print(f"[{timestamp}] [{proto}] {src_ip} -> {dst_ip}")

# Main function
def main():
    parser = argparse.ArgumentParser(
        description="Basic Network Sniffer using Scapy",
        epilog="Example: sudo python3 sniffer.py -c 100 -f tcp"
    )

    parser.add_argument(
        "-c", "--count",
        type=int,
        default=0,
        help="Number of packets to capture (default: 0 for infinite)"
    )

    parser.add_argument(
        "-f", "--filter",
        type=str,
        default="ip",
        help="BPF filter to apply (e.g. ip, tcp, udp, icmp). Default: ip"
    )

    args = parser.parse_args()

    print(f"\nSniffing started... Filter: '{args.filter}', Count: {'∞' if args.count == 0 else args.count}")
    print("Press Ctrl+C to stop.\n")

    sniff(filter=args.filter, prn=process_packet, store=False, count=args.count if args.count > 0 else 0)

if __name__ == "__main__":
    main()
