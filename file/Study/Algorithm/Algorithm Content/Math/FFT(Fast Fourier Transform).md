# Concept
- `Fourier Transform` : 시간에 대한 함수를 구성하고 있는 주파수 성분으로 분해하는 과정을 말한다.
- Fourier Transform 원리 (출처 : 공대생의 차고)
![[FT 원리.gif]] 
- `DFT(Discrete Fourier Transform)` : 연속이 아닌 **이산 시간**에 대한 함수를 **이산 주파수**로 변환하는 과정을 말한다. 컴퓨터 속 퓨리에 변환은 대부분 DFT를 의미한다.
- FFT는 이러한 퓨리에 변환을 빠르게 하는 방법을 말하며 주로 알고리즘에서의 FFT는 이산 합성곱(두 벡터의 합성곱)을 `O(nlogn)`의 시간복잡도로 계산하는 알고리즘을 말한다. ex) (x+2)(x+3) =  x<sup>2</sup>+5x+6 -> `v = [1,2]  u = [1,3] v * u = [1, 5, 6]`
# FFT 원리
- 2부터 차례대로 배수를 구하면서 N이하인 2의 배수들을 배열에서 제거해나가는 방식이다.
#### 🖼️그림으로 이해하기
![[]]
# FFT CODE
- 1~n까지의 숫자들 중 소수가 무엇인지를 찾는 것이기 때문에 n이 커지면 커질 수록 계산 시간이 오래 걸린다.

#### ⌨️ Code
```cpp

```
##### ❓ 예제 Input
	56

##### ⭐ 예제 Output
	2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 53
# FFT 응용문제
### 📑[17134 - 르모앙의 추측](https://www.acmicpc.net/problem/17134)
#### 🔓 KeyPoint
- 4자리 소수에서 한 자리씩 수를 바꾸어 최종 원하는 소수로 바꾸는 과정에서 존재하는 모든 수
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>
#define MAX 1000000

using namespace std;

typedef complex<double> cpx;
const double PI = acos(-1);

int t;
bool IsPrime[MAX] = {0, };

void FFT(vector<cpx> &v_cpx, bool IsIDFT) {
    int n = (int)v_cpx.size();
    
    for ( int i = 1, j = 0; i < n; i++ ) {
        int bit = n / 2;
        while ( j >= bit ) {
            j -= bit;
            bit /= 2;
        }
        j += bit;
        
        if ( i < j ) swap(v_cpx[i], v_cpx[j]);
    }

    for ( int i = 1; i < n; i *= 2 ) {
        cpx w;
        if ( IsIDFT ) w = cpx(cos(PI / i), sin(PI / i));
        else w = cpx(cos(-PI / i), sin(-PI / i));
        
        for ( int j = 0; j < n; j += i * 2 ) {
            cpx nw(1, 0);
            
            for ( int k = 0; k < i; k++ ) {
                cpx even = v_cpx[j+k];
                cpx odd = v_cpx[i+j+k];
                
                v_cpx[j+k] = even + nw * odd;
                v_cpx[i+j+k] = even - nw * odd;
                nw *= w;
            }
        }
    }
    
    if ( IsIDFT ) {
        for ( int i = 0; i < n; i++ ) v_cpx[i] /= n;
    }
}

