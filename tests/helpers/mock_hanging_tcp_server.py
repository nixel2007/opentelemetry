#!/usr/bin/env python3
"""Hanging TCP server - accepts connections but never sends data.
Used to test gRPC transport timeout behavior.
"""
import socket
import sys
import threading
import time


def handle_client(conn):
    try:
        time.sleep(60)
    finally:
        conn.close()


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 14317
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', port))
    server.listen(10)
    print(f'Hanging TCP server on port {port}', flush=True)
    while True:
        conn, _ = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,))
        thread.daemon = True
        thread.start()


if __name__ == '__main__':
    main()
