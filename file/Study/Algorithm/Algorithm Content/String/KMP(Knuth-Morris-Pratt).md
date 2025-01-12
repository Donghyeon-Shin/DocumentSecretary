# Concept
- 문자열에서 부분 문자열을 찾아내는 알고리즘이다.
- 실제 여러 프로그램에서 Ctrl + F의 찾기 기능은 이 알고리즘을 사용한 것이다.
- Knuth, Morris, Pratt가 만들어 만든 사람의 앞 글자를 따 KMP 알고리즘이라고 한다.
- 브루트포스 알고리즘으로 부분 문자열을 찾는다고 했을 때, 시간복잡도는 O(NM) / 문자열 길이 N, 부분 문자열 길이 M
- 접두사(prefix)와 접미사(suffix)을 이용해 중복 탐색을 최소화하여 문자열을 탐색한다.
- KMP의 시간복잡도는 O(N+M)이다. / 문자열 길이 N, 부분 문자열 길이 M
# KMP 원리📑[1786 - 찾기](https://www.acmicpc.net/problem/1786)
- `pi[i] = 문자열 s에서 0~i까지 부분 문자열 중(prefix == suffix)인 가장 긴 부분 문자열의 길이`로 놓는다.
- Target String에서 Key String을 찾는다고 했을 때 Key String에 Pi를 구한다.
- Pi를 바탕으로 Target에서 Key을 찾을 때 Key의 값과 Target의 값이 (Target Idx : i, Key Idx : j)에서 맞지 않는다면 `j = pi[j-1]`로 업데이트 시켜 이미 맞았던 부분은 건너뛰고 그 다음 값을 체크한다.
- j가 m-1이 됐다면 Target에서 Key의 모든 값을 찾았다는 것이므로 해당 i값을 결과 Array에 넣고 다음 Key를 찾기 위해 `j = pi[j]`로 업데이트 한다.
#### 🖼️그림으로 이해하기
![[KMP Graph.svg]]
# KMP CODE
- Pi 값을 구하는 것도 Key String에서 Key String을 찾는 과정과 유사하기 때문에 KMP 함수와 getPI함수가 크게 다르지 않다.
- `while ( j > 0 && s[i] != s[j] ) j = pi[j-1]`은 i와 j부분에서 Target과 Key가 맞지 않는다면 계속해서 pi를 업데이트 시켜 j = 0이 되거나 i와 j부분에서 값이 맞을 때까지 반복하는 계산을 수행한다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

string s1, s2;

vector<int> getPi(string s) {
    int m = (int)s.length(),j = 0;
    vector<int> pi(m);
    
    for ( int i = 1; i < m; i++ ) {
        while ( j > 0 && s[i] != s[j] ) j = pi[j-1];
        if ( s[i] == s[j] ) pi[i] = ++j;
    }
    
    return pi;
}

vector<int> KMP(string target, string key) {
    int n = (int)target.length(), m = (int)key.length(), j = 0;
    vector<int> pi = getPi(key);
    
    vector<int> result;
    
    for ( int i = 0; i < n; i++ ) {
        while ( j > 0 && target[i] != key[j] ) j = pi[j-1];
        if ( target[i] == key[j] ) {
            if ( j == m - 1 ) {
                result.push_back(i-m+1);
                j = pi[j];
            } else j++;
        }
    }
    
    return result;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    getline(cin, s1);
    getline(cin, s2);
    
    vector<int> ans = KMP(s1, s2);
    cout << (int)ans.size() << '\n';
    for ( auto i : ans ) cout << i+1 << ' ';
    return 0;
}
```
##### ❓ 예제 Input
	ABCABKABCAKABCABEA
	ABCABE
##### ⭐ 예제 Output
	1
	12
# KMP 응용문제
### 📑[1305 - 광고](https://www.acmicpc.net/problem/1305)
#### 🔓 KeyPoint
- 광고 전광판의 크기가 l일 때, 한 순간의 광고는 길이가 l인 문자열이다.
- 광고가 l보다 크다고 하더라도 잘리기 때문에 한순간의 광고판을 보고 유추할 수 있는 광고의 길이(x)는 1 <= x <= l이다.
- 광고에서 `pi[l-1](prefix == suffix)`인 부분은 처음 부분이 다시 등장한 것으로 볼 수 있다.
- 따라서 광고의 최소 길이는 `l - pi[l-1]`이다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int l;
string s;

vector<int> getPi(string str) {
    int m = (int)str.length(),j = 0;
    vector<int> pi(m);
    
    for ( int i = 1; i < m; i++ ) {
        while ( j > 0 && str[i] != str[j] ) j = pi[j-1];
        if ( str[i] == str[j] ) pi[i] = ++j;
    }
    
    return pi;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> l >> s;
    vector<int> pi = getPi(s);
    cout << l - pi[l-1];
    return 0;
}
```
### 📑[4354 - 문자열 제곱](https://www.acmicpc.net/problem/4354)
#### 🔓 KeyPoint
- 문자열의 부분 문자열이 반복되는지 안되는지 판단하고 반복된다면 몇 번 반복된 것인지를 계산하는 문제이다.
- 문자열의 길이를 m이라 할 때, `pi[m-1](prefix == suffix)`이 m으로 나누었을 때 나머지가 존재하지 않는다면 `m - pi[m-1]`이 반복한 문자열 길이이다.
- 반복 횟수는 전체 문자열 길이 `m`을 반복한 문자열 길이 `m - pi[m-1]`로 나눈 몫이다.
- 나머지가 존재한다면 문자열이 반복된 것이 아니기 때문에 1를 출력한다
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

string s;

vector<int> getPi(string str) {
    int m = (int)str.length(), j = 0;
    vector<int> pi(m);
    
    for ( int i = 1; i < m; i++ ) {
        while ( j > 0 && str[i] != str[j] ) j = pi[j-1];
        if ( str[i] == str[j] ) pi[i] = ++j;
    }
    
    return pi;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    while ( 1 ) {
        cin >> s;
        int m = (int)s.length();
        if ( m == 1 && s[0] == '.' ) break;
        vector<int> pi = getPi(s);
        if ( m % (m - pi[m-1]) != 0 ) cout << 1 << '\n';
        else cout << m / (m - pi[m-1]) << '\n';
    }
    return 0;
}
```
