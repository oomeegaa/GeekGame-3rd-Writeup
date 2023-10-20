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