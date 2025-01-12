# Concept
- Bruteforce 알고리즘에서 배열의 크기가 적당히 클 때 배열을 반으로 나누어 계산하는 알고리즘이다.
- 분할정복의 아이디어와 유사하지만, MITM의 경우 작은 부분으로 나누고 이를 다시 합치는 과정에서 추가 연산이 들어가게 된다.
- 단순 Bruteforce에서 시간 복잡도가 O(2^n)이라고 했을 때 MITM 알고리즘을 사용하면 O(2^(n/2) + 2^(n/2))로 계산할 수 있게 되는데, 이는 충분히 큰 배열에서 큰 차이를 보인다.
# Meet in the middle 원리 (📑[1208 - 부분수열의 합 2](https://www.acmicpc.net/problem/1208))
- MITM을 동작 과정을 살피기 위해 배열의 크기가 10인 수열을 준비하고 이에 모든 부분 집합에서 집합 원소의 합이 특정 값 K인 부분 집합의 개수를 찾는다고 해보자. 
- 단순 Bruteforce를 사용한다면 모든 부분 집합의 합을 구한 후 그 값이 K인지 탐색해야 하기 때문에 O(2^10)만큼의 시간이 걸릴 것이다. 하지만 MITM을 이용하면 O(2^5 + 2^5)이 걸리게 된다.
- 한 개의 배열을 절반씩 두 개의 배열로 나눈 뒤 나눈 배열들의 모든 부분집합의 합을 구한 뒤, 이 합들을 조합하여 K인지 아닌지를 판단한다.
#### 🖼️그림으로 이해하기
![[MITM Recursion.svg]]
# Meet in the middle CODE
- MITM은 보통 재귀를 통해 구현한다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, k, arr[100001], cnt = 0;
map<int,int> combin_left;

void combination(int start, int end, int sum) {
    if ( start == end ) {
        combin_left[sum]++;
        return;   
    }
    combination(start+1, end, sum);
    combination(start+1, end, sum + arr[start]);
}

void MITM(int start, int end, int sum) {
    if ( start == end ) {
        cnt += combin_left[k-sum];
        return;
    }
    
    MITM(start+1, end, sum);
    MITM(start+1, end, sum + arr[start]);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n;
    for ( int i = 0; i < n; i++ ) cin >> arr[i];
    cin >> k;
    
    combination(0, n/2, 0);
    MITM(n/2, n, 0);
    
    cout << cnt;
    return 0;
}
```
##### ❓ 예제 Input
	10
	1 3 6 11 17 5 22 8 9 13
	20
##### ⭐ 예제 Output
	9
# Meet in the middle 응용문제
### 📑[1450 - 냅색문제](https://www.acmicpc.net/problem/1450)
#### 🔓 KeyPoint
- '부분수열의 합 2' 문제랑 다른 점은 부분 수열에서 특정 값 K를 찾는게 아니라 K값 이하의 부분 수열의 개수를 찾는 문제라는 것이다.
- 조합을 Map으로 구현하는 것이 아니라 Vector로 구현해 이분 탐색을 통해 K값 이하의 부분 수열의 개수를 찾아야 한다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

long long n, c, obj[30], result = 0;
vector<long long> combin;

void combination(int start, int end, long long sum) {
    
    if ( start == end ) {
        combin.push_back(sum);
        return;
    }
    combination(start+1, end, sum);
    combination(start+1, end, sum+obj[start]);
}

void meetInTheMiddle(int start, int end, long long sum) {
    
    if ( start == end ) {
        if ( sum > c ) return;
        
        int index = (upper_bound(combin.begin(), combin.end(), c - sum ) - combin.begin());
        result += index;
        return;
    }
    
    meetInTheMiddle(start+1, end, sum);
    meetInTheMiddle(start+1, end, sum+obj[start]);
}


int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n >> c;
    for ( int i = 0; i < n; i++ ) cin >> obj[i];
    combination(0, n/2, 0);
    sort(combin.begin(), combin.end());
    meetInTheMiddle(n/2, n, 0);
    cout << result;
    return 0;
}
```
### 📑[2087 - 암호문](https://www.acmicpc.net/problem/2087)
#### 🔓 KeyPoint
- 부분 수열을 구성할 때 Parameter에 sum뿐만 아니라 bits식도 추가로 넘겨준다.
- 조합을 찾았으면 해당 조합의 Bits 값들을 String으로 변환하여 출력한다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

long long n, k, arr[40];
bool done = false;
map<long long, long long> combin;

string to_binary(long long num) {
    string s = "";
    while ( num >= 2 ) {
        if ( num % 2 == 1 ) s = "1"+ s;
        else s = "0" + s;
        num >>= 1;
    }
    return s;
}

void combination(int start, int end, long long sum, long long bits) {
    
    if ( start == end ) {
        combin[sum] = bits;
        return;
    }
    combination(start+1, end, sum, bits << 1 );
    combination(start+1, end, sum + arr[start], (bits << 1) + 1);
}

void meetInTheMiddle(int start, int end, long long sum, long long bits) {
    
    if ( done || start > end ) return;
    if ( start == end ) {
        if ( (combin[k-sum] != 0 || sum == k ) && !done ) {
            done = true;
            cout << to_binary(combin[k-sum]) << to_binary(bits);
            return;
        }
    }
    meetInTheMiddle(start+1, end, sum, bits << 1 );
    meetInTheMiddle(start+1, end, sum + arr[start], (bits << 1) + 1);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n;
    for ( int i = 0; i < n; i++ ) cin >> arr[i];
    cin >> k;
    combination(0, n/2, 0, 1);
    meetInTheMiddle(n/2, n, 0, 1);
    return 0;
}
```
