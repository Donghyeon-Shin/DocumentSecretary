# Concept
- 방향성이 있는 그래프에서 모든 정점이 다른 모든 정점에 방문할 수 있는 경우 이를 '강하게 연결되어 있다'고 표현하고 이것을 강한 연결 요소라고 한다.
- 전체 그래프가 강한 연결 요소가 아니더라도 부분이 강하게 연결되어 있으면 그 부분 그래프는 강한 연결 요소가 된다.
- SCC를 구하는 알고리즘은 Kosaraju's Algoritm(코사라주 알고리즘)과 Tarjan's Algorithm(타잔 알고리즘)이 있다.
- Kosaraju's Algoritm은 동작 과정에서 DFS를 순방향/역방향 2번을 해야하지만 Tarjan's Algorithm은 한번의 DFS로 구할 수 있기 때문에 대부분 Tarjan's Algorithm을 이용한다.
- 시간복잡도는 O(V+E)이다. / 노드 수(V), 간선 수(E)
# SCC 원리(Tarjan's Algorithm)
- 정점 번호가 낮은 노드에서 [[DFS(Depth-First Search)]]로 그래프를 탐색하면서 탐색 순서대로 고유 값(id)을 넣고 이를 Stack에 넣는다.
- SCC를 만족하는 명제는 '탐색하는 노드의 자식 노드들이  탐색하는 노드의 부모노드를 갈 수 없는 경우'이다.
- p라는 변수를 만들어 자신과 자신의 자식들 중 가장 id가 작은 값을 저장한다.
- p가 자기 id랑 같다면 강하게 연결되어 있다는 것을 뜻함으로 Stack에서 자기 자신이 나올때 까지 pop하여 자기 자신과 자신의 자식을 하나의 그룹으로 묶는다.
- 모든 노드의 탐색과 그룹화가 끝날 때까지 이를 반복한다.
#### 🖼️그림으로 이해하기
![[SCC Graph.svg]]
# SCC CODE
- SCC가 되는 조건에 주의하며 코드를 작성해야 한다.
- Finish Array를 통해 이미 SCC가 된 노드는 중복으로 들어가지 않게 처리해야 한다.
- 📑[2150 - Strongly Connected Component](https://www.acmicpc.net/problem/2150) 문제를 바탕으로 작성하였다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int v, e, parent[10001] = {0, }, id = 0;
bool finish[10001] = {0, };
stack<int> st;
vector<int> graph[10001];
vector<vector<int>> result;

int dfs(int node) {
    parent[node] = ++id;
    st.push(node);
    
    int p = parent[node];
    
    for ( int i = 0; i < (int)graph[node].size(); i++ ) {
        int nNode = graph[node][i];
        
        if ( parent[nNode] == 0 ) p = min(p, dfs(nNode));
        else if ( !finish[nNode] ) p = min(p, parent[nNode]);
    }
    
    if ( p == parent[node] ) {
        vector<int> scc;
        while( 1 ) {
            int n = st.top();
            st.pop();
            
            scc.push_back(n);
            finish[n] = true;
            if ( node == n ) break;
        }
        sort(scc.begin(), scc.end());
        result.push_back(scc);
    }
    return p;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> v >> e;
    for ( int i = 0; i < e; i++ ) {
        int n1, n2;
        cin >> n1 >> n2;
        graph[n1].push_back(n2);
    }
    
    for ( int i = 1; i <= v; i++ ) {
        if ( !finish[i] ) dfs(i);
    }
    
    sort(result.begin(), result.end());
    
    cout << (int)result.size() << '\n';
    for ( int i = 0; i < (int)result.size(); i++ ) {
        for ( int j = 0; j < (int)result[i].size(); j++ ) cout << result[i][j] << ' ';
        cout << "-1\n";
    }
    return 0;
}
```
##### ❓ 예제 Input
	9 12
	1 2
	2 3
	3 4
	4 6
	6 5
	5 4
	6 7
	7 6
	3 8
	8 3
	2 9
	9 1
##### ⭐ 예제 Output
	3
	1 2 9 -1
	3 8 -1
	4 5 6 7 -1
# SCC 응용문제
### 📑[4196 - 도미노](https://www.acmicpc.net/problem/4196)
#### 🔓 KeyPoint
- 하나의 도미노가 연결된 다른 도미노들을 쓰러트릴때 손으로 넘어트려야되는 최소 횟수를 구하는 문제이다.
- 하나의 SCC에 속한 도미노들은 그 그룹에 속한 어떤 도미노를 쓰려트려도 모두 넘어지게 된다.
- 하지만 다른 SCC에 속하더라도 연결되어 있다면 한번의 횟수만으로도 두 SCC 그룹을 다 넘어트릴 수 있다.
- 모든 SCC를 구하고 SCC간에 관계를 구해 다른 SCC의 자식이 아닌 SCC 그룹의 개수를 구하면 된다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int t, n, m, id, sccId, result;
int parent[100001], sccGroupId[100001], sccConnectedNum[100001];
bool finish[100001];
vector<int> graph[100001];
stack<int> st;

void init() {
    id = 0;
    sccId = 0;
    result = 0;
    memset(parent, 0, sizeof(parent));
    memset(sccGroupId, 0, sizeof(sccGroupId));
    memset(sccConnectedNum, 0, sizeof(sccConnectedNum));
    memset(finish, 0, sizeof(finish));
    for ( int i = 0; i < 100001; i++ ) graph[i].clear();
}

int dfs(int node) {
    parent[node] = ++id;
    int p = parent[node];
    
    st.push(node);
    
    for ( int i = 0; i < (int)graph[node].size(); i++ ) {
        int nNode = graph[node][i];
        
        if ( parent[nNode] == 0 ) p = min(p, dfs(nNode));
        else if ( !finish[nNode] ) p = min(p, parent[nNode]);
    }
    
    if ( p == parent[node] ) {
        while ( 1 ) {
            int n = st.top();
            st.pop();
            
            sccGroupId[n] = sccId;
            finish[n] = true;
            if ( node == n ) break; 
        }
        sccId++;
    }
    
    return p;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> t;
    while ( t-- ) {
        init();
        cin >> n >> m;
        for ( int i = 0; i < m; i++ ) {
            int x, y;
            cin >> x >> y;
            graph[x].push_back(y);
        }
        
        for ( int i = 1; i <= n; i++ ) {
            if ( !finish[i] ) dfs(i);
        }
        
        for ( int i = 1; i <= n; i++ ) {
            for ( int j = 0; j < (int)graph[i].size(); j++ ) {
                int node = graph[i][j];
                if ( sccGroupId[i] == sccGroupId[node] ) continue;
                sccConnectedNum[sccGroupId[node]]++;
            }
        }
        
        for ( int i = 0; i < sccId; i++ ) {
            if ( sccConnectedNum[i] == 0 ) result++;
        }
        
        cout << result << '\n';
    }
    return 0;
}
```
### 📑[3977 - 축구 전술](https://www.acmicpc.net/problem/3977)
#### 🔓 KeyPoint
- 도미노 문제와 비슷하게 SCC를 구하고 SCC간에 관계에서 root가 있는지 없는지를 판단하면 된다.
- SCC들의 root가 하나만 존재한다면 다른 모든 구역에 도달할 수 있지만 root가 여러 개가 존재할 경우 다른 모든 구역에 도달 할 수 없다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int t, n, m, id, sccId;
int parent[100001], sccGroupId[100001], sccConnectedNum[100001];
bool finish[100001];
stack<int> st;
vector<int> graph[100001];

void init() {
    id = 0;
    sccId = 0;
    memset(parent, 0, sizeof(parent));
    memset(sccGroupId, 0, sizeof(sccGroupId));
    memset(sccConnectedNum, 0, sizeof(sccConnectedNum));
    memset(finish, 0, sizeof(finish));
    for ( int i = 0; i < 100001; i++ ) graph[i].clear();
}

int dfs( int node ) {
    parent[node] = ++id;
    int p = parent[node];
    
    st.push(node);
    
    for ( int i = 0; i < (int)graph[node].size(); i++ ) {
        int nNode = graph[node][i];
        
        if ( parent[nNode] == 0 ) p = min(p, dfs(nNode));
        else if ( !finish[nNode] ) p = min(p, parent[nNode]);
    }
    
    if ( p == parent[node] ) {
        while ( 1 ) {
            int n = st.top();
            st.pop();
            
            sccGroupId[n] = sccId;
            finish[n] = true;
            if ( n == node ) break; 
        }
        sccId++;
    }
    
    return p;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> t;
    while ( t-- ) {
        init();
        cin >> n >> m;
        for ( int i = 0; i < m; i++ ) {
            int a, b;
            cin >> a >> b;
            graph[a].push_back(b);
        }
        
        for ( int i = 0; i < n; i++ ) {
            if ( !finish[i] ) dfs(i);
        }
        
        for ( int i = 0; i < n; i++ ) {
            for ( int j = 0; j < (int)graph[i].size(); j++ ) {
                int node = graph[i][j];
                if ( sccGroupId[i] == sccGroupId[node] ) continue;
                sccConnectedNum[sccGroupId[node]]++;
            }
        }
        
        int resultGroupId = -1;
        bool flag = true;
        for ( int i = 0; i < sccId; i++ ) {
            if ( sccConnectedNum[i] == 0 ) {
                if ( resultGroupId == -1 ) resultGroupId = i;
                else flag = false;
            }
        }
        
        if ( flag == false || resultGroupId == -1 ) cout << "Confused\n";
        else {
            for ( int i = 0; i < n; i++ ) {
                if ( sccGroupId[i] == resultGroupId ) cout << i << '\n';
            }
        }
        cout << '\n';
    }
    return 0;
}
```

