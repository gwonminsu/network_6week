import os
import socket
import threading
import socketserver

SERVER_HOST = 'localhost'
SERVER_PORT = 0
BUF_SIZE = 1024
ECHO_MSG = 'Hello echo server!'

class ForkingServer(socketserver.ForkingMixIn, socketserver.TCPServer,):
    """Nothing to add here, inherited everthing necessary from parents"""
    pass

class ForkingServerRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = str(self.request.recv(BUF_SIZE), 'utf-8')

        current_process_id = os.getpid()
        response = f'{current_process_id}: [{data}]'
        print (f"Server sending response [current_process_id: data] = [{response}]")
        self.request.send(bytes(response, 'utf-8'))
        return
    
class ForkedClient():
    """ A client to test forking server"""
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))

    def run(self):
        """Client playing with the server"""
        current_process_id = os.getpid()
        print(f'PID {current_process_id} Sending echo message to the server : [{ECHO_MSG}]')
        sent_data_length = self.sock.send(bytes(ECHO_MSG, 'utf-8'))
        print(f"Sent: {sent_data_length} characters, so far...")

        response = self.sock.recv(BUF_SIZE)
        print(f"PID {current_process_id} received: {response[5:]}")

    def shutdown(self):
        """Cleanup the client socket"""
        self.sock.close()
    
def main():
    server = ForkingServer((SERVER_HOST, SERVER_PORT), ForkingServerRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.setDaemon(True)
    server_thread.start()
    print (f"Server loop running PID: {os.getpid()}")

    client1 = ForkedClient(ip, port)
    client1.run()
    print("First client running")

    client2 = ForkedClient(ip, port)
    client2.run()
    print("Second client running")

    server.shutdown()
    client1.shutdown()
    client2.shutdown()
    server.socket.close()

if __name__ == '__main__':
    main()