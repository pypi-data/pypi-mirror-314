import socket
import threading
import copy
from time import sleep, time

class AutoDiscovery(object):

    def __init__(self):
        self.peers = {}
        self.token = b"f9bf78b9a18ce6d46a0cd2b0b86df9da"
        self.port = 44444
        self.run = False

    def discovery(self, timeout=1):
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.settimeout(timeout)
        server.bind(("", self.port))

        self.run = True

        while self.run:
            try:
                data, addr = server.recvfrom(1024)
                if self.token in data:
                    # print(f"Got service announcement from {addr[0]}")
                    self.peers[addr[0]] = time()

            except TimeoutError as e:
                # print("Timeout...")
                pass

            except KeyboardInterrupt:
                self.run = False
            
            peers = copy.deepcopy(self.peers)
            for peer in self.peers:
                if time() - peers[peer] > 20:
                    del peers[peer]
                
            self.peers = peers

        server.close()

    def run_discovery(self, timeout=1):
        t = threading.Thread(target=self.discovery, args=(timeout,), daemon=True)
        t.start()

    def announcement(self, sleep_time=5):
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.run = True

        while self.run:
            server.sendto(self.token, ("<broadcast>", self.port))
            sleep(sleep_time)

        
    
    def run_announcement(self, timeout=1):
        t = threading.Thread(target=self.announcement, args=(timeout,), daemon=True)
        t.start()