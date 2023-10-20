data = [0x0F49, 0x121, 0x31C44DFF, 0x9BBB244, 0x9CD2637, 0x99E9344, 0x3A1174D9, 0x2982CE42, 0x202A3E59, 0x3AD2F444, 0x655DAC3, 0x181AE6C1, 0x2FFCF1EE, 0x0AAE9419, 0x2016E6F4, 0x19CF9F98, 0x2DEA04C3, 0x89262F4, 0x18327C16, 0x373BD1D9, 0x938E62A, 0x36B7868B, 0x3813BCFE, 0x0D213F8D, 0x7E67F22, 0x38FCD76, 0x32A17A7E, 0x2386EE67, 0x382D9FD7, 0x2FA45664, 0x4CFE37E, 0x2AF595C, 0x2103E392, 0x1536B2BA, 0x1C46D639, 0x0B170DEB, 0x2104AB3D, 0x334666E4, 0x0D52FFE1, 0x144A6446, 0x242BCC46, 0x37BF7317, 0x3A97D9A, 0x3B329D1A, 0x724F983, 0x1ED8A93E, 0x25E09BB8, 0x18121D9E, 0x2E301013, 0x105E3542, 0x375ADF03, 0x51674FE, 0x2AC2758E, 0x352291E2, 0x375D7604, 0x338E6B2A, 0x0C8EB7EB, 0x2F5350DC, 0x20E81988, 0x35F5C18E, 0x8753392, 0x0CD0ACE9, 0x17DF5455, 0x1B91C2B0]

n = 64
mod = 998244353

invn = pow(n, mod - 2, mod)
w = pow(3, (mod - 1) // n, mod)

wn = [0] * n
wn[n // 2] = 1
for i in range(n // 2 + 1, n):
    wn[i] = wn[i - 1] * w % mod
for i in range(n // 2 - 1, 0, -1):
    wn[i] = wn[i * 2]


mid = 1
while (mid < n):
    for i in range(0, n, mid * 2):
        for j in range(0, mid):
            x, y = data[i + j], data[i + j + mid] * wn[j + mid] % mod
            data[i + j], data[i + j + mid] = (x + y) % mod, (x - y) % mod
    mid <<= 1

if (idft := 1):
    for i in range(1, n // 2):
        data[i], data[n - i] = data[n - i], data[i]
    for i in range(0, n):
        data[i] = data[i] * invn % mod

print(bytes(data))