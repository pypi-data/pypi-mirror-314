"""
python socket to a docker container, inputting json & requesting json output
"""
import requests
import docker
import time
import socket

def is_port_available(port):
    """
    check whether the port is available
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex(('localhost', port))
        return result != 0

def get_available_port(start_port, end_port):
    """
    get an available port in a range
    """
    for port in range(start_port, end_port):
        if is_port_available(port):
            return port
    raise Exception("No available port found in the range")

class DockerSocket:
    """
    a python socket to a new container from the image {image_name}
    """
    def __init__(self, image_name, start_port=5000, end_port=6000, timeout = 300):
        """
        Args:
        image_name (str): image name
        start_port, end_port (int): range of the port of the host to bind with the container
        timeout (int): maximum waiting time for container setting
        """
        self.pt = get_available_port(start_port, end_port)
        client = docker.from_env()
        self.container = client.containers.run(
            image_name,
            detach=True,
            ports={'5000/tcp': self.pt}
        )
        timeout = timeout
        start_time = time.time()
        print(f'{image_name} container initializing...')
        while True:
            # 获取容器日志
            logs = self.container.logs()
            if b"Running on" in logs:
                print("Flask service is ready.")
                break
            if time.time() - start_time > timeout:
                print("Timeout waiting for Flask app to start.")
                break
            time.sleep(2)
    def request(self, dinput):
        url = f"http://localhost:{self.pt}/predict"
        try:
            response = requests.post(url, json = dinput)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
    def close(self):
        self.container.stop()
        self.container.remove()
