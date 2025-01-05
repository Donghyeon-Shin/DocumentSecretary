
## 📑[31027 - 물고기 게임](https://www.acmicpc.net/problem/31027)
#### 🔓 KeyPoint
-  이 문제는 '게임 이론'을 적용하는 문제이다.
-  2 x n 크기의 격자판에서 오토가 (1,1) 데이브가 (2, n)에서 서있을 때 둘 다 최대한 많은 물고기를 얻을려고 할 때 각자 몇 마리를 얻을 수 있는가를 구해야 한다.
-  격자 크기, 물고기에 양에 따라서 각자 얻고자 하는 격자판이 달라지기 때문에 이를 고려하는게 이 문제의 핵심이다.
- 오토가 먼저 움직이기 때문에 이 또한 고려하여야 한다.
#### 🖼️그림으로 이해하기
![[Fish Game.svg]]
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, farm[3][500001];
long long total = 0, otto_CaseA = 0, otto_CaseB = 0, david_CaseA = 0, david_CaseB = 0;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n;
    for ( int i = 1; i <= 2; i++ ) {
        for ( int j = 1; j <= n; j++ ) {
            cin >> farm[i][j];
            total += farm[i][j];
        }
    }
    
    if ( n == 2 ) {
        cout << max(farm[1][2],farm[2][1]) << ' ' << total - max(farm[1][2],farm[2][1]);
    } else {
        if ( n % 2 == 0 ) {
            for ( int i = 1; i <= n; i++ ) david_CaseA += farm[2][i];
            for ( int i = 1; i <= 2; i++ ) {
                for ( int j = (n/2) + 2; j <= n; j++ ) david_CaseB += farm[i][j];
            }
            
            if ( david_CaseA >= david_CaseB ) {
                for ( int i = 1; i <= n; i++ ) otto_CaseA += farm[1][i];
                for ( int i = 1; i <= 2; i++ ) {
                    for ( int j = 1; j <= (n/2); j++ ) otto_CaseB += farm[i][j];
                }
                
                if ( otto_CaseA > otto_CaseB ) cout << otto_CaseA << ' ' << total - otto_CaseA;
                else cout << otto_CaseB << ' ' << total - otto_CaseB;
            } else cout << total - david_CaseB << ' ' << david_CaseB;
        } else {
            for ( int i = 1; i <= n; i++ ) otto_CaseA += farm[1][i];
            for ( int i = 1; i <= 2; i++ ) {
                    for ( int j = 1; j <= (n/2); j++ ) otto_CaseB += farm[i][j];
            }
            
            if ( otto_CaseA >= otto_CaseB ) {
                for ( int i = 1; i <= n; i++ ) david_CaseA += farm[2][i];
                for ( int i = 1; i <= 2; i++ ) {
                    for ( int j = (n/2) + 2; j <= n; j++ ) david_CaseB += farm[i][j];
                }
                
                if ( david_CaseA > david_CaseB ) cout << total - david_CaseA << ' ' << david_CaseA;
                else cout << total - david_CaseB << ' ' << david_CaseB;
            } else cout << otto_CaseB << ' ' << total - otto_CaseB;
        }
    }
    return 0;
}
```

## 📑[20529 - 가장 가까운 세 사람의 심리적 거리](https://www.acmicpc.net/problem/20529)