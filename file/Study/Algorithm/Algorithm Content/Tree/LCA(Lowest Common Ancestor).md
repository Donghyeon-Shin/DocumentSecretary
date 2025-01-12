# Concept
- Tree에서 두 노드(v, u)가 있을 때, 그 두 노드의 최소 공통 조상을 찾는 알고리즘이다.
- LCA 구하는 방법에는 여러가지 방법이 있다.
	1. 두 노드의 깊이를 맞춘 다음 한 칸씩 올라가며 공통 조상을 찾는 방법 `O(n) / 트리의 깊이 : n`
	2. 1번 방법과 유사하지만 한 칸씩 올라가는 것이 아닌 [[DP(Dynamic Programming)]]을 이용해 2^i만큼 올라가며 조상을 비교하는 방법 `O(logN) / 트리의 깊이 : n`
- 2번 방법이 시간복잡도면에서 효율적이기 때문에 대부분 2번 방법을 이용해 LCA를 구한다.
# LCA 원리 (📑[11438 - LCA 2](https://www.acmicpc.net/problem/11438))
- LCA은 각 노드들의 [[DFS(Depth-First Search)]]를 이용해 노드의 level(깊이) & parent Array를 채우는 과정과 두 노드(v, u)의 조상을 찾는 과정으로 나눌 수 있다.
- LCA는 `level[i] = i번 노드의 깊이`와 `parent[i][j] = i의 2^j의 부모`의 정보를 토대로 찾게된다.
- level과 parent를 알기 위해 root 노드부터 시작해서 자식 노드(child)로 내려가며 `level[child][i] = 1씩 증가하고 parent[child][j]를 j = 1 ~ MAX_HEIGHT(Tree 최대 깊이)까지 업데이트 한다.` ( j = 0인 경우는 업데이트 전 초기에 `parent[child][0] = p(부모)`로 설정한다)
- `parent[i][j] = parent[parent[i][j-1][j-1]`를 만족하기 때문에 이를 이용해 parent를 업데이트 한다.
- 두 노드를 찾는 과정에서는 우선 두 노드 중 level이 큰 노드(v)가 다른 노드(u)와 level이 비슷해질 때까지 parent를 통해 v를 움직인다(단 이때 `level[v] < level[u]`면 안된다). 두 노드들을 같은 크기만큼 p(부모)를 비교하여 두 노드의 p가 같으면 공통 노드인 것이다. 이 공통 노드 중 가장 깊이가 깊은 것이 LCA이다.
- 노드의 p를 비교할 때`j = 2^(MAX_HEIGHT - 1) ~ 2^0 (MAX_HEIGHT : log(Maximum Height))`순으로 비교해야 모든 노드를 비교할  수 있다. (0부터 비교하게 되면 2^0, 2^1, 2^2...만큼의 p만 비교하기 때문에 중간에 노드들을 건너뛸 수가 있다.)
- LCA 찾는 과정에서 두 노드가 움직일 때 두 노드의 공통 부모가 아니라면 두 노드를 움직이여야한다. 그리고 LCA는 움직임 유무 상관없이 `LCA = parent[v][i]`로 업데이트 해주어야 한다.
#### 🖼️그림으로 이해하기
![[LCA Graph.svg]]
# LCA CODE
- LCA는 말보다 코드로 보는 것이 이해하기 더 쉬울 수 있기 때문에 직접 코드를 작성해보는 것이 좋다.
- root노드를 1번 노드로 고정했지만 상황에 따라 dfs Parameter에 원하는 노드를 넣으면 된다.
- dfs의 visited는 level로 대처 가능하기 때문에 초기에 level Array를 -1로 초기화 해준다.
- 처음 level을 맞추는 과정은 `level[v] == level[u]`라면 할 필요없고 LCA를 찾는 과정은 `v == u`라면 할 필요가 없다.
- LCA의 경우 공통 조상중 가장 깊이가 깊은 조상을 저장할 수 있도록 계속 업데이트 한다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>
#define MAX_HEIGHT 18

using namespace std;

int n, m, level[100001], parent[100001][MAX_HEIGHT];
vector<int> graph[100001];

void dfs(int node, int height, int p) {

    level[node] = height;
    parent[node][0] = p;
    for ( int i = 1; i < MAX_HEIGHT; i++ ) parent[node][i] = parent[parent[node][i-1]][i-1];
    
    for ( int i = 0; i < (int)graph[node].size(); i++ ) {
        int nNode = graph[node][i];
        if ( level[nNode] == -1 ) dfs(nNode, height+1, node);
    }
}

