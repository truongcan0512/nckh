import argparse
import logging
import random
import socket
import sys
import time
import ssl

parser = argparse.ArgumentParser(
    description="GET request traffic"
)
parser.add_argument("host", nargs="?", help="Host to perform stress test on")
parser.add_argument(
    "-p", "--port", default=80, help="Port of webserver, usually 80", type=int
)
parser.add_argument(
    "-s",
    "--sockets",
    default=100,
    help="Number of sockets to use in the test",
    type=int,
)

parser.add_argument(
    "--sleeptime",
    dest="sleeptime",
    default=1,
    type=int,
    help="Time to sleep between each header sent.",
)

args = parser.parse_args()

if len(sys.argv) <= 1:
    parser.print_help()
    sys.exit(1)

if not args.host:
    print("Host required!")
    parser.print_help()
    sys.exit(1)

def send_line(self, line):
    line = f"{line}\r\n"
    self.send(line.encode("utf-8"))


def send_header(self, name, value):
    self.send_line(f"{name}: {value}")

setattr(socket.socket, "send_line", send_line)
setattr(socket.socket, "send_header", send_header)

list_of_sockets =[]

def init_socket(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)

    s.connect((ip, args.port))

    return s


def main():
    ip = args.host
    socket_count = args.sockets
    # logging.info("Generating traffic %s with %s sockets.", ip, socket_count)
    print('[%s]' %(time.strftime("%H:%M:%S")),"Starting generating traffic %s with %s sockets." %(ip, socket_count))

    logging.info("Creating sockets...")
    for _ in range(socket_count):
        try:
            logging.debug("Creating socket nr %s", _)
            s = init_socket(ip)
        except socket.error as e:
            logging.debug(e)
            break
        list_of_sockets.append(s)

    while True:
        try:
            
            for s in list(list_of_sockets):
                try:
                    print('[%s]' %(time.strftime("%H:%M:%S")),
                        "Send GET request on port %s "  %s.getsockname()[1])

                    s.send('GET / HTTP/1.1\r\n'.encode())
                    s.send("Content-Type: text/html\r\n\r\n".encode())
                    # s.close()
                except socket.error:
                    list_of_sockets.remove(s)

            for _ in range(socket_count - len(list_of_sockets)):
                logging.debug("Recreating socket...")
                try:
                    s = init_socket(ip)
                    if s:
                        list_of_sockets.append(s)
                except socket.error as e:
                    logging.debug(e)
                    break
            logging.debug("Sleeping for %d seconds", args.sleeptime)
            time.sleep(args.sleeptime)

        except (KeyboardInterrupt, SystemExit):
            print('[%s]' %(time.strftime("%H:%M:%S")),
                        "Stopping generating traffic")
            break


if __name__ == "__main__":
    main()
