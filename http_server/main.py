import socket
import inspect
from datetime import datetime, timezone
from email.utils import format_datetime
import json
import psycopg
from user import User


def parse_request(request):
    head, _, body = request.partition("\r\n\r\n")
    #print(parsed_req[0])
    head = head.split("\r\n")
    #print(head)
    head_json = {}
    for i in head:
        if i == head[0]:
            header = i.split(" ")
            assert len(header) == 3
            head_json["Method"] = header[0]
            head_json["Route"] = header[1]
            head_json["Version"] = header[2]
            continue
        name,_,value = i.partition(":")
        head_json[name.strip()] = value.strip()
    
    return head_json, body

def get_user(name, email)->bool:
    conn_string = "postgresql://user:password@localhost:5432/http_db"
    with psycopg.connect(conn_string) as db_conn:
        with db_conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE username = %s AND email = %s", (name, email))
            rows = cur.fetchone()
            print(rows)
            
            if rows:
                return True
            return False
        
def add_user(name, email) -> bool: 
    conn_string = "postgresql://user:password@localhost:5432/http_db"
    with psycopg.connect(conn_string) as db_conn:
        with db_conn.cursor() as cur:
            try:
                cur.execute("INSERT INTO users (username, email) VALUES (%s, %s)", (name, email))
                return True
            except:
                return False


    


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

    now = datetime.now(timezone.utc)
    http_date = format_datetime(now, usegmt=True)
    try:
        req = info.decode()
        head_req, body_req = parse_request(req)
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
        body_json = json.loads(body_req)

        assert len(body_json) == 2 and "Name" in body_json.keys() and "Email" in body_json.keys()
        print('didnt break assert')
        requested_user = User(body_json["Name"], body_json["Email"])
        if head_req["Method"] == "GET":
            body = get_user(requested_user.name, requested_user.email)
            body = str(body)
        elif head_req["Method"] == "POST":
            body = add_user(requested_user.name, requested_user.email)
            body = str(body)
        else:
            body = ""

        
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
            

    except Exception as e:
        print("error",type(e).__name__, e)
        http_resp = "\r\n".join([
                    "HTTP/1.1 400 Bad Request",
                    "Server: localhost",
                    f"Date: {http_date}",
                    "Content-Type: application/json",
                    f"Content-Length: 0",
                    "",
                    "",
                ])

    finally: 
        encoded_resp = http_resp.encode()
        conn.sendall(encoded_resp)
        conn.close()



