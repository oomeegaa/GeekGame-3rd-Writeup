from random import Random
from randcrack import RandCrack

with open("password2.txt", "r") as f:
    seed1, seed2, praw = f.read().split()

void1 = Random(int(seed1, 16))
void2 = Random(int(seed2, 16))

password = b''
for i in range(0, len(praw), 2):
    password += int(praw[i:i+2], 16).to_bytes(length=1,byteorder='little')

print(password)

gen = []
n = (1 << 22) + 6000

A = void1.randbytes(n)
B = void2.randbytes(n)

C = [x ^ y for x, y in zip(A, B)]

answer = b''

for start in range(0, (1 << 22) + 1, 1):
    if (start % 1000 == 0):
        print("now: ", start)
    rc = RandCrack()
    for p in range(0, 2496, 4):
        ab = int.from_bytes(C[p+start:p+start+4],byteorder='little')
        abc = int.from_bytes(password[p:p+4], byteorder='little')
        rc.submit(ab ^ abc)
    next_ab = int.from_bytes(C[start+2496:start+2500],byteorder='little')
    predict_c = rc.predict_getrandbits(32)
    next_abc = int.from_bytes(password[2496:2500], byteorder='little')
    if next_ab ^ predict_c == next_abc:
        print("found!", start, len(password))
        for i in range(2500, len(password), 4):
            next_ab = int.from_bytes(C[start+i:start+i+4],byteorder='little')
            next_c  = rc.predict_getrandbits(32)
            next_abc = int.from_bytes(password[i:i+4], byteorder='little')
            int32 = next_ab ^ next_c ^ next_abc
            answer += int32.to_bytes(length=4,byteorder='little')
        print(answer)
        exit(0)