int get_Common_Ancestor(int n1, int n2) {
    
    if ( n1 == 1 || n2 == 1 ) return 1;
    
    if ( level[n1] != level[n2] ) {
        for ( int i = MAX_HEIGHT - 1; i >= 0; i-- ) {
            if ( level[parent[n1][i]] >= level[n2] ) n1 = parent[n1][i];
        }
    }
    
    int result = n1;
    if ( n1 != n2 ) {
        for ( int i = MAX_HEIGHT - 1; i >= 0; i-- ) {
            if ( parent[n1][i] != parent[n2][i] ) {
                n1 = parent[n1][i];
                n2 = parent[n2][i];
            }
            result = parent[n1][i];
        }
    }
    
    return result;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    memset(level, -1, sizeof(level));
    
    cin >> n;
    for ( int i = 0; i < n-1; i++ ) {
        int n1, n2;
        cin >> n1 >> n2;
        graph[n1].push_back(n2);
        graph[n2].push_back(n1);
    }
    
    dfs(1, 1, 0);
    
    cin >> m;
    for ( int i = 0; i < m; i++ ) {
        int n1, n2;
        cin >> n1 >> n2;
        if ( level[n1] > level[n2] ) cout << get_Common_Ancestor(n1, n2) << '\n';
        else cout << get_Common_Ancestor(n2, n1) << '\n';
    }
    return 0;
}
```
##### ❓ 예제 Input
	15
	1 2
	1 3
	2 4
	2 5
	4 8
	4 9
	3 6
	3 7
	6 10
	7 11
	7 12
	9 13
	9 14
	10 15
	3
	5 6
	10 7
	13 4
##### ⭐ 예제 Output
	1
	3
	4
# LCA 응용문제
### 📑[1761 - 정점들의 거리](https://www.acmicpc.net/problem/1761)
#### 🔓 KeyPoint
- LCA를 구하는 대표적인 문제이다.
- 노드들의 연결 정보와 연결 간선사이의 거리가 주어질 때 두 노드(v, u)의 거리를 구해야 한다.
- `cost[i] = root 노드에서 i번째 노드까지의 거리`를 dfs를 통해 구한다.
- 노드 v, u의 LCA(x)를 구하고 `cost[v] + cost[u] - 2 * cost[x]`를 계산하면 두 노드 v, u의 거리가 나온다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>
#define MAX_HEIHGT 17

using namespace std;

int n, m, level[40001], cost[40001], parent[40001][MAX_HEIHGT];
vector<pair<int,int>> graph[40001];

void dfs(int node, int height, int p, int c) {
    
    level[node] = height;
    cost[node] = c;
    parent[node][0] = p;
    
    for ( int i = 1; i < MAX_HEIHGT; i++ ) parent[node][i] = parent[parent[node][i-1]][i-1];
    
    for ( int i = 0; i < (int)graph[node].size(); i++ ) {
        int nNode, nCost;
        tie(nNode, nCost) = graph[node][i];
        if ( level[nNode] == -1 ) dfs(nNode, height+1, node, c + nCost);
    }
}

int get_Common_Ancestor(int n1, int n2) {
    
    if ( n1 == 1 || n2 == 1 ) return 1;
    
    if ( level[n1] != level[n2] ) {
        for ( int i = MAX_HEIHGT - 1; i >= 0; i-- ) {
            if ( level[parent[n1][i]] >= level[n2] ) n1 = parent[n1][i];
        }
    }
    
    int result = n1;
    if ( n1 != n2 ) {
        for ( int i = MAX_HEIHGT - 1; i >= 0; i-- ) {
            if ( parent[n1][i] != parent[n2][i] ) {
                n1 = parent[n1][i];
                n2 = parent[n2][i];
            }
            result = parent[n1][i];
        }
    }
    
    return result;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    memset(level, -1, sizeof(level));
    
    cin >> n;
    for ( int i = 0; i < n - 1; i++) {
        int n1, n2, c;
        cin >> n1 >> n2 >> c;
        graph[n1].push_back({n2,c});
        graph[n2].push_back({n1,c});
    }
    
    dfs(1, 1, 0, 0);
    
    cin >> m;
    for ( int i = 0; i < m; i++ ) {
        int n1, n2, ancestor;
        cin >> n1 >> n2;
        ancestor = ( level[n1] > level[n2] ) ? get_Common_Ancestor(n1, n2) : get_Common_Ancestor(n2, n1);
        cout << cost[n1] + cost[n2] - 2 * cost[ancestor] << '\n';
    }
    return 0;
}
```
### 📑[3176 - 도로 네트워크](https://www.acmicpc.net/problem/3176)
#### 🔓 KeyPoint
- 두 노드(v, u)의 LCA(x)를 구하고 그 사이의 존재하는 간선들을 비교해야 하는 문제이다.
- 두 노드를 연결하는 간선들은 `v - x에 존재하는 간선, x - u에 존재하는 간선`이다.
- `road[i][j].first = i와 i의 2^j의 부모 사이에 존재하는 간선 중 작은 값`, `road[i][j].second = i와 i의 2^j의 부모 사이에 존재하는 간선 중 가장 큰 값`을 선언해 `parent[i][j]`와 같이 업데이트 한다.
- x를 구한 다음 v와 x사이의 간선, u와 x사이의 간선 사이에 있는 도로의 최소 값과 최대 값을 LCA를 구했던 것과 마찬가지로 `road[child][j]를 j = 1 ~ MAX_HEIGHT(Tree 최대 깊이)`를 통해 구한다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>
#define MAX 100001
#define MAX_HEIGHT 18

