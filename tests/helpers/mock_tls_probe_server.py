#!/usr/bin/env python3
"""TCP server that records how each client opens a connection.

For every connection one line is appended to the log file:
  h2c        - HTTP/2 cleartext preface, the connection has no TLS
  tls-ok     - TLS handshake completed: the client accepted the self-signed certificate
  tls-failed - TLS handshake aborted: the client rejected the certificate
  other      - anything else
The self-signed certificate for localhost is generated with openssl at startup.
Used to test which connections the gRPC transport protects with TLS.
"""
import os
import socket
import ssl
import subprocess
import sys
import tempfile
import threading


def create_context():
    directory = tempfile.mkdtemp()
    cert = os.path.join(directory, 'cert.pem')
    key = os.path.join(directory, 'key.pem')
    subprocess.run(
        ['openssl', 'req', '-x509', '-newkey', 'ec', '-pkeyopt', 'ec_paramgen_curve:prime256v1',
         '-nodes', '-keyout', key, '-out', cert, '-days', '1', '-subj', '/CN=localhost',
         '-addext', 'subjectAltName=DNS:localhost'],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(cert, key)
    return context


def classify(conn, context):
    conn.settimeout(5)
    try:
        first = conn.recv(1, socket.MSG_PEEK)
    except OSError:
        return 'other'
    if first == b'P':
        return 'h2c'
    if first != b'\x16':
        return 'other'
    try:
        tls_conn = context.wrap_socket(conn, server_side=True)
    except (ssl.SSLError, OSError):
        return 'tls-failed'
    tls_conn.close()
    return 'tls-ok'


def handle_client(conn, context, log_path, lock):
    try:
        kind = classify(conn, context)
    finally:
        conn.close()
    with lock:
        with open(log_path, 'a', encoding='utf-8') as log:
            log.write(kind + '\n')


def main():
    port = int(sys.argv[1])
    log_path = sys.argv[2]
    context = create_context()
    lock = threading.Lock()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', port))
    server.listen(10)
    print(f'TLS probe server on port {port}', flush=True)
    while True:
        conn, _ = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, context, log_path, lock))
        thread.daemon = True
        thread.start()


if __name__ == '__main__':
    main()
