# Concept
- 소수를 구하는 대표적인 알고리즘이다.
- 2부터 원하는 수까지 배열로 나열하여 그 중 소수가 아닌 수들을 걸러내는 방법이다. 이 과정을 돌과 쌀을 나누는 '체'와 비슷하다고 하여 `에라토스테네스의 체`라고 한다.
- 특정 수(N)가 소수인지 아닌지를 판별하는 것이 아닌 2부터 N까지 소수가 무엇인지 구하는 알고리즘이다.
- N이 소수인지 아닌지 판별하는 알고리즘의 시간 복잡도는 O(N ** 0.5)이다.
- 시간 복잡도는 O(N x log N  x log N)이다.
# Sieve Of Eratosthenes 원리
- 2부터 차례대로 배수를 구하면서 N이하인 2의 배수들을 배열에서 제거해나가는 방식이다.
- 2부터 N의 제곱근까지 중 소수인 수의 자기 자신을 제외한 모든 배수들을 제거한다.
- 이미 소수가 아닌 수들은 다른 소수의 배수에 포함되므로 추가 연산을 진행할 필요가 없다.
#### 🖼️그림으로 이해하기
![[Sieve of Eratosthenes Graph.svg]]
# Sieve Of Eratosthenes CODE
- 1~n까지의 숫자들 중 소수가 무엇인지를 찾는 것이기 때문에 n이 커지면 커질 수록 계산 시간이 오래 걸린다.
- 문제를 고려해 어느 정도의 범위까지 찾는게 적절한지 판단하는게 중요하다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n;
bool isPrime[1000001] = {0, };

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n;
    memset(isPrime, 1, sizeof(isPrime));
    for ( int i = 2; i * i <= n; i++ ) {
        if ( isPrime[i] ) {
            for ( int j = i + i; j <= n; j += i ) isPrime[j] = false;
        }
    }
    
    for ( int i = 1; i <= n; i++ ) {
        if ( isPrime[i] ) cout << i << ' ';
    }
    return 0;
}
```
##### ❓ 예제 Input
	56

##### ⭐ 예제 Output
	2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 53
# Sieve Of Eratosthenes 응용문제
### 📑[1963 - 소수 경로](https://www.acmicpc.net/problem/1963)
#### 🔓 KeyPoint
- 4자리 소수에서 한 자리씩 수를 바꾸어 최종 원하는 소수로 바꾸는 과정에서 존재하는 모든 수가 소수인지, 만약 그렇다면 최소 몇 번의 과정을 거쳐야 하는지를 구하는 문제이다.
- 변환하는 과정에서 수들이 모두 소수인지 아닌지 알아야 하기 때문에 '에라토스테네스의 체'를 활용해야 한다.
- 수의 변환 경로를 [[BFS(Breadth-First Search)]]로  탐색해 구하면 된다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int t, n, target;
bool isPrime[10000] = {0, };

int bfs() {
    
    bool visited[10000] = {0, };
    queue<pair<int,int>> q;
    q.push({n, 0});
    
    visited[n] = true;
    
    while( !q.empty() ) {
        int num, cnt;
        tie(num, cnt) = q.front();
        q.pop();
        
        if ( num == target ) return cnt;
        for ( int i = 0; i < 4; i++ ) {
            for ( int j = 0; j <= 9; j++ ) {
                if ( i == 3 && j == 0 ) continue;
                int digit = (num / (int)pow(10, i)) % 10;
                int newNum = num - ((digit - j) * (int)pow(10, i));
                
                if ( isPrime[newNum] && !visited[newNum] ) {
                    visited[newNum] = true;
                    q.push({newNum, cnt+1});
                }
            }
        }
    }
    return -1;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    memset(isPrime, 1, sizeof(isPrime));
    
    for ( int i = 2; i <= sqrt(9999); i++ ) {
        if ( !isPrime[i] ) continue;
        for ( int j = i + i; j <= 9999; j += i ) isPrime[j] = false;
    }
    
    cin >> t;
    while( t-- ) {
        cin >> n >> target;
        int cnt = bfs();
        if ( cnt == -1 ) cout << "Impossible\n";
        else cout << cnt << '\n';
    }
    return 0;
}
```
### 📑[1017 - 소수 쌍](https://www.acmicpc.net/problem/1017)
#### 🔓 KeyPoint
- 여러 수로 이루어진 배열을 두 개의 쌍(그룹)으로 나누어 짝지었을때, 짝지은 모든 수들의 합이 소수가 되는지, 된다면 첫번째 수와 짝지어진 수들을 오름차순으로 나열하는 문제이다.
- 배열의 모든 쌍의 합이 소수인지 아닌지 판별하기 위해 '에라토스테네스의 체'를 이용한다.
- 2를 제외한 짝수는 소수가 아니기 때문에 배열을 두 개의 쌍으로 나눌 때 한쪽은 홀수만 한쪽은 짝수만으로 이루어지게 짜야하며, 이 나누어진 두 쌍의 원소 개수의 크기가 서로 다르다면 모든 수들을 짝지을수 없다.
- 두 그룹에서 미리 서로의 합이 소수가 되는 짝을 Edge로 이어놓고 방문 탐색을 하며 모든 수가 짝이 되는지 체크한다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, arr[51], mission[1001];
bool isPrime[2000], check[1001];
vector<int> graph[51], group_A, group_B;

