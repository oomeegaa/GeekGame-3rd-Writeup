from pwn import *

ip = "prob08.geekgame.pku.edu.cn"
port = 10008
token = b"9:MEQCIAtVYew8qAhgBismBROItbCOeG1QCsei8lHhPwxiRWX5AiAGrTGtAJjhLuU3nD8plEYou0a7j8cnQ2OVt3Ryr2Zodg=="

r = remote(ip, port)
r.sendline(token)

print(r.recv())
r.sendline(b'3')
s = r.recvuntil('>')
s = s[s.find(b'<')+1:s.find(b'>')]
s = s.replace(b"0x",b'')

r.sendline(s)
r.interactive()




