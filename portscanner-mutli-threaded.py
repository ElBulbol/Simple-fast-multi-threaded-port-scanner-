import socket
import time
from concurrent.futures import ThreadPoolExecutor
ip = input("What is the IP you want to scan [Default: 127.0.0.1]: ") or "127.0.0.1"
port_rang = int(input("What is the range of port you want to scan (0 - default 65536): ") or 65536)
print("note: Start with: 1000 , Aggressive: 2000–3000 , Extreme: 5000+")
threads =int(input("How many threads you want it to preform this scan "))
port_rang = port_rang +1 
open_ports = []

def scan_port(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))
            if result == 0:
                return port
    except:
        pass
    return None

start = time.perf_counter()

with ThreadPoolExecutor(max_workers=int(threads)) as executor:
    results = executor.map(scan_port, range(0, int(port_rang)))
    print(results)
    for port in results:
        if port:
            open_ports.append(port)

end = time.perf_counter()
print(f"Open ports: {open_ports}")
print(f"Execution time: {end - start:.2f} seconds")
