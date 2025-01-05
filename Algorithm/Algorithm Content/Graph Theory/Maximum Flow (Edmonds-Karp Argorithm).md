# Concept
- 방향 그래프(G)에서의 시작점(source), 종점(sink)까지 엣지 용량(capacity)을 고려해 최대 유량을  구하는 문제이다.
- 이를 구하기 위한 알고리즘을 에드몬드-카프(Edmonds-Karp Argorithm) 알고리즘이라고 한다.
- 노드 v,u에서 '흐를 수 있는 유량'을 capacity라고 하고 c(v,u)라고 표현하다.
- 실제 노드 v,u에서 '흐르는 유량'을 flow라고 하고 f(v,u)라고 표현한다.
- Capacity와 Flow를 합쳐서 F/C로 표기하기도 한다.
- 한 정점에서 다른 정점까지 흐를 수 있는 데이터의 최대 크기가 어느 정도인지를 확인하는 Network Flow라고도 부른다.

# Edmonds-Karp Argorithm 원리
- Source에서부터 [[BFS(Breadth-First Search)]]을 이용하여 모든 경의 수를 탐색한다.
- 처음에 모든 Flow를 0으로 설정한 뒤, Source -> Sink로 가는 경로의 최소 Capacity만큼 유량을 흘려보내준다.
- 유량을 흘려보내줄 때 반대편으로 음의 유량을 흘려보내야한다.(유량의 대칭성) 즉 f(v, u) += 5라면 f(u, v) -= 5로 표시한다. 이를 통해 새로운 경로를 만들어 더 많은 유량이 가도록 할 수 있다.
- 모든 경우의 탐색을 진행하면 Sink로 가는 모든 Flow가 Maximum Flow이다.
- 특별한 조건이 없는 이상 탐색 순서는 중요하지 않다.
- Edmonds-Karp Argorithm은 O(VE^2)이다.
#### 🖼️그림으로 이해하기
![[Maximum Flow Graph.svg]]

# Edmonds-Karp Argorithm CODE
- 유량의 대칭성을 생각하며 C(v, u)뿐 아니라 C(u, v)도 구현해야 한다.
- Parent Array를 통해 노드의 정보를 연결하고 Source와 Sink가 연결되면 Sink부터 Parent를 통해 역순으로 탐색하며 Minimum Flow를 찾으면 된다.
- Minimum Flow를 찾은 후, 다시 역순으로 탐색하며 parentNode -> node에는 +유량을 node -> parentNode에는 -유량을 더해준다.
- 모든 Minimum Flow의 합이 Maximum Flow이다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>
#define SOUR 1
#define SINK 7

using namespace std;

int e, capacity[52][52], flow[52][52];

