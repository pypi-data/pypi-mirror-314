import socket
import requests

def get_public_ip():
    """Get server's public IP address using external service"""
    try:
        response = requests.get('https://api.ipify.org')
        return response.text
    except:
        # Fallback method if the first service fails
        try:
            response = requests.get('https://api.ip.sb/ip')
            return response.text.strip()
        except:
            return None

# Existing code remains unchanged...
def get_ip_from_domain(domain:str):
    try:
        domain = domain.replace('*','asdfasf')
        return socket.gethostbyname(domain)
    except:pass
    
def test_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    result = sock.connect_ex((ip, port))
    res = False
    if result == 0:
        res = True
    sock.close()
    return res
