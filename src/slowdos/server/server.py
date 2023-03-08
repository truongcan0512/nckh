import argparse
import http
import time, threading, socket
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import parser
import sys

parser = argparse.ArgumentParser(description="HTTP server customize by Truong Can")
parser.add_argument(
    "host_name",
    default='127.0.0.1',
    nargs="?", 
    help="IP address of server")
parser.add_argument(
    "-p",
    "--port", 
    default=8000, 
    help="Port of webserver, usually 8000", 
    type=int
)
parser.add_argument(
    "-s",
    "--sockets",
    default=100,
    help="Number of sockets to use in the test",
    type=int
)

args = parser.parse_args()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        try:
            split_path = os.path.splitext(self.path)
            request_extension = split_path[1]
            if request_extension != ".py":
                f = open(self.path[1:]).read()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(bytes(f, 'utf-8'))
            else:
                f = "File not found"
                self.send_error(404,f)
        except:
            f = "File not found"
            self.send_error(404,f)

class _Threads(list):
    """
    Joinable list of all non-daemon threads.
    """
    def append(self, thread):
        self.reap()
        if thread.daemon:
            return
        super().append(thread)

    def pop_all(self):
        self[:], result = [], self[:]
        return result

    def join(self):
        for thread in self.pop_all():
            thread.join()

    def reap(self):
        self[:] = (thread for thread in self if thread.is_alive())

class _NoThreads:
    """
    Degenerate version of _Threads.
    """
    def append(self, thread):
        pass

    def join(self):
        pass

class ThreadingMixIn():
    """Mix-in class to handle each request in a new thread."""

    # Decides how threads will act upon termination of the
    # main process
    daemon_threads = False
    # If true, server_close() waits until all non-daemonic threads terminate.
    block_on_close = True
    # Threads object
    # used by server_close() to wait for all threads completion.
    _threads = _NoThreads()

    # Counting threads (Customizing)
    count = 0
    max_thread = 1

    def process_request_thread(self, request, client_address):
        """Same as in BaseServer but as a thread.
        In addition, exception handling is done here.
        """
        try:
            self.finish_request(request, client_address)
            self.count -= 1     # if finishing a thread --> decreasing count variable
        except Exception:
            self.handle_error(request, client_address)
        finally:
            self.shutdown_request(request)
            self.count -= 1     

    def process_request(self, request, client_address):
        """Start a new thread to process the request."""
        self.count += 1
        if self.block_on_close:
            vars(self).setdefault('_threads', _Threads())

        """Customizing is here"""
        if self.count < self.max_thread:
            # print('Threads: ', self.count)
            t = threading.Thread(target = self.process_request_thread,
                                args = (request, client_address))
            t.daemon = self.daemon_threads
            self._threads.append(t)
            t.start()
        if self.count < 0:
            self.count = 1

    def server_close(self):
        super().server_close()
        self._threads.join()

class httpServer(ThreadingMixIn,HTTPServer):
    pass

HOST_NAME = args.host_name
PORT = args.port

def main():
    try:

        webServer = httpServer((HOST_NAME,PORT),Handler)
        webServer.max_thread = args.sockets
        print(time.asctime(), "Start Server - %s:%s" %(HOST_NAME,PORT))
        
        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        webServer.server_close()
        print(time.asctime(),'Stop Server - %s:%s' %(HOST_NAME,PORT))
    except Exception:
        pass

if __name__ == "__main__":
    main()