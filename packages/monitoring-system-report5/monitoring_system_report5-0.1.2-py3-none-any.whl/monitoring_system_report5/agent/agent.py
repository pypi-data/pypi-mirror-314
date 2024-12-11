# import socket
# import time
# import psutil
#
# def collect_metrics():
#     """Collect system metrics."""
#     cpu_usage = psutil.cpu_percent(interval=1)
#     memory = psutil.virtual_memory()
#     memory_usage = memory.percent
#     return {
#         "cpu": cpu_usage,
#         "memory": memory_usage
#     }
#
# def send_metrics(server_ip, server_port, hostname):
#     """Send metrics to the server."""
#     while True:
#         metrics = collect_metrics()
#         for metric, value in metrics.items():
#             message = f"{hostname}|{metric}|{value}"
#             try:
#                 client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#                 client.connect((server_ip, server_port))
#                 client.send(message.encode())
#                 response = client.recv(1024)
#                 print(f"Server response: {response.decode()}")
#                 client.close()
#             except Exception as e:
#                 print(f"Error: {e}")
#         time.sleep(5)
#
# if __name__ == "__main__":
#     SERVER_IP = "10.0.20.55"
#     SERVER_PORT = 10052
#     HOSTNAME = "test-host"
#     send_metrics(SERVER_IP, SERVER_PORT, HOSTNAME)

# //////////dynamic server ip//////////////////////

import socket
import time
import psutil


def get_local_ip():
    """Get the local IP address of the machine."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))  # Connect to a public IP to determine the local IP
            local_ip = s.getsockname()[0]
        return local_ip
    except Exception as e:
        print(f"Error retrieving local IP: {e}")
        return None


def collect_metrics():
    """Collect system metrics."""
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    return {
        "cpu": cpu_usage,
        "memory": memory_usage
    }


def send_metrics(server_ip, server_port, hostname):
    """Send metrics to the server."""
    while True:
        metrics = collect_metrics()
        for metric, value in metrics.items():
            message = f"{hostname}|{metric}|{value}"
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((server_ip, server_port))
                client.send(message.encode())
                response = client.recv(1024)
                print(f"Server response: {response.decode()}")
                client.close()
            except Exception as e:
                print(f"Error: {e}")
        time.sleep(5)


# if __name__ == "__main__":
#     SERVER_PORT = 10052
#     HOSTNAME = "test-host"
def main():
    SERVER_PORT = 10052
    HOSTNAME = "test-host"

    # Dynamically fetch the server's IP address
    SERVER_IP = get_local_ip()
    if SERVER_IP:
        print(f"Using dynamically determined IP: {SERVER_IP}")
        send_metrics(SERVER_IP, SERVER_PORT, HOSTNAME)
    else:
        print("Could not determine the local IP address.")
