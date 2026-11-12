import socket
import inspect
from datetime import datetime, timezone
from email.utils import format_datetime
import json


def parse_request(request):
    head, _, body = request.partition("\r\n\r\n")
    #print(parsed_req[0])
    head = head.split("\r\n")
    #print(head)
    head_json = {}
    for i in head:
        if i == head[0]:
            head_json["Header"]= i
            continue
        name,_,value = i.partition(":")
        head_json[name.strip()] = value.strip()
    return head_json, body

    


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 4221))
s.listen()

while True:
    conn, addr = s.accept()
    info = b""
    while b"\r\n\r\n" not in info:
        chunk = conn.recv(4096)
        if not chunk:
            break
        info += chunk

    req = info.decode()
    head_req, body_req = parse_request(req)
    print(head_req)
    length = 0
    for k,v in head_req.items():
        if k.lower() == "content-length":
            length = int(v)
    body_bytes = body_req.encode()
    while len(body_bytes) < length:
        chunk = conn.recv(min(4096,length-len(body_bytes)))
        if not chunk:
            break
        body_bytes += chunk
    body_req = body_bytes.decode()


    now = datetime.now(timezone.utc)
    http_date = format_datetime(now, usegmt=True)
    body = json.dumps({"message":f"You said {body_req}"})
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
    #print(encoded_resp)
    conn.sendall(encoded_resp)
    conn.close()



