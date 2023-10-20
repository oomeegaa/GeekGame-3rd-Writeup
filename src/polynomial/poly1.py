data = [0x0CF6, 0x16C80709, 0x86B7BDA, 0x5FBEE9E, 0x24D1FFC1, 0x16F76AE2, 0x15F03305, 0x218C23F9, 0x33163AC1, 0x332C16E, 0x27E7B4A7, 0x241D8073, 0x1C6F122, 0x2D73DE13, 0x7FC0A09, 0x0D50F7B7, 0x261B1DD, 0x37E5BB8E, 0x0DA71DC5, 0x2DC3F20C, 0x0CCB13A, 0x2F6341E4, 0x0B0611DB, 0x0A382A1A, 0x103C09B2, 0x1CE2BE88, 0x19A9FD15, 0x2621CFC1, 0x2970DEAC, 0x8A463AA, 0x116C6D31, 0x222E9178, 0x33B9C9DD, 0x2F98D035, 0x0B8177A, 0x342611E8]

mod = 998244353
n = 36

matrix = [[0] * (n + 1) for i in range(n)]

def swap(i, j):
    for k in range(n + 1):
        matrix[i][k], matrix[j][k] = matrix[j][k], matrix[i][k]
def add(i, k, j):
    for p in range(n + 1):
        matrix[i][p] = (matrix[i][p] + k * matrix[j][p]) % mod

for i in range(n):
    matrix[i][n] = data[i]
    for j in range(n):
        matrix[i][j] = (i + 1) ** j % mod

for i in range(n):
    for j in range(n + 1):
        print(matrix[i][j], end=' ')
    print()

for i in range(n):
    for j in range(i + 1, n):
        if (matrix[j][i]):
            swap(i, j)
            while (matrix[j][i]):
                add(i, -(matrix[i][i] // matrix[j][i]), j)
                swap(i, j)

for i in range(n):
    for j in range(n + 1):
        print(matrix[i][j], end=' ')
    print()

s = ""
for i in range(n - 1, -1, -1):
    for c in range(32, 127):
        if (matrix[i][i] * c % mod == matrix[i][n]):
            ans = c
            s += chr(c)
            break
    else:
        print("boom!")
        break
    
    for j in range(i):
        matrix[j][n] = (matrix[j][n] - ans * matrix[j][i]) % mod

print(s[::-1])