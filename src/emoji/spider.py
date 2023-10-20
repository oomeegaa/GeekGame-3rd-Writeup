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