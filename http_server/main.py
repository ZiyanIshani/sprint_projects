import socket
import inspect
from datetime import datetime, timezone
from email.utils import format_datetime
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 4221))
s.listen()

while True:
    conn, addr = s.accept()
    info = conn.recv(4096)
    resp = info.decode()
    now = datetime.now(timezone.utc)
    http_date = format_datetime(now, usegmt=True)
    body = json.dumps({"message":f"You said {resp}"})
    body_len = len(body.encode())
    http_resp = "\r\n".join([
        "HTTP/1.1 200 OK",
        "Server: localhost",
        f"Date: {http_date}",
        "Content-Type: application/json",
        f"Content-Length: {body_len}",
        "",
        body,
    ])
         
    encoded_resp = http_resp.encode()
    print(encoded_resp)
    conn.sendall(encoded_resp)
    conn.close()



