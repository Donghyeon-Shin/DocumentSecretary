# Concept
- 노드 탐색 방법 중 하나로 임의의 노드에서 다음 Branch로 넘어가기 전에 해당 Branch를 완벽하게 탐색하는 방법을 말한다.
- 하나의 Branch씩 탐색하기 때문에 보통 재귀를 이용해 구현한다.
- BFS와 마찬가지로 Visited Array로 중복 탐색을 방지한다.
- 노드의 개수 n, 간선의 개수 e이라 할 때 시간 복잡도는 O(n+e)

# DFS 원리
![[BASE TREE.svg]]
- [>] Node 1에서부터 탐색을 시작한다고 하자. 
	Node 1를 기준으로 왼쪽 Branch부터 탐색한다고 했을 때 Node 2, Node 4, Node 5가 순서대로 호출된다. 그 다음 재귀를 통해 다시 Node 4로 돌아가 오른쪽 Branch에 있는 Node 6을 탐색한다. Node 6은 다음 Branch가 없기 때문에 다른 Branch가 있는 Node 1번까지 올라가 Node 3을 탐색한다. 이러한 방식을 더 이상 탐색할 수 없을 때까지 반복한다.

이를 Recursion 순서도로 표현하자면 밑 그림처럼 된다.
#### 🖼️그림으로 이해하기
![[DFS Recursion.svg]]

# DFS CODE
- DFS는 반복문과 재귀를 이용하여 구현한다.
- 중복 탐색를 방지하는 것이 매우 중요하기 때문에 이를 신경쓰며 구현하여야 한다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n; // node cnt
int e; // edge cnt
int start; // start node
vector<int> graph[10001];
bool visited[10001] = {0, };

void dfs(int node) {
    cout << node << ' ';
    visited[node] = true;
    for ( int i = 0; i < (int)graph[node].size(); i++ ) {
        int nNode = graph[node][i];
        if ( !visited[nNode] ) dfs(nNode);
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n >> e;
    for ( int i = 0; i < e; i++ ) {
        int a, b;
        cin >> a >> b;
        graph[a].push_back(b);
        graph[b].push_back(a);
    }
    cin >> start;
    dfs(start);
    return 0;
}
```
##### ❓ 예제 Input
	10
	9
	1 2
	1 3
	2 4
	4 5
	4 6
	3 7
	3 8
	8 9
	8 10
	1
##### ⭐ 예제 Output
	1 2 4 5 6 3 7 8 9 10

# DFS 응용문제
### 📑[1012 - 유기농 배추](https://www.acmicpc.net/problem/1012)
#### 🔓 KeyPoint
- 그래프 이론에 DFS를 사용하는 대표적인 문제이다.
- Visited Array 대신 방문한 좌표에 Graph 값을 1에서 0으로 바꿈으로서 중복 탐색을 방지했다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int t, k, n, m, graph[51][51];
int dx[4] = {0, 0, 1, -1}, dy[4] = {1, -1, 0, 0};

bool dfs(int x, int y) {
    if ( graph[x][y] == 1 ) {
        graph[x][y] = 0;
        for ( int i = 0; i < 4; i++ ) {
            int nx = x + dx[i];
            int ny = y + dy[i];
            if ( x >= 0 && x <= m-1&& y >= 0 && y <= n-1 ) dfs(nx, ny);
        }
        return true;
    }
    return false;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> t;
    while ( t-- ) {
        int result = 0;
        memset(graph, 0, sizeof(graph));
        cin >> m >> n >> k;

        for ( int i = 0; i < k; i++ ) {
            int x, y;
            cin >> x >> y;
            graph[x][y] = 1;
        }
        
        for ( int i = 0; i < m; i++ ) {
            for ( int j = 0; j < n; j++ ) {
                if ( dfs(i,j) ) result++;
            }
        }
        cout << result << '\n';
    }
    return 0;
}
```
### 📑[1520 - 내리막 길](https://www.acmicpc.net/problem/1520)
#### 🔓 KeyPoint
- DFS와 DP를 합쳐서 풀어낼 수 있다.
- (1,1)에서 출발해 내리막 길을 찾는 것이 아니라 (m,n)에서 반대로 오르막 길을 찾아 올라가는 것이 핵심이다.
- Visited Array  사용해 중복 체크를 하는 것이 아닌 DP를 통해 이미 확인한 경로의 경우는 다시 탐색하는 것이 아니라 이미 계산했던 값을 가져와 중복 탐색을 방지한다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;	

int m, n, graph[500][500], dp[500][500];
int dx[4] = {0, 0, 1, -1}, dy[4] = {1, -1, 0, 0};

int dfs(int x, int y) {

	if ( dp[x][y] != -1 ) return dp[x][y];
	if ( x == 0 && y == 0 ) return 1;
	dp[x][y] = 0;
	
	for ( int i = 0; i < 4; i++ ) {
		int nx = x - dx[i];
		int ny = y - dy[i];

		if ( nx < 0 || nx >= m || ny < 0 || ny >= n ) continue;
		if ( graph[nx][ny] > graph[x][y] ) dp[x][y] += dfs(nx,ny);
	}
	return dp[x][y];
}

int main() {
	ios_base::sync_with_stdio(false);
	cin.tie(NULL); cout.tie(NULL);

	cin >> m >> n;
	for ( int i = 0; i < m; i++ ) {
		for ( int j = 0; j < n; j++ ) {
			cin >> graph[i][j];
			dp[i][j] = -1;
		}
	}

	dfs(m-1,n-1);
	cout << dp[m-1][n-1];
	return 0;
}
```