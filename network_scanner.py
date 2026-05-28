import subprocess
import socket
import ipaddress
import platform
import os
import re
from datetime import datetime

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def get_network_range(local_ip):
    parts = local_ip.split(".")
    return f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"

def ping_host(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    timeout = "-w" if platform.system().lower() == "windows" else "-W"
    command = ["ping", param, "1", timeout, "1", str(ip)]
    try:
        result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0
    except Exception:
        return False

def get_hostname(ip):
    try:
        return socket.gethostbyaddr(str(ip))[0]
    except Exception:
        return "Unknown"

def scan_port(ip, port, timeout=0.5):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((str(ip), port))
        sock.close()
        return result == 0
    except Exception:
        return False

COMMON_PORTS = {
    21:   "FTP",
    22:   "SSH",
    23:   "Telnet",
    25:   "SMTP",
    53:   "DNS",
    80:   "HTTP",
    110:  "POP3",
    135:  "MS-RPC",
    139:  "NetBIOS",
    143:  "IMAP",
    443:  "HTTPS",
    445:  "SMB",
    3306: "MySQL",
    3389: "RDP",
    5900: "VNC",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
}

RISKY_PORTS = [21, 23, 135, 139, 445, 3389, 5900]

def scan_ports(ip):
    open_ports = []
    for port, service in COMMON_PORTS.items():
        if scan_port(ip, port):
            risk = "⚠ RISKY" if port in RISKY_PORTS else "  OK   "
            open_ports.append((port, service, risk))
    return open_ports

def discover_hosts(network_range, max_hosts=20):
    print(f"\n  Scanning network: {network_range}")
    print("  Please wait...\n")
    live_hosts = []
    network = ipaddress.IPv4Network(network_range, strict=False)

    hosts = list(network.hosts())[:max_hosts]
    total = len(hosts)

    for i, ip in enumerate(hosts):
        print(f"  Scanning {i+1}/{total}: {ip}    ", end="\r")
        if ping_host(ip):
            hostname = get_hostname(ip)
            live_hosts.append((str(ip), hostname))

    print(" " * 50, end="\r")
    return live_hosts

def print_banner():
    print("\n  ╔══════════════════════════════════════════════╗")
    print("  ║         HOME NETWORK SCANNER                 ║")
    print("  ║         by Kartik | Cybersecurity Tool       ║")
    print("  ╚══════════════════════════════════════════════╝")

def save_report(results, local_ip):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"scan_report_{timestamp}.txt"
    with open(filename, "w") as f:
        f.write("=" * 60 + "\n")
        f.write("       HOME NETWORK SCAN REPORT\n")
        f.write(f"       Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"       Your IP: {local_ip}\n")
        f.write("=" * 60 + "\n\n")

        for ip, hostname, ports in results:
            f.write(f"HOST: {ip} ({hostname})\n")
            if ports:
                for port, service, risk in ports:
                    f.write(f"   Port {port:5d}  {service:<12} {risk}\n")
            else:
                f.write("   No common open ports found.\n")
            f.write("\n")

    print(f"\n  ✔  Report saved: {filename}")
    return filename

def main():
    print_banner()

    local_ip = get_local_ip()
    network_range = get_network_range(local_ip)

    print(f"\n  Your IP Address : {local_ip}")
    print(f"  Network Range   : {network_range}")
    print(f"  Scan Time       : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    print("\n  ─── MENU ───────────────────────────────────────")
    print("   1. Quick Scan   (ping sweep — find live hosts)")
    print("   2. Full Scan    (ping sweep + port scan)")
    print("   3. Scan single IP (port scan only)")
    print("   4. Exit")
    print("  ─────────────────────────────────────────────────")

    choice = input("\n  Enter choice (1/2/3/4): ").strip()

    # ── QUICK SCAN
    if choice == "1":
        hosts = discover_hosts(network_range)
        print(f"\n  Found {len(hosts)} live host(s):\n")
        print(f"  {'IP Address':<18} {'Hostname'}")
        print("  " + "-"*45)
        for ip, hostname in hosts:
            marker = " ◄ YOU" if ip == local_ip else ""
            print(f"  {ip:<18} {hostname}{marker}")

    # ── FULL SCAN
    elif choice == "2":
        hosts = discover_hosts(network_range)
        if not hosts:
            print("\n  No live hosts found.")
            return

        print(f"\n  Found {len(hosts)} live host(s). Starting port scan...\n")
        results = []
        for ip, hostname in hosts:
            print(f"\n  ┌─ HOST: {ip} ({hostname})")
            marker = " ◄ YOUR DEVICE" if ip == local_ip else ""
            print(f"  │  {marker}")
            open_ports = scan_ports(ip)
            if open_ports:
                print(f"  │  {'PORT':<8} {'SERVICE':<14} {'STATUS'}")
                print("  │  " + "-"*35)
                for port, service, risk in open_ports:
                    print(f"  │  {port:<8} {service:<14} {risk}")
            else:
                print("  │  No common open ports found.")
            print("  └" + "─"*40)
            results.append((ip, hostname, open_ports))

        save = input("\n  Save report to file? (y/n): ").strip().lower()
        if save == "y":
            save_report(results, local_ip)

    # ── SINGLE IP SCAN
    elif choice == "3":
        target = input("\n  Enter IP address to scan: ").strip()
        try:
            ipaddress.IPv4Address(target)
        except ValueError:
            print("  ✘  Invalid IP address.")
            return

        hostname = get_hostname(target)
        print(f"\n  Scanning {target} ({hostname})...")
        open_ports = scan_ports(target)

        print(f"\n  ┌─ HOST: {target} ({hostname})")
        if open_ports:
            print(f"  │  {'PORT':<8} {'SERVICE':<14} {'STATUS'}")
            print("  │  " + "-"*35)
            for port, service, risk in open_ports:
                print(f"  │  {port:<8} {service:<14} {risk}")
        else:
            print("  │  No common open ports found.")
        print("  └" + "─"*40)

        risky = [p for p, s, r in open_ports if "RISKY" in r]
        if risky:
            print(f"\n  ⚠  WARNING: Risky ports open: {risky}")
            print("     Consider closing or securing these services.")

    elif choice == "4":
        print("\n  Goodbye! Stay secure. 🔐\n")
    else:
        print("\n  Invalid choice.")

if __name__ == "__main__":
    main()