int network_Flow(int source, int sink) {
    int result = 0;
    
    while ( 1 ) {
        int parent[52];
        memset(parent, -1, sizeof(parent));
        
        parent[source] = source;
        queue<int> q;
        q.push(source);
        
        while ( !q.empty() && parent[sink] == -1 ) {
            int node = q.front();
            q.pop();
            
            for ( int nNode = 0; nNode < 52; nNode++ ) {
                if ( capacity[node][nNode] - flow[node][nNode] > 0 && parent[nNode] == -1 ) {
                    parent[nNode] = node;
                    q.push(nNode);
                } 
            }
        }
        
        if ( parent[sink] == -1 ) break;
        
        int mini_Amount = 1e9;
        
        for( int node = sink; node != source; node = parent[node] ) mini_Amount = min(mini_Amount, capacity[parent[node]][node] - flow[parent[node]][node]);
        
        for( int node = sink; node != source; node = parent[node] ) {
            flow[parent[node]][node] += mini_Amount;
            flow[node][parent[node]] -= mini_Amount;
        }
        result += mini_Amount;
    }
    
    return result;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    memset(capacity, 0, sizeof(capacity));
    memset(flow, 0, sizeof(flow));
    
    cin >> e;
    for ( int i = 0; i < e; i++ ) {
        int v, u;
        int amount;
        cin >> v >> u >> amount;
        capacity[v][u] += amount;
    }
    
    cout << network_Flow(SOUR, SINK);
    return 0;
}
```
##### ❓ 예제 Input
	10
	1 2 8
	1 4 11
	2 3 4
	2 5 3
	2 7 6
	3 7 6
	4 5 10
	5 3 5
	5 6 10
	6 7 7
##### ⭐ 예제 Output
	18

# Maximum Flow 응용문제
### 📑[6086 - 최대 유량](https://www.acmicpc.net/problem/6086)
#### 🔓 KeyPoint
- Baisc한 Maximum Flow Problem이다.
- 양방향 간선이기 때문에 Capacity를 둘 다 입력해야 된다.
- 알파벳이 대문자와 소문자 둘 다 나오기 때문에 이를 고려해 수로 바꾼 뒤 Edmonds-Karp Argorithm을 사용하면 된다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, capacity[52][52], flow[52][52];

int alphToNum(char c) {
    if ( c >= 'A' && c <= 'Z' ) return c - 'A' + 26;
    else return c - 'a';
}

int network_Flow(int source, int sink) {
    int result = 0;
    
    while ( 1 ) {
        int parent[52];
        memset(parent, -1, sizeof(parent));
        
        parent[source] = source;
        queue<int> q;
        q.push(source);
        
        while ( !q.empty() && parent[sink] == -1 ) {
            int node = q.front();
            q.pop();
            
            for ( int nNode = 0; nNode < 52; nNode++ ) {
                if ( capacity[node][nNode] - flow[node][nNode] > 0 && parent[nNode] == -1 ) {
                    parent[nNode] = node;
                    q.push(nNode);
                } 
            }
        }
        
        if ( parent[sink] == -1 ) break;
        
        int mini_Amount = 1e9;
        
        for( int node = sink; node != source; node = parent[node] ) mini_Amount = min(mini_Amount, capacity[parent[node]][node] - flow[parent[node]][node]);
        
        for( int node = sink; node != source; node = parent[node] ) {
            flow[parent[node]][node] += mini_Amount;
            flow[node][parent[node]] -= mini_Amount;
        }
        result += mini_Amount;
    }
    
    return result;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    memset(capacity, 0, sizeof(capacity));
    memset(flow, 0, sizeof(flow));
    
    cin >> n;
    for ( int i = 0; i < n; i++ ) {
        char a, b;
        int amount;
        cin >> a >> b >> amount;
        int na = alphToNum(a);
        int nb = alphToNum(b);
        capacity[na][nb] += amount;
        capacity[nb][na] += amount;
    }
    
    cout << network_Flow(alphToNum('A'), alphToNum('Z'));
    return 0;
}
```
### 📑[11406 - 책 구매하기 2](https://www.acmicpc.net/problem/11406)
#### 🔓 KeyPoint
- Maximum Flow Problem을 책 구매 내용으로 바꾼 문제이다.
- Source는 책 구매자들과 연결해 각자 사고 싶은 책의 개수를 Capacity로 갖는다.
- Sink는 서점과 연결해 서점이 가지고 있는 책의 개수를 Capacity로 갖는다.
- 책 구매자가 한 서점과 연결해 살 수 있는 책의 개수를 Capacity로 갖는다.
- Sink에 들어오는 책의 양이 모든 사람들이 구매한 책의 최대 개수이다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>
#define INF 1e9
#define SOUR 1
#define SINK 2

using namespace std;

int n, m, capacity[205][205], flow[205][205], result_Cnt = 0;
vector<int> adj[205];

void mf() {
    while ( 1 ) {
        int parent[205];
        memset(parent, -1, sizeof(parent));
        
        queue<int> q;
        q.push(SOUR);
        
        while ( !q.empty() ) {
            int node = q.front();
            q.pop();
            
            for ( int i = 0; i < (int)adj[node].size(); i++ ) {
                int nNode = adj[node][i];
                
                if ( capacity[node][nNode] - flow[node][nNode] > 0 && parent[nNode] == -1 ) {
                    parent[nNode] = node;
                    q.push(nNode);
                }
            }
        }
        
        if ( parent[SINK] == -1 ) break;
        
        int amount = INF;
        for ( int i = SINK; i != SOUR; i = parent[i] ) amount = min(amount, capacity[parent[i]][i] - flow[parent[i]][i]);
        for ( int i = SINK; i != SOUR; i = parent[i] ) {
            flow[parent[i]][i] += amount;
            flow[i][parent[i]] -= amount;
        }
        
        result_Cnt += amount;
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n >> m;
    for ( int i = 3; i < n + 3; i++ ) {
        cin >> capacity[SOUR][i];
        adj[SOUR].push_back(i);
        adj[i].push_back(SOUR);
    }
    
    for ( int i = 3 + n; i < 3 + n + m; i++ ) {
        cin >> capacity[i][SINK];
        adj[i].push_back(SINK);
        adj[SINK].push_back(i);
    }
    
    for ( int i = 3 + n; i < 3 + n + m; i++ ) {
        for ( int j = 3; j < 3 + n; j++ ) {
            cin >> capacity[j][i];
            adj[j].push_back(i);
            adj[i].push_back(j);
        }
    }
    
    mf();
    cout << result_Cnt;
    return 0;
}
```