bool dfs(int node) {
    if ( node == 1 || check[node] ) return false;
    check[node] = true;
    
    for ( int i = 0; i < (int)graph[node].size(); i++ ) {
        int target = graph[node][i];
        
        if ( mission[target] == 0 || dfs(mission[target]) ) {
            mission[target] = node;
            return true;
        }
    }
    
    return false;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    memset(isPrime, 1, sizeof(isPrime));
    for ( int i = 2; i <= sqrt(1999); i++ ) {
        if ( !isPrime[i] ) continue;
        for ( int j = i + i; j <= 1999; j += i ) isPrime[j] = false;
    }
    
    cin >> n;
    for ( int i = 1; i <= n; i++ ) cin >> arr[i];
    
    bool firstIsEven = (arr[1] % 2) ? false : true;
    
    for ( int i = 1; i <= n; i++ ) {
        if ( firstIsEven ) {
            if ( arr[i] % 2 == 0 ) group_A.push_back(i);
            else group_B.push_back(i);
        } else {
            if ( arr[i] % 2 == 0 ) group_B.push_back(i);
            else group_A.push_back(i);
        }
    }
    
    if ( (int)group_A.size() != (int)group_B.size() ) {
        cout << -1;
        return 0;
    }
    
    for ( int i = 0; i < (int)group_A.size(); i++ ) {
        int a = group_A[i];
        for ( int j = 0; j < (int)group_B.size(); j++ ) {
            int b = group_B[j];
            if ( isPrime[arr[a]+arr[b]] ) graph[a].push_back(b);
        }
    }
    
    vector<int> result;
    
    for ( int i = 0; i < (int)graph[1].size(); i++ ) {
        int b = graph[1][i];
        
        memset(mission, 0, sizeof(mission));
        mission[b] = 1;
        
        bool flag = false;
        
        for ( int j = 1; j < (int)group_A.size(); j++ ) {
            int next = group_A[j];
            memset(check, 0, sizeof(check));
            if ( !dfs(next) ) {
                flag = true;
                break;
            }
        }
        
        if ( !flag ) result.push_back(arr[b]);
        
    }
    
    if ( (int)result.size() == 0 ) {
        cout << -1;
        return 0;
    }
    
    sort(result.begin(), result.end());
    
    for ( int i = 0; i < (int)result.size(); i++ ) cout << result[i] << ' ';
    return 0;
}
```
