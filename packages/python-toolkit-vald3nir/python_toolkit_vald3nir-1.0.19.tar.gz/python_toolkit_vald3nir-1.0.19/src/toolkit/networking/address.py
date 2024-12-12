import socket


def get_local_ip() -> str:
    try:
        # Create a temporary socket to discover the local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Tries to connect to an external address
        s.connect(("8.8.8.8", 80))
        # Gets the local IP address used for the connection
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        return f"Error getting local IP: {e}"