using namespace std;

int n, m, level[MAX], parent[MAX][MAX_HEIGHT];
pair<int,int> road[MAX][MAX_HEIGHT];
vector<pair<int,int>> graph[MAX];

void dfs(int node, int height, int p, int dist) {

    road[node][0] = {dist, dist};
    parent[node][0] = p;
    level[node] = height;
   
    for ( int i = 1; i < MAX_HEIGHT; i++ ) {
        parent[node][i] = parent[parent[node][i-1]][i-1];
        road[node][i].first = min(road[node][i-1].first, road[parent[node][i-1]][i-1].first);
        road[node][i].second = max(road[node][i-1].second, road[parent[node][i-1]][i-1].second);
    }
   
    for ( int i = 0; i < (int)graph[node].size(); i++ ) {
        int nNode, nDist;
        tie(nNode, nDist) = graph[node][i];
        if ( level[nNode] == -1 ) dfs(nNode, height + 1, node, nDist);
    }
}

int get_Common_Ancestor(int n1, int n2) {
   
    if ( n1 == 1 || n2 == 1 ) return 1;
   
    if ( level[n1] != level[n2] ) {
        for ( int i = MAX_HEIGHT - 1; i >= 0; i-- ) {
            if ( level[parent[n1][i]] >= level[n2] ) {
                n1 = parent[n1][i];      
            }
        }
    }
   
    int result = n1;
   
    if ( n1 != n2 ) {
        for ( int i = MAX_HEIGHT - 1; i >= 0; i-- ) {
            if ( parent[n1][i] != parent[n2][i] ) {
                n1 = parent[n1][i];
                n2 = parent[n2][i];
            }
            result = parent[n1][i];
        }
    }
    return result;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    cout.tie(NULL);
    memset(level, -1, sizeof(level));
   
    cin >> n;
    for ( int i = 0; i < n-1; i++ ) {
        int n1, n2, cost;
        cin >> n1 >> n2 >> cost;
        graph[n1].push_back({n2, cost});
        graph[n2].push_back({n1, cost});
    }
   
    dfs(1, 1, 0, 0);
   
    cin >> m;
    for ( int i = 0; i < m; i++ ) {
        int n1, n2;
        int minimum = 1e9, maximum = -1;
        cin >> n1 >> n2;
        int lca = ( level[n1] > level[n2] ) ? get_Common_Ancestor(n1, n2) : get_Common_Ancestor(n2, n1);
        
        for ( int i = MAX_HEIGHT - 1; i >= 0; i-- ) {
            if ( parent[n1][i] == 0 ) continue;
            
            if ( lca == parent[n1][i] ) {
                minimum = min(minimum, road[n1][i].first);
                maximum = max(maximum, road[n1][i].second);
                break;
            }
            
            if ( level[lca] < level[parent[n1][i]] ) {
                minimum = min(minimum, road[n1][i].first);
                maximum = max(maximum, road[n1][i].second);
                n1 = parent[n1][i];
            }
        }

        for ( int i = MAX_HEIGHT - 1; i >= 0; i-- ) {
            if ( lca == parent[n2][i] ) {
                minimum = min(minimum, road[n2][i].first);
                maximum = max(maximum, road[n2][i].second);
                break;
            }
            
            if ( level[lca] < level[parent[n2][i]] ) {
                minimum = min(minimum, road[n2][i].first);
                maximum = max(maximum, road[n2][i].second);
                n2 = parent[n2][i];
            }
        }
        cout << minimum << ' ' << maximum << '\n';
    }
    return 0;
}

```