vector<cpx> multiply(vector<cpx> &v_cpx, vector<cpx> &u_cpx) {
    int n = 2;
    while ( n < (int)v_cpx.size() + (int)u_cpx.size() ) n *= 2;
    v_cpx.resize(n);
    u_cpx.resize(n);
    FFT(v_cpx, false);
    FFT(u_cpx, false);
    
    vector<cpx> r_cpx(n);
    for ( int i = 0; i < n; i++ ) r_cpx[i] = v_cpx[i] * u_cpx[i];
    
    FFT(r_cpx, true);
    return r_cpx;
} 

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> t;
    
    memset(IsPrime, 1, sizeof(IsPrime));
    
    for ( int i = 2; i <= sqrt(MAX); i++ ) {
        if ( !IsPrime[i] ) continue;
        for ( int j = i * i; j < MAX; j += i ) IsPrime[j] = false;
    }
    
    vector<cpx> v_cpx(MAX), u_cpx(MAX);
    for ( int i = 2; i < MAX; i++ ) {
        if ( IsPrime[i] ) {
            v_cpx[i] = cpx(1, 0);
            if ( i * 2 < MAX ) u_cpx[i*2] = cpx(1, 0);
        }
    }
    
    vector<cpx> r_cpx = multiply(v_cpx, u_cpx);
    while ( t-- ) {
        int n;
        cin >> n;
        cout << round(r_cpx[n].real()) << '\n';
    }
    return 0;
}
```
### 📑[22289 - 큰 수 곱셈 (3)](https://www.acmicpc.net/problem/22289)
#### 🔓 KeyPoint
- 여러 수로 이루어진 배열을 두 개의 쌍(그룹)으로 나누어 짝지었을때, 짝지은 모든 수들의 합이 
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

typedef complex<double> cpx;

const double PI = acos(-1);

void FFT(vector<cpx> &v, bool IsIDFT) {
    int n = (int)v.size();
    
    for ( int i = 1, j = 0; i < n; i++ ) {
        int bit = n / 2;
        
        while ( j >= bit ) {
            j -= bit;
            bit /= 2;
        }
        j += bit;
        if ( i < j ) swap(v[i], v[j]);
    }
    
    for ( int i = 1; i < n; i *= 2 ) {
        cpx w;
        if ( IsIDFT ) w = cpx(cos(PI / i), sin(PI / i));
        else w = cpx(cos(-PI / i), sin(-PI / i));
        
        for ( int j = 0; j < n; j += i*2 ) {
            cpx nw(1, 0);
            
            for ( int k = 0; k < i; k++ ) {
                cpx even = v[j+k];
                cpx odd = v[i+j+k];
                
                v[j+k] = even + nw * odd;
                v[i+j+k] = even - nw * odd;
                nw *= w;
            }
        }
    }
    
    if ( IsIDFT ) {
        for ( int i = 0; i < n; i++ ) v[i] /= n;
    }
}

vector<int> multiply(vector<int> &v, vector<int> &u) {
    vector<cpx> v_cpx, u_cpx;
    
    for ( int i = 0; i < (int)v.size(); i++ ) v_cpx.push_back(cpx(v[i], 0));
    for ( int i = 0; i < (int)u.size(); i++ ) u_cpx.push_back(cpx(u[i], 0));
    
    int n = 2;
    while ( n < (int)v.size() + (int)u.size() ) n *= 2;
    
    v_cpx.resize(n);
    u_cpx.resize(n);
    FFT(v_cpx, false);
    FFT(u_cpx, false);
    
    vector<cpx> r_cpx(n);
    
    for( int i = 0; i < n; i++ ) r_cpx[i] = v_cpx[i] * u_cpx[i];
    
    FFT(r_cpx, true);
    
    vector<int> result(n);
    
    for( int i = 0; i < n; i++ ) result[i] = round(r_cpx[i].real());
    
    return result;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    string a, b;
    cin >> a >> b;
    
    vector<int> v, u;
    for ( int i = 0; i < (int)a.length(); i++ ) v.push_back(a[i] - '0');
    for ( int i = 0; i < (int)b.length(); i++ ) u.push_back(b[i] - '0');

    reverse(v.begin(), v.end());
    reverse(u.begin(), u.end());

    vector<int> result = multiply(v, u);

    for ( int i = 0; i < (int)result.size() - 1; i++ ) {
        if ( result[i] / 10 ) {
            result[i+1] += result[i] / 10;
            result[i] %= 10;
        }
    }
    
    reverse(result.begin(), result.end());
    
    int idx = 0; 
    while(result[idx] == 0) idx++;
    
    if(idx >= (int)result.size()) {
        cout << 0;
        return 0;
    }

    while(idx < (int)result.size()) {
        cout << result[idx];
        idx++;
    }
    
    return 0;
}
```
