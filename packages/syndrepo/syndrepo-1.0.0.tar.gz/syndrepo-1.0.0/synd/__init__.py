import socket
import time

def syndrepo(port, target):
    """
    Sends a SYN-like request to a given port and target.

    Args:
        port (int): The port to connect to (e.g., 80, 443).
        target (str): The target domain or IP address.

    Returns:
        dict: A dictionary containing the target, port, status, and response time.
    """
    try:
        # Attempt to resolve the hostname to an IP address
        resolved_ip = socket.gethostbyname(target)
        
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)  # Set a timeout for the connection
        
        # Record the start time
        start = time.time()
        
        # Connect to the target IP and port
        s.connect((resolved_ip, port))
        
        # Prepare the request based on the port
        if port == 80:
            s.send(b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")
        elif port == 443:
            s.send(b"POST / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")
        else:
            s.send(b"GET / HTTP/1.1\r\n\r\n")
        
        # Calculate response time
        response_time = time.time() - start
        
        # Close the socket
        s.close()
        
        # Return success
        return {
            "target": target,
            "resolved_ip": resolved_ip,
            "port": port,
            "status": "Success",
            "response_time": f"{response_time:.4f} seconds",
        }
    except socket.gaierror:
        # Handle DNS resolution errors
        return {
            "target": target,
            "resolved_ip": None,
            "port": port,
            "status": "Failed - Unable to resolve hostname (Invalid or Nonexistent)",
            "response_time": None,
        }
    except socket.timeout:
        # Handle connection timeout
        return {
            "target": target,
            "resolved_ip": resolved_ip if 'resolved_ip' in locals() else None,
            "port": port,
            "status": "Failed - Connection timed out",
            "response_time": None,
        }
    except Exception as e:
        # Handle other exceptions
        return {
            "target": target,
            "resolved_ip": resolved_ip if 'resolved_ip' in locals() else None,
            "port": port,
            "status": f"Failed - {e}",
            "response_time": None,
        }
    finally:
        if 's' in locals():
            s.close()
