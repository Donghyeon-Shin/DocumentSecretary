
# Concept
- 2진수 비트를 활용하여 특정 값의 상태를 표하는 자료구조이다.
- 0은 'Off/데이터 없음'을 나타내고 1은 'On/데이터 있음'을 나타낸다.
- 비트 연산을 통해 값을 찾거나 계산할 수 있어 시간복잡도는 O(1)이다.
- `데이터의 수 = 비트의 수`이기 때문에 데이터가 많으면 `Bitmask`을 사용하기 어렵다. (Ex : 10개의 데이터를 Bitmask하기 위해선 2<sup>10</sup>의 Bit가 필요하다.)
# Bitmask 원리
- 대부분 Array를 통해 Bitmask를 표현한다.
- Bitmask는 비트 연산을 통해 특정 값을 추가하거나 제거할 수 있고 해당 값이 있는지 없는지를 판단 할 수 있다.
- n개의 Bitmask를 표현할 수 있는 Array 만들기 : `array[1 << n]`
- n번 위치의 값 추가 ex ) 0000 | 0100 = 0100  : `val |= ( 1 << n )`
- n번 위치의 값 제거 ex ) 0100 & (~0100) = 0000 : `val &= ~( 1 << n )`
- n번 위치의 값이 있는지 확인 ex ) 0110 & 0100 =  : `(val & ( 1 << n )) != 0`
#### 🖼️그림으로 이해하기
![[Bitmask Graph.svg]]
# Bitmask CODE
- 비트 연산만 알고 있으면 쉽게 구현 할 수 있다.
- 데이터 개수와 연산 방식 및 시간복잡도와 공간복잡도를 고려하여 Bitmask를 사용할지 말지를 고려하는 것이 중요하다. 
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int addCnt, delCnt, CheckCnt, num, key = 0;
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> addCnt >> delCnt >> CheckCnt;
    while ( addCnt-- ) {
        cin >> num;
        if ( num < 0 || num > 10 ) continue;
        key |= ( 1 << num );
    }
    
    while ( delCnt-- ) {
        cin >> num;
        if ( num < 0 || num > 10 ) continue;
        key &= ~( 1 << num );
    }
    
    while ( CheckCnt-- ) {
        cin >> num;
        if ( num < 0 || num > 10 ) continue;
        if ( (key & ( 1 << num )) != 0 ) cout << "It exists.\n";
        else cout << "It not exists.\n";
    }
    
    return 0;
}
```
##### ❓ 예제 Input
	2 1 1
	2
	4
	4
##### ⭐ 예제 Output
	It exists.
# Bitmask 응용문제
### 📑[2098 - 외판원 순회](https://www.acmicpc.net/problem/2098)
#### 🔓 KeyPoint
- [[DP(Dynamic Programming)]]에 `Bitmask` 자료구조를 이용하여 문제를 해결할 수 있다.
- `dp[현재도시][도시 비트마스킹] = dp[city][bit]`로 놓고 모든 도시를 방문하면서 최소 비용을 구하면 된다.
- `bits == ( 1 << n ) - 1`일 경우 모든 도시를 돌았다는 뜻이다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>
#define INF 1e9

using namespace std;

int n, dp[16][1 << 16] = {0, }, w[16][16] = {0, };

int circuit(int city, int bits) {
    
    
    if ( dp[city][bits] != -1 ) return dp[city][bits];
    if ( bits == ( 1 << n ) - 1 ) {
        if ( w[city][0] == 0 ) return INF;
        else return w[city][0];
    }
    
    int minimum = INF;
    
    for ( int i = 0; i < n; i++ ) {
        if ( w[city][i] == 0 || (bits & ( 1 << i ) ) ) continue;
        minimum = min(minimum, circuit(i, bits | ( 1 << i )) + w[city][i]);
    }
    
    return dp[city][bits] = minimum;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n;
    for ( int i = 0; i < n; i++ ) {
        for ( int j = 0; j < n; j++ ) cin >> w[i][j];
    }
    
    memset(dp, -1, sizeof(dp));
    cout << circuit(0, 1);
    return 0;
}
```
### 📑[1194 - 달이 차오른다, 가자.](https://www.acmicpc.net/problem/1194)
#### 🔓 KeyPoint
- [[BFS(Breadth-First Search)]]에 `Bitmask` 자료구조를 이용하여 문제를 해결할 수 있다.
- 현재 a~f의 열쇠들을 가지고 있는지 아닌지의 상태를 `Bitmask`로 표현하고 해당 열쇠를 가고 있으면 문을 열고 갈 수 있도록 구현하면 된다.
- `cnt[현재 x위치][현재 y위치][열쇠 비트마스킹] = cnt[x][y][bit]`로 놓아서 중복 탐색을 방지해야 한다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, m, start_x, start_y, cnt[50][50][64] = {0, };
int dx[4] = {0, 0, 1, -1}, dy[4] = {1, -1, 0, 0};
char graph[50][50];

int bfs() {
    cnt[start_x][start_y][0] = 1;
    queue<tuple<int,int,int>> q;
    q.push({start_x,start_y,0});

    while ( !q.empty() ) {
        int x = get<0>(q.front());
        int y = get<1>(q.front());
        int key = get<2>(q.front());
        q.pop();

        if ( graph[x][y] == '1' ) return cnt[x][y][key] - 1;

        for ( int i = 0; i < 4; i++ ) {
            int nx = x + dx[i];
            int ny = y + dy[i];

            if ( nx < 0 || nx >= n || ny < 0 || ny >= m ) continue;
            
            if ( graph[nx][ny] == '#' || cnt[nx][ny][key] != 0 ) continue;

            if ( 'a' <= graph[nx][ny] && graph[nx][ny] <= 'f' ) {
                int nkey = key | (1 << (graph[nx][ny] - 'a'));
                if ( cnt[nx][ny][nkey] == 0 ) {
                    cnt[nx][ny][nkey] = cnt[x][y][key] + 1;
                    q.push({nx,ny,nkey});
                }
            } else if ( 'A' <= graph[nx][ny] && graph[nx][ny] <= 'F' ) {
                int check = key & (1 << (graph[nx][ny] - 'A')); 
                if ( check != 0 ) {
                    cnt[nx][ny][key] = cnt[x][y][key] + 1;
                    q.push({nx,ny,key});
                }
            } else {
                if ( cnt[nx][ny][key] == 0 ) {
                    cnt[nx][ny][key] = cnt[x][y][key] + 1;
                    q.push({nx,ny,key});                    
                }
            }
        }
    }
    return -1;
}


int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);

    cin >> n >> m;

    for ( int i = 0; i < n; i++ ) {
        for ( int j = 0; j < m; j++ ) {
            cin >> graph[i][j];
            if ( graph[i][j] == '0' ) {
                start_x = i;
                start_y = j;
            }
        }
    }

    cout << bfs();
    return 0;
}
```
