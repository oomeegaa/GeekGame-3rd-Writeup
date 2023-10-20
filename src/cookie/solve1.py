from random import Random
from randcrack import RandCrack

rc = RandCrack()

with open("password1.txt", "r") as f:
    password = f.read()

for i in range(624):
    dword = password[i * 8: (i + 1) * 8]
    int32 = dword[6:8]+dword[4:6]+dword[2:4]+dword[0:2]
    int32 = int(int32, 16)
    rc.submit(int32)

stream = password[:624 * 8]
while (len(stream) < len(password)):
    int32 = rc.predict_getrandbits(32)
    int32 = '{:08x}'.format(int32)
    stream += int32[6:8]+int32[4:6]+int32[2:4]+int32[0:2]

print(len(password))

b = []
for i in range(5000, len(password), 2):
    byte = int(password[i:i+2],16) ^ int(stream[i:i+2],16)
    b += [byte]

print(bytes(b))
# print(password[:624 * 8] + rc.predict_getrandbits())