from pwn import *
import re

ip = "prob16.geekgame.pku.edu.cn"
port = 10016
token = b"9:How do you know my uid is 9"

instructions = [
    "newgame",
    "wwj",
    "y",
    "n","n","e","pickup key",
    "w","s","s","e","e","e","pickup trinket",
    "w","s","usewith key door",
    "s","s","n","w","w","w","n","pickup key",
    "s","e","e","e","n","n","w","w","n","n","w","w","usewith key door","use trinket"
]

while True:

    sleep(2.5)

    r = remote(ip, port)

    r.sendline(token)
    r.recv()

    for ins in instructions:
        r.sendline(ins.encode())
        r.recvuntil(b"]:")

    san = 0
    while san < 117:
        r.sendline(b"h")
        s = r.recvuntil(b"]:").decode()
        san = re.match("[\s\S]*\((-?\d+)%\)[\s\S]*",s)
        san = int(san.group(1))
        if san < 0:
            break
        print(san)
    
    if san > 0:
        break

r.interactive()