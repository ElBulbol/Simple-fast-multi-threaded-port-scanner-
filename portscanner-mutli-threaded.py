import socket
import time
import argparse
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

DEFAULT_IP = '127.0.0.1'
DEFAULT_PORT_RANGE = 65535
DEFAULT_THREADS = 1000
open_ports = []

# Argument parser
arg = argparse.ArgumentParser(description='Multithreaded Port Scanner')
arg.add_argument("-ip", dest="ip", help="IP address to scan", default=DEFAULT_IP)
arg.add_argument("-p", dest="port", help=f"Port range (default: {DEFAULT_PORT_RANGE})", type=int, default=DEFAULT_PORT_RANGE)
arg.add_argument("-th", dest="threads_num", help=f"Number of threads (default: {DEFAULT_THREADS}) \n <1-500 (normal)> <500-1000(high)> <1000-5000(intense)> ", type=int, default=DEFAULT_THREADS)
arg.add_argument("-o", dest="output", help="Output file to save results", default=None)

params = arg.parse_args()

ip = params.ip
port_range = params.port + 1  
threads = params.threads_num
output_file = params.output

try:
    socket.inet_aton(ip)
except socket.error:
    print(f"* Invalid IP address: {ip}")
    exit(1)

if port_range < 1 or port_range > 65536:
    print("* Port range must be between 1 and 65535")
    exit(1)

def scan_port(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.3)
            result = sock.connect_ex((ip, port))
            if result == 0:
                try:
                    service = socket.getservbyport(port, 'tcp')
                except OSError:
                    service = "unknown"
                return (port, service)
    except Exception:
        return None
    return None

print(f" Scanning {ip} on ports 0-{port_range - 1} using {threads} threads...")
start = time.perf_counter()

with ThreadPoolExecutor(max_workers=threads) as executor:
    results = list(tqdm(executor.map(scan_port, range(0, port_range)), total=port_range, desc="Scanning"))

for res in results:
    if res:
        open_ports.append(res)

open_ports.sort()

end = time.perf_counter()

print("\n Scan complete!")
print(f"Execution time: {end - start:.2f} seconds")
if open_ports:
    print(f"Open ports on {ip}:")
    for port, service in open_ports:
        print(f"{port}/tcp ({service})")
else:
    print("No open ports found ")

if output_file:
    try:
        with open(output_file, 'w') as f:
            for port, service in open_ports:
                f.write(f"{port}/tcp ({service})\n")
        print(f"Results saved to {output_file}")
    except Exception as e:
        print(f"Failed to save output: {e}")